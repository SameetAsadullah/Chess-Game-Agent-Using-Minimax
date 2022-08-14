import copy
import numpy as np


# function to find all possible moves of king
def kingMoves(n_board, piece, row, col):
    moves_array = []
    if col != 0 and (n_board[row][col - 1] == "--" or n_board[row][col - 1][1] != piece[1]):
        moves_array.append((row, col - 1))
    if col != 7 and (n_board[row][col + 1] == "--" or n_board[row][col + 1][1] != piece[1]):
        moves_array.append((row, col + 1))
    if row != 0 and (n_board[row - 1][col] == "--" or n_board[row - 1][col][1] != piece[1]):
        moves_array.append((row - 1, col))
    if row != 7 and (n_board[row + 1][col] == "--" or n_board[row + 1][col][1] != piece[1]):
        moves_array.append((row + 1, col))
    if col != 0 and row != 0 and (n_board[row - 1][col - 1] == "--" or n_board[row - 1][col - 1][1] != piece[1]):
        moves_array.append((row - 1, col - 1))
    if col != 0 and row != 7 and (n_board[row + 1][col - 1] == "--" or n_board[row + 1][col - 1][1] != piece[1]):
        moves_array.append((row + 1, col - 1))
    if col != 7 and row != 0 and (n_board[row - 1][col + 1] == "--" or n_board[row - 1][col + 1][1] != piece[1]):
        moves_array.append((row - 1, col + 1))
    if col != 7 and row != 7 and (n_board[row + 1][col + 1] == "--" or n_board[row + 1][col + 1][1] != piece[1]):
        moves_array.append((row + 1, col + 1))

    return moves_array


# function to find all possible moves of white pawn
def whitePawnMoves(n_board, piece, row, col):
    moves_array = []
    if row != 0:
        if col != 0 and n_board[row - 1][col - 1] != "--" and n_board[row - 1][col - 1][1] != piece[1]:
            moves_array.append((row - 1, col - 1))
        if col != 7 and n_board[row - 1][col + 1] != "--" and n_board[row - 1][col + 1][1] != piece[1]:
            moves_array.append((row - 1, col + 1))

    if row == 6:
        if n_board[row - 1][col] == "--":
            moves_array.append((row - 1, col))
        else:
            return moves_array

        if n_board[row - 2][col] == "--":
            moves_array.append((row - 2, col))
    else:
        if n_board[row - 1][col] == "--":
            moves_array.append((row - 1, col))

    return moves_array


# function to find all possible moves of black pawn
def blackPawnMoves(n_board, piece, row, col):
    moves_array = []
    if row != 7:
        if col != 0 and n_board[row + 1][col - 1] != "--" and n_board[row + 1][col - 1][1] != piece[1]:
            moves_array.append((row + 1, col - 1))
        if col != 7 and n_board[row + 1][col + 1] != "--" and n_board[row + 1][col + 1][1] != piece[1]:
            moves_array.append((row + 1, col + 1))

    if row == 1:
        if n_board[row + 1][col] == "--":
            moves_array.append((row + 1, col))
        else:
            return moves_array

        if n_board[row + 2][col] == "--":
            moves_array.append((row + 2, col))
    else:
        if n_board[row + 1][col] == "--":
            moves_array.append((row + 1, col))

    return moves_array


# function to find all possible straight moves
def straightMoves(n_board, piece, row, col):
    moves_array = []
    if col != 0:
        for i in range(col - 1, -1, -1):
            if n_board[row][i] == "--":
                moves_array.append((row, i))
            elif n_board[row][i][1] != piece[1]:
                moves_array.append((row, i))
                break
            else:
                break
    if col != 7:
        for i in range(col + 1, 8, 1):
            if n_board[row][i] == "--":
                moves_array.append((row, i))
            elif n_board[row][i][1] != piece[1]:
                moves_array.append((row, i))
                break
            else:
                break
    if row != 0:
        for i in range(row - 1, -1, -1):
            if n_board[i][col] == "--":
                moves_array.append((i, col))
            elif n_board[i][col][1] != piece[1]:
                moves_array.append((i, col))
                break
            else:
                break
    if row != 7:
        for i in range(row + 1, 8, 1):
            if n_board[i][col] == "--":
                moves_array.append((i, col))
            elif n_board[i][col][1] != piece[1]:
                moves_array.append((i, col))
                break
            else:
                break

    return moves_array


# function to find all possible diagonal moves
def diagonalMoves(n_board, piece, row, col):
    moves_array = []
    if col != 0 and row != 0:
        r1 = row - 1
        c1 = col - 1
        for i in range(0, 8):
            if n_board[r1][c1] == "--":
                moves_array.append((r1, c1))
            elif n_board[r1][c1][1] != piece[1]:
                moves_array.append((r1, c1))
                break
            else:
                break
            r1 -= 1
            c1 -= 1

            if r1 < 0 or c1 < 0:
                break

    if col != 7 and row != 0:
        r1 = row - 1
        c1 = col + 1
        for i in range(0, 8):
            if n_board[r1][c1] == "--":
                moves_array.append((r1, c1))
            elif n_board[r1][c1][1] != piece[1]:
                moves_array.append((r1, c1))
                break
            else:
                break
            r1 -= 1
            c1 += 1

            if r1 < 0 or c1 > 7:
                break

    if col != 0 and row != 7:
        r1 = row + 1
        c1 = col - 1
        for i in range(0, 8):
            if n_board[r1][c1] == "--":
                moves_array.append((r1, c1))
            elif n_board[r1][c1][1] != piece[1]:
                moves_array.append((r1, c1))
                break
            else:
                break
            r1 += 1
            c1 -= 1

            if r1 > 7 or c1 < 0:
                break

    if col != 7 and row != 7:
        r1 = row + 1
        c1 = col + 1

        for i in range(0, 8):
            if n_board[r1][c1] == "--":
                moves_array.append((r1, c1))
            elif n_board[r1][c1][1] != piece[1]:
                moves_array.append((r1, c1))
                break
            else:
                break
            r1 += 1
            c1 += 1

            if r1 > 7 or c1 > 7:
                break

    return moves_array


# function to find all possible moves of knight
def knightMoves(n_board, piece, row, col):
    moves_array = []
    if col != 0:
        if row != 0 and row != 1 and (n_board[row - 2][col - 1] == "--" or n_board[row - 2][col - 1][1] != piece[1]):
            moves_array.append((row - 2, col - 1))
        if row != 6 and row != 7 and (n_board[row + 2][col - 1] == "--" or n_board[row + 2][col - 1][1] != piece[1]):
            moves_array.append((row + 2, col - 1))

        if col != 1:
            if row != 0 and (n_board[row - 1][col - 2] == "--" or n_board[row - 1][col - 2][1] != piece[1]):
                moves_array.append((row - 1, col - 2))
            if row != 7 and (n_board[row + 1][col - 2] == "--" or n_board[row + 1][col - 2][1] != piece[1]):
                moves_array.append((row + 1, col - 2))

    if col != 7:
        if row != 0 and row != 1 and (n_board[row - 2][col + 1] == "--" or n_board[row - 2][col + 1][1] != piece[1]):
            moves_array.append((row - 2, col + 1))
        if row != 6 and row != 7 and (n_board[row + 2][col + 1] == "--" or n_board[row + 2][col + 1][1] != piece[1]):
            moves_array.append((row + 2, col + 1))

        if col != 6:
            if row != 0 and (n_board[row - 1][col + 2] == "--" or n_board[row - 1][col + 2][1] != piece[1]):
                moves_array.append((row - 1, col + 2))
            if row != 7 and (n_board[row + 1][col + 2] == "--" or n_board[row + 1][col + 2][1] != piece[1]):
                moves_array.append((row + 1, col + 2))

    return moves_array


# function to find all possible moves of castling
def castlingMoves(n_board, piece, row, col, lrd1, rrd1):
    moves_array = []

    if rrd1 == 0:
        if n_board[row][col + 1] == "--" and n_board[row][col + 2] == "--":
            moves_array.append((row, col + 2))

    if lrd1 == 0:
        if n_board[row][col - 1] == "--" and n_board[row][col - 2] == "--" and n_board[row][col - 3] == "--":
            moves_array.append((row, col - 2))

    return moves_array


# function to find all possible moves
def movesPossible(n_board, piece, row, col, kd1, lrd1, rrd1):
    moves_array = []

    if piece[0] == 'K':  # king movements
        moves_array.extend(kingMoves(n_board, piece, row, col))

        if kd1 == 0:
            moves_array.extend(castlingMoves(n_board, piece, row, col, lrd1, rrd1))

    if piece == 'P1':  # pawn movements for white
        moves_array.extend(whitePawnMoves(n_board, piece, row, col))

    if piece == 'P2':  # pawn movements for black
        moves_array.extend(blackPawnMoves(n_board, piece, row, col))

    if piece[0] == 'N':  # knight movements
        moves_array.extend(knightMoves(n_board, piece, row, col))

    if piece[0] == 'R' or piece[0] == 'Q':  # rook movements and queen straight line movements
        moves_array.extend(straightMoves(n_board, piece, row, col))

    if piece[0] == 'B' or piece[0] == 'Q':  # bishop movements and queen diagonal movements
        moves_array.extend(diagonalMoves(n_board, piece, row, col))

    return moves_array


# function to apply move
def applyMove(board_copy, piece, move):
    piece_name = piece[0]
    piece_loc = piece[1]
    board_copy[piece_loc[0]][piece_loc[1]] = "--"

    if piece_name == "P1" and move[0] == 0:
        board_copy[move[0]][move[1]] = "Q1"
    elif piece_name == "P2" and move[0] == 7:
        board_copy[move[0]][move[1]] = "Q2"
    elif piece_name[0] == "K" and move[1] - piece_loc[1] == 2:
        if piece_name == "K1":
            board_copy[move[0]][move[1] - 1] = "R1"
            board_copy[move[0]][move[1] + 1] = "--"
        else:
            board_copy[move[0]][move[1] - 1] = "R2"
            board_copy[move[0]][move[1] + 1] = "--"

        board_copy[move[0]][move[1]] = piece_name

    elif piece_name[0] == "K" and move[1] - piece_loc[1] == -2:
        if piece_name == "K1":
            board_copy[move[0]][move[1] + 1] = "R1"
            board_copy[move[0]][move[1] - 2] = "--"
        else:
            board_copy[move[0]][move[1] + 1] = "R2"
            board_copy[move[0]][move[1] - 2] = "--"

        board_copy[move[0]][move[1]] = piece_name

    else:
        board_copy[move[0]][move[1]] = piece_name

    return board_copy


# function to find check
def check(n_board, player, kd, lrd, rrd):
    index_inverse = "1"
    index = "2"
    if player == "black":
        index = "1"
        index_inverse = "2"

    king_loc = np.asarray(np.where(n_board == "K" + index_inverse)).T.tolist()
    king_loc = (king_loc[0][0], king_loc[0][1])

    for row in range(n_board.shape[0]):
        for col in range(n_board.shape[1]):
            if n_board[row][col][1] == index:
                moves = movesPossible(n_board, n_board[row][col], row, col, kd, lrd, rrd)
                for move in moves:
                    if move == king_loc:
                        return True
    return False


# function to find checkmate
def checkMate(board_copy, player, kd1, lrd1, rrd1, kd2, lrd2, rrd2):
    index = "1"
    if player == "black":
        index = "2"

    valid_moves = []

    for row in range(board_copy.shape[0]):
        for col in range(board_copy.shape[1]):
            if board_copy[row][col][1] == index:
                moves = movesPossible(board_copy, board_copy[row][col], row, col, kd1, lrd1, rrd1)
                for move in moves:
                    board_temp = np.copy(board_copy)
                    board_temp = applyMove(board_temp, (board_copy[row][col], (row, col)), move)
                    if not check(board_temp, player, kd2, lrd2, rrd2):
                        valid_moves.append((board_copy[row][col], move))

    if len(valid_moves) == 0:
        return True, valid_moves
    return False, valid_moves
