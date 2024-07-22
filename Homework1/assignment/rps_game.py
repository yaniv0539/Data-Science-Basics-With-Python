import json


# Run the game with the provided results file.
def game(results_filename):
    print(f'starting the game with {results_filename}')

    with open(results_filename, "r") as fin:
        names_and_moves = fin.read().split()

    names = names_and_moves[:2]
    moves = names_and_moves[2:]

    players = {f"player{i}": {"moves": list(), "wins": 0} for i in range(1, 3)}

    players = add_moves_to_players(players, moves)

    for i in range(len(players["player1"]["moves"])):
        determine_round_winner(players, i)

    return determine_game_winner(players)


# Determine the winner of a round and update players' wins.
def determine_round_winner(players, round_index):
    if players["player1"]["moves"][round_index] == players["player2"]["moves"][round_index]:
        pass
    elif (
        (players["player1"]["moves"][round_index] == "rock" and players["player2"]["moves"][round_index] == "scissors")
        or (players["player1"]["moves"][round_index] == "scissors" and players["player2"]["moves"][round_index] == "paper")
        or (players["player1"]["moves"][round_index] == "paper" and players["player2"]["moves"][round_index] == "rock")
    ):
        players["player1"]["wins"] += 1
    else:
        players["player2"]["wins"] += 1


# Determine the winner of the game.
def determine_game_winner(players):
    if players["player1"]["wins"] > players["player2"]["wins"]:
        return "player1"
    elif players["player1"]["wins"] < players["player2"]["wins"]:
        return "player2"
    else:
        return "tie"


# Add moves to the players' moves list.
def add_moves_to_players(players, moves):
    for i in range(len(moves)):
        player_key = "player1" if i % 2 == 0 else "player2"
        players[player_key]["moves"].append(moves[i])

    return players

# todo: fill in your student ids
students = {'id1': '209028349', 'id2': '206593444'}

if __name__ == '__main__':
    with open('config-rps.json', 'r') as json_file:
        config = json.load(json_file)

    winner = game(config['results_filename'])
    print(f'the winner is: {winner}')
