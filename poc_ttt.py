"""
Monte Carlo Tic-Tac-Toe Player
"""
import random
import poc_ttt_gui
import poc_ttt_provided as provided

NTRIALS = 1000
SCORE_CURRENT = 1.0
SCORE_OTHER = 1.0

def mc_trial(board, player):
    empty_squares = board.get_empty_squares()
    while not board.check_win():
        row, col = random.sample(empty_squares, 1)[0]
        board.move(row, col, player)
        player = provided.switch_player(player)
        empty_squares.remove((row, col))

def mc_update_scores(scores, board, player):
    win = board.check_win()
    if win == provided.DRAW:
        return
    dim = board.get_dim()
    for row in range(dim):
        for col in range(dim):
            square = board.square(row, col)
            if square == provided.EMPTY:
                continue
            if win == player:
                if square == player:
                    scores[row][col] += SCORE_CURRENT
                else: # square != player
                    scores[row][col] -= SCORE_OTHER
            else: # win != player:
                if square == player:
                    scores[row][col] -= SCORE_CURRENT
                else: # square != player
                    scores[row][col] += SCORE_OTHER

def get_best_move(board, scores):
    empty_squares = board.get_empty_squares()
    if not len(empty_squares):
        return
    max_squares = [empty_squares[0]]
    max_score = scores[empty_squares[0][0]][empty_squares[0][1]]
    for square in empty_squares:
        row, col = square
        if scores[row][col] == max_score:
            max_squares.append(square)
        elif scores[row][col] > max_score:
            max_squares = [square]
            max_score = scores[row][col]
    return random.sample(max_squares, 1)[0]

def mc_move(board, player, trials):
    dim = board.get_dim()
    scores = [[0] * dim for _ in range(dim)]
    for _ in range(trials):
        clone = board.clone()
        mc_trial(clone, player)
        mc_update_scores(scores, clone, player)
    return get_best_move(board, scores)

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
