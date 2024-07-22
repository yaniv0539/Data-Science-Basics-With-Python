import json


# Decipher a given phrase using the provided lexicon and alphabet files.
def decipher_phrase(phrase, lexicon_filename, abc_filename):
    print(f'starting deciphering using {lexicon_filename} and {abc_filename}')

    if phrase == "":
        return {"status": 2, "orig_phrase": '', "K": 0}

    separated_phrase = phrase.split(" ")

    with open(lexicon_filename, 'r', encoding='utf-8') as file_arr:
        lexicon_arr = file_arr.read().splitlines()

    with open(abc_filename, 'r', encoding='utf-8') as abc_arr:
        abc_arr = abc_arr.read().splitlines()

    found, orig_arr, k = valid_sentence(separated_phrase, abc_arr, lexicon_arr)

    status = 1

    if found:
        status = 0

    orig_string = " ".join(orig_arr)

    return {"status": status, "orig_phrase": orig_string, "K": k}


# Convert a word using a Caesar cipher with a given shift value.
def convert_word(word, k, abc_arr):
    array_result = []
    for letter in word:
        array_result.append(abc_arr[abc_arr.index(letter) - k])
    result_string = ''.join(array_result)
    return result_string


# Check if a word is present in a dictionary.
def word_in_dictionary(dictionary, word):
    for try_word in dictionary:
        if try_word == word:
            return True
    return False


# Check if a separated phrase can be deciphered using the provided alphabet and lexicon.
def valid_sentence(separated_phrase, abc_arr, lexicon_arr):
    found = True
    i = 0
    orig_arr = list()

    for i in range(0, len(abc_arr)):
        found = True

        for word in separated_phrase:
            word = convert_word(word, i, abc_arr)

            if not word_in_dictionary(lexicon_arr, word):
                orig_arr = list()
                found = False
                break

            orig_arr.append(word)

        if found:
            break

    return found, orig_arr, i

# todo: fill in your student ids
students = {'id1': '209028349', 'id2': '206593444'}

if __name__ == '__main__':
    with open('config-decipher.json', 'r') as json_file:
        config = json.load(json_file)

    result = decipher_phrase(config['secret_phrase'],
                             config['lexicon_filename'],
                             config['abc_filename'])

    assert result["status"] in {0, 1, 2}

    if result["status"] == 0:
        print(f'deciphered phrase: {result["orig_phrase"]}, K: {result["K"]}')
    elif result["status"] == 1:
        print("cannot decipher the phrase!")
    else:  # result["status"] == 2:
        print("empty phrase")