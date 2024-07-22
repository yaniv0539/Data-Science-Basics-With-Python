import time
import json
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from typing import List
from scipy.spatial.distance import cdist
from collections import Counter
import numpy as np

def classify_with_NNR(data_trn: str, data_vld: str, df_tst: pd.DataFrame) -> List:
    df_train = pd.read_csv(data_trn)
    df_valid = pd.read_csv(data_vld)

    df_train_class = df_train.iloc[:, -1]
    df_valid_class = df_valid.iloc[:, -1]

    df_train.drop(columns=df_train.columns[-1], inplace=True)
    df_valid.drop(columns=df_valid.columns[-1], inplace=True)

    scaler_train = StandardScaler()
    scaler_valid = StandardScaler()

    scaler_train.fit(df_train)
    scaler_valid.fit(df_valid)

    predictors_scaled_train = scaler_train.transform(df_train)
    predictors_scaled_valid = scaler_valid.transform(df_valid)

    distances = cdist(predictors_scaled_valid, predictors_scaled_train, 'euclidean')

    mean_radius = np.mean(distances, axis=1)

    # Initialize success counter
    success_counter = 0

    for i, radius in enumerate(mean_radius):
        # Count occurrences of each class within the radius
        class_counter = Counter(df_train_class[distances[i] <= radius])

        if class_counter:  # Check if any classes are found within the radius
            # Get the predicted class with the highest count
            predicted_class = class_counter.most_common(1)[0][0]

            # Update success counter if the predicted class matches the true class
            if df_valid_class[i] == predicted_class:
                success_counter += 1

    success_rate = success_counter / len(df_valid_class)
    print("Success rate:", success_rate)

    print(f'Starting classification with {data_trn}, {data_vld}, predicting on {len(df_tst)} instances')

    predictions = list()  # todo: return a list of your predictions for test instances
    return predictions


if __name__ == '__main__':
    start = time.time()

    with open('config.json', 'r', encoding='utf8') as json_file:
        config = json.load(json_file)

    df = pd.read_csv(config['data_file_test'])
    predicted = classify_with_NNR(config['data_file_train'],
                                  config['data_file_validation'],
                                  df.drop(['class'], axis=1))

    labels = df['class'].values
    if not predicted:  # empty prediction, should not happen in your implementation
        predicted = list(range(len(labels)))

    assert(len(labels) == len(predicted))  # make sure you predict label for all test instances
    print(f'test set classification accuracy: {accuracy_score(labels, predicted)}')

    print(f'total time: {round(time.time()-start, 0)} sec')
