import numpy as np
import math
import chess

# global variables
global ai_player, board
board = np.array([["R2", "N2", "B2", "Q2", "K2", "B2", "N2", "R2"],
                  ["P2", "P2", "P2", "P2", "P2", "P2", "P2", "P2"],
                  ["--", "--", "--", "--", "--", "--", "--", "--"],
                  ["--", "--", "--", "--", "--", "--", "--", "--"],
                  ["--", "--", "--", "--", "--", "--", "--", "--"],
                  ["--", "--", "--", "--", "--", "--", "--", "--"],
                  ["P1", "P1", "P1", "P1", "P1", "P1", "P1", "P1"],
                  ["R1", "N1", "B1", "Q1", "K1", "B1", "N1", "R1"]])

max_depth = 4
ai_player = None

# Evaluation matrices for black pieces
pawn_matrix = [[0,  0,  0,  0,  0,  0,  0,  0],
               [5, 10, 10,-20,-20, 10, 10,  5],
               [5, -5,-10,  0,  0,-10, -5,  5],
               [0,  0,  0, 20, 20,  0,  0,  0],
               [5,  5, 10, 25, 25, 10,  5,  5],
               [10, 10, 20, 30, 30, 20, 10, 10],
               [50, 50, 50, 50, 50, 50, 50, 50],
               [0,  0,  0,  0,  0,  0,  0,  0]]

knight_matrix = [[-50,-40,-30,-30,-30,-30,-40,-50],
                 [-40,-20,  0,  5,  5,  0,-20,-40],
                 [-30,  5, 10, 15, 15, 10,  5,-30],
                 [-30,  0, 15, 20, 20, 15,  0,-30],
                 [-30,  5, 15, 20, 20, 15,  5,-30],
                 [-30,  0, 10, 15, 15, 10,  0,-30],
                 [-40,-20,  0,  0,  0,  0,-20,-40],
                 [-50,-40,-30,-30,-30,-30,-40,-50]]

bishop_matrix = [[-20,-10,-10,-10,-10,-10,-10,-20],
                 [-10,  5,  0,  0,  0,  0,  5,-10],
                 [-10, 10, 10, 10, 10, 10, 10,-10],
                 [-10,  0, 10, 10, 10, 10,  0,-10],
                 [-10,  5,  5, 10, 10,  5,  5,-10],
                 [-10,  0,  5, 10, 10,  5,  0,-10],
                 [-10,  0,  0,  0,  0,  0,  0,-10],
                 [-20,-10,-10,-10,-10,-10,-10,-20]]

rook_matrix = [[ 0,  0,  0,  5,  5,  0,  0,  0],
               [-5,  0,  0,  0,  0,  0,  0, -5],
               [-5,  0,  0,  0,  0,  0,  0, -5],
               [-5,  0,  0,  0,  0,  0,  0, -5],
               [-5,  0,  0,  0,  0,  0,  0, -5],
               [-5,  0,  0,  0,  0,  0,  0, -5],
               [ 5, 10, 10, 10, 10, 10, 10,  5],
               [ 0,  0,  0,  0,  0,  0,  0,  0]]

queen_matrix = [[-20,-10,-10, -5, -5,-10,-10,-20],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-10,  5,  5,  5,  5,  5,  0,-10],
                [  0,  0,  5,  5,  5,  5,  0, -5],
                [ -5,  0,  5,  5,  5,  5,  0, -5],
                [-10,  0,  5,  5,  5,  5,  0,-10],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-20,-10,-10, -5, -5,-10,-10,-20]]

king_matrix = [[ 20, 30, 10,  0,  0, 10, 30, 20],
               [ 20, 20,  0,  0,  0,  0, 20, 20],
               [-10,-20,-20,-20,-20,-20,-20,-10],
               [-20,-30,-30,-40,-40,-30,-30,-20],
               [-30,-40,-40,-50,-50,-40,-40,-30],
               [-30,-40,-40,-50,-50,-40,-40,-30],
               [-30,-40,-40,-50,-50,-40,-40,-30],
               [-30,-40,-40,-50,-50,-40,-40,-30]]


# function to get sum of all the points of pieces of the given player on the board
def getMaterialisticSum(board_copy, player):
    totalSum = 0
    index = "1"

    if player == "black":
        index = "2"

    for row in board_copy:
        for col in row:
            if col[1] == index:
                if col[0] == "R":
                    totalSum += 500
                elif col[0] == "P":
                    totalSum += 100
                elif col[0] == "N":
                    totalSum += 320
                elif col[0] == "B":
                    totalSum += 330
                elif col[0] == "Q":
                    totalSum += 900
                elif col[0] == "K":
                    totalSum += 1000
    if player == "white":
        return -1 * totalSum
    return totalSum


# function to get sum of all the heuristic points of pieces of the given player on the board
def getHeuristicSum(board_copy, player):
    totalSum = 0
    index = "2"
    sub_factor = 0

    if player == "white":
        index = "1"
        sub_factor = 7

    for i in range(board_copy.shape[0]):
        for j in range(board_copy.shape[1]):
            if board_copy[i][j][1] == index:
                if board_copy[i][j][0] == "R":
                    totalSum += rook_matrix[abs(i - sub_factor)][j]
                elif board_copy[i][j][0] == "P":
                    totalSum += pawn_matrix[abs(i - sub_factor)][j]
                elif board_copy[i][j][0] == "N":
                    totalSum += knight_matrix[abs(i - sub_factor)][j]
                elif board_copy[i][j][0] == "B":
                    totalSum += bishop_matrix[abs(i - sub_factor)][j]
                elif board_copy[i][j][0] == "Q":
                    totalSum += queen_matrix[abs(i - sub_factor)][j]
                elif board_copy[i][j][0] == "K":
                    totalSum += king_matrix[abs(i - sub_factor)][j]
    if player == "white":
        return -1 * totalSum
    return totalSum


# function to evaluate the board
def evaluateBoard(board_copy, player):
    totalSum = getMaterialisticSum(board_copy, player)
    totalSum += getHeuristicSum(board_copy, player)
    return totalSum


# function to check winner of the game
def checkWinner():
    if not np.asarray(np.where(board == "K2")).T.tolist():
        return -10000
    elif not np.asarray(np.where(board == "K1")).T.tolist():
        return 10000
    return 0


# function to get pieces of the given player on the board
def getPieces(board_copy, player):
    index = "1"
    if player == "black":
        index = "2"

    pieces = []
    for i in range(len(board_copy)):
        for j in range(len(board_copy[0])):
            if board_copy[i][j][1] == index:
                pieces.append((board_copy[i][j], (i, j)))
    return pieces


# max value in minimax
def maxValue(board_copy, depth, alpha, beta, kd1, lrd1, rrd1, kd2, lrd2, rrd2):
    winner = checkWinner()
    if winner != 0:
        return winner
    if depth == 0:
        return evaluateBoard(board_copy, "black")
    v = -math.inf
    pieces = getPieces(board_copy, "black")
    for piece in pieces:
        for move in chess.movesPossible(board_copy, piece[0], piece[1][0], piece[1][1], kd1, lrd1, rrd1):
            skip_move = False
            if piece[0][0] == 'K' and kd1 == 0 and (move[1] == 6 or move[1] == 2):
                board_temp = np.copy(board_copy)
                board_temp = chess.applyMove(board_temp, piece, move)
                board_temp1 = np.copy(board_copy)
                if move[1] == 2:
                    board_temp1 = chess.applyMove(board_temp1, piece, (move[0], move[1] + 1))
                else:
                    board_temp1 = chess.applyMove(board_temp1, piece, (move[0], move[1] - 1))

                if chess.check(board_temp, "black", kd2, lrd2, rrd2) or chess.check(board_copy, "black", kd2, lrd2, rrd2) or \
                        chess.check(board_temp1, "black", kd2, lrd2, rrd2):
                    skip_move = True

            if not skip_move:
                if piece[0][0] == 'K':
                    kd1 = 1
                if piece[0][0] == 'R' and piece[1][1] == 0:
                    lrd1 = 1
                if piece[0][0] == 'R' and piece[1][1] == 7:
                    rrd1 = 1

                v = max(v, minValue(chess.applyMove(np.copy(board_copy), piece, move), depth - 1, alpha, beta, kd2, lrd2, rrd2, kd1, lrd1, rrd1))
                alpha = max(alpha, v)
                if alpha >= beta:
                    return v
    return v


# min value in minimax
def minValue(board_copy, depth, alpha, beta, kd1, lrd1, rrd1, kd2, lrd2, rrd2):
    winner = checkWinner()
    if winner != 0:
        return winner
    if depth == 0:
        return evaluateBoard(board_copy, "white")
    v = math.inf
    pieces = getPieces(board_copy, "white")
    for piece in pieces:
        for move in chess.movesPossible(board_copy, piece[0], piece[1][0], piece[1][1], kd1, lrd1, rrd1):
            skip_move = False
            if piece[0][0] == 'K' and kd1 == 0 and (move[1] == 6 or move[1] == 2):
                board_temp = np.copy(board_copy)
                board_temp = chess.applyMove(board_temp, piece, move)
                board_temp1 = np.copy(board_copy)
                if move[1] == 2:
                    board_temp1 = chess.applyMove(board_temp1, piece, (move[0], move[1] + 1))
                else:
                    board_temp1 = chess.applyMove(board_temp1, piece, (move[0], move[1] - 1))

                if chess.check(board_temp, "white", kd2, lrd2, rrd2) or chess.check(board_copy, "white", kd2, lrd2, rrd2) or \
                        chess.check(board_temp1, "white", kd2, lrd2, rrd2):
                    skip_move = True

            if not skip_move:
                if piece[0][0] == 'K':
                    kd1 = 1
                if piece[0][0] == 'R' and piece[1][1] == 0:
                    lrd1 = 1
                if piece[0][0] == 'R' and piece[1][1] == 7:
                    rrd1 = 1

                v = min(v, maxValue(chess.applyMove(np.copy(board_copy), piece, move), depth - 1, alpha, beta, kd2, lrd2, rrd2, kd1, lrd1, rrd1))
                beta = min(beta, v)
                if alpha >= beta:
                    return v
    return v


# Returns the optimal move for the current player on the board
def minimax(kd1, lrd1, rrd1, kd2, lrd2, rrd2):
    board_copy = np.copy(board)
    depth = max_depth
    best_move = None
    best_move_piece = None
    alpha = -math.inf
    beta = math.inf

    kd1_copy, lrd1_copy, rrd1_copy, kd2_copy, lrd2_copy, rrd2_copy = kd1, lrd1, rrd1, kd2, lrd2, rrd2

    if ai_player == "black":
        minimum = -math.inf
        pieces = getPieces(board, "black")
        for piece in pieces:
            for move in chess.movesPossible(board_copy, piece[0], piece[1][0], piece[1][1], kd1, lrd1, rrd1):
                skip_move = False
                if piece[0][0] == 'K' and kd1 == 0 and (move[1] == 6 or move[1] == 2):
                    board_temp = np.copy(board_copy)
                    board_temp = chess.applyMove(board_temp, piece, move)
                    board_temp1 = np.copy(board_copy)
                    if move[1] == 2:
                        board_temp1 = chess.applyMove(board_temp1, piece, (move[0], move[1] + 1))
                    else:
                        board_temp1 = chess.applyMove(board_temp1, piece, (move[0], move[1] - 1))

                    if chess.check(board_temp, "black", kd2, lrd2, rrd2) or chess.check(board_copy, "black", kd2, lrd2, rrd2) or \
                            chess.check(board_temp1, "black", kd2, lrd2, rrd2):
                        skip_move = True

                if not skip_move:
                    if piece[0][0] == 'K':
                        kd1 = 1
                    if piece[0][0] == 'R' and piece[1][1] == 0:
                        lrd1 = 1
                    if piece[0][0] == 'R' and piece[1][1] == 7:
                        rrd1 = 1

                    check = minValue(chess.applyMove(np.copy(board_copy), piece, move), depth - 1, alpha, beta, kd2, lrd2, rrd2, kd1, lrd1, rrd1)
                    if check > minimum:
                        minimum = check
                        best_move = move
                        best_move_piece = piece
                    alpha = max(alpha, check)
                    if alpha >= beta:
                        return best_move_piece, best_move

                kd1, lrd1, rrd1, kd2, lrd2, rrd2 = kd1_copy, lrd1_copy, rrd1_copy, kd2_copy, lrd2_copy, rrd2_copy
    else:
        maximum = math.inf
        pieces = getPieces(board, "white")
        for piece in pieces:
            for move in chess.movesPossible(board_copy, piece[0], piece[1][0], piece[1][1], kd1, lrd1, rrd1):
                skip_move = False
                if piece[0][0] == 'K' and kd1 == 0 and (move[1] == 6 or move[1] == 2):
                    board_temp = np.copy(board_copy)
                    board_temp = chess.applyMove(board_temp, piece, move)
                    board_temp1 = np.copy(board_copy)
                    if move[1] == 2:
                        board_temp1 = chess.applyMove(board_temp1, piece, (move[0], move[1] + 1))
                    else:
                        board_temp1 = chess.applyMove(board_temp1, piece, (move[0], move[1] - 1))

                    if chess.check(board_temp, "white", kd2, lrd2, rrd2) or chess.check(board_copy, "white", kd2, lrd2, rrd2) or \
                            chess.check(board_temp1, "white", kd2, lrd2, rrd2):
                        skip_move = True

                if not skip_move:
                    if piece[0][0] == 'K':
                        kd1 = 1
                    if piece[0][0] == 'R' and piece[1][1] == 0:
                        lrd1 = 1
                    if piece[0][0] == 'R' and piece[1][1] == 7:
                        rrd1 = 1

                    check = maxValue(chess.applyMove(np.copy(board_copy), piece, move), depth - 1, alpha, beta, kd2, lrd2, rrd2, kd1, lrd1, rrd1)
                    if check < maximum:
                        maximum = check
                        best_move = move
                        best_move_piece = piece
                    beta = min(beta, check)
                    if alpha >= beta:
                        return best_move_piece, best_move

                kd1, lrd1, rrd1, kd2, lrd2, rrd2 = kd1_copy, lrd1_copy, rrd1_copy, kd2_copy, lrd2_copy, rrd2_copy
    return best_move_piece, best_move


# function to print the board
def printBoard():
    print("   A   B   C   D   E   F   G   H")
    for i in range(8):
        print(8 - i, end="  ")
        for j in range(8):
            print(board[i][j], end="  ")
        print(8 - i)
    print("   A   B   C   D   E   F   G   H")


# main
if __name__ == "__main__":
    ai_kd, ai_lrd, ai_rrd = 0, 0, 0
    p_kd, p_lrd, p_rrd = 0, 0, 0

    user_player = input("Choose a Player (black/white): ")
    while user_player != "black" and user_player != "white":
        print("\n--Please enter valid input--")
        user_player = input("Choose a Player (black/white): ")

    if user_player == "black":
        ai_player = "white"
    else:
        ai_player = "black"

    print("\nInitial Board:\n")
    printBoard()

    player_turn = "white"
    while True:
        if ai_player == player_turn:
            checkMate, _ = chess.checkMate(board, ai_player, ai_kd, ai_lrd, ai_rrd, p_kd, p_lrd, p_rrd)
            if checkMate:
                if chess.check(board, ai_player, p_kd, p_lrd, p_rrd):
                    print("\nGame Over: {0} wins.".format(user_player))
                    break
                print("\nGame Over: Draw (Stalemate).".format(user_player))
                break

            piece, move = minimax(ai_kd, ai_lrd, ai_rrd, p_kd, p_lrd, p_rrd)
            board = chess.applyMove(board, piece, move)

            if piece[0][0] == 'K':
                ai_kd = 1
            elif piece[0][0] == 'R' and piece[1][1] == 0:
                ai_lrd = 1
            elif piece[0][0] == 'R' and piece[1][1] == 7:
                ai_rrd = 1

            player_turn = user_player

            print("\nAI Move: {0} of position {1}{2} moved to {3}{4}\n".format(piece[0], 8 - piece[1][0],
                                                            chr(65 + piece[1][1]), 8 - move[0], chr(65 + move[1])))
            printBoard()

        elif user_player == player_turn:
            checkMate, valid_moves = chess.checkMate(board, user_player, p_kd, p_lrd, p_rrd, ai_kd, ai_lrd, ai_rrd)
            if checkMate:
                if chess.check(board, user_player, ai_kd, ai_lrd, ai_rrd):
                    print("\nGame Over: {0} wins.".format(ai_player))
                    break
                print("\nGame Over: Draw (Stalemate).".format(user_player))
                break

            player_no = "1"
            if user_player == "black":
                player_no = "2"

            check = chess.check(board, user_player, ai_kd, ai_lrd, ai_rrd)
            print("\n--Enter input--")
            if check:
                print("NOTE: You're in check!!!")
            player = input("Player: ")
            tmp_i = int(input("Current row: "))
            tmp_j = input("Current col: ")
            i = 8 - tmp_i
            j = ord(tmp_j) - 65
            row = int(input("Goal row: "))
            col = input("Goal col: ")
            row = 8 - row
            col = ord(col) - 65

            invalid_input = False
            if p_kd == 0 and p_lrd == 0 and p_rrd == 0 and (col == 6 or col == 2):
                board_temp1 = np.copy(board)
                if col == 2:
                    board_temp1 = chess.applyMove(board_temp1, (player, (i, j)), (row, col + 1))
                else:
                    board_temp1 = chess.applyMove(board_temp1, (player, (i, j)), (row, col - 1))
                if chess.check(board, user_player, ai_kd, ai_lrd, ai_rrd) or \
                        chess.check(board_temp1, user_player, ai_kd, ai_lrd, ai_rrd):
                    invalid_input = True

            while board[i][j] != player or player_no != player[1] or (row, col) not in \
                    chess.movesPossible(board, player, i, j, p_kd, p_lrd, p_rrd) or 8 < tmp_i < 1 or 7 < j < 0 \
                    or 7 < row < 0 or 7 < col < 0 or (player, (row, col)) not in valid_moves or invalid_input:
                print("\n--Please enter valid input--")
                if check:
                    print("NOTE: You're in check!!!")
                player = input("Player: ")
                tmp_i = int(input("Current row: "))
                tmp_j = input("Current col: ")
                i = 8 - tmp_i
                j = ord(tmp_j) - 65
                row = int(input("Goal row: "))
                col = input("Goal col: ")
                row = 8 - row
                col = ord(col) - 65

                invalid_input = False
                if p_kd == 0 and p_lrd == 0 and p_rrd == 0 and (col == 6 or col == 2):
                    board_temp1 = np.copy(board)
                    if col == 2:
                        board_temp1 = chess.applyMove(board_temp1, (player, (i, j)), (row, col + 1))
                    else:
                        board_temp1 = chess.applyMove(board_temp1, (player, (i, j)), (row, col - 1))
                    if chess.check(board, user_player, ai_kd, ai_lrd, ai_rrd) or \
                            chess.check(board_temp1, user_player, ai_kd, ai_lrd, ai_rrd):
                        invalid_input = True

            if player[0] == 'K':
                p_kd = 1
            elif player[0] == 'R' and j == 0:
                p_lrd = 1
            elif player[0] == 'R' and j == 7:
                p_rrd = 1

            board = chess.applyMove(board, (player, (i, j)), (row, col))
            print("\nUser Move: {0} of position {1}{2} moved to {3}{4}\n".format(player, tmp_i, tmp_j, 8 - row,
                                                                                 chr(65 + col)))
            printBoard()
            player_turn = ai_player
