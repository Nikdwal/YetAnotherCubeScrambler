import kociemba

# the inverse of a single move
def inverse_move(move : str):
    if len(move) <= 1:
        return move + "\'"
    if move[-1] == "'":
        return move[0]
    return move

# the inverse of an algorithm
def inverse_alg(alg : str):
    return " ".join(reversed([inverse_move(move) for move in alg.split(" ")]))

# generate an algorithm for the given random state
def generate_state(random_state):
    return inverse_alg(kociemba.solve(random_state))
