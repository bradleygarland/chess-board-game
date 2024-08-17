import pygame
import random
import copy

# Constants
SQUARE_SIZE = 100


# Get Mouse Square Position
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    return mouse_pos[1] // SQUARE_SIZE, mouse_pos[0] // SQUARE_SIZE


# Check for Legal Move
def is_valid_move(piece, move, board, last_move, castling_rights, bottom_color, top_color):
    start_pos = move[0]
    end_pos = move[1]

    start_row, start_col = start_pos
    end_row, end_col = end_pos
    move_piece = piece[1]
    piece_color = piece[0]

    if move_piece == 'p':   # Pawn Logic
        if piece_color == bottom_color:  # Bottom Color Pawn
            # Initial Two-Step Move
            if start_row == 6 and end_row == 4 and start_col == end_col and board[5][start_col] == '--' and board[4][start_col] == '--':
                return True
            # One-Step Move
            if end_row == start_row - 1 and start_col == end_col and board[end_row][end_col] == '--':
                return True
            # Capture Move
            if end_row == start_row - 1 and abs(end_col - start_col) == 1:
                # Regular Capture
                if board[end_row][end_col] != '--' and board[end_row][end_col][0] == top_color:
                    return True
                # En Passant Capture
                if last_move and last_move[0][0] == 1 and last_move[1][0] == 3 and last_move[1][1] == end_col and board[end_row + 1][end_col] == top_color + 'p':
                    return True

        else:  # Top Color Pawn
            # Initial Two-Step Move
            if start_row == 1 and end_row == 3 and start_col == end_col and board[2][start_col] == '--' and board[3][start_col] == '--':
                return True
            # One-Step Move
            if end_row == start_row + 1 and end_col == start_col and board[end_row][end_col] == '--':
                return True
            # Capture Move
            if end_row == start_row + 1 and abs(end_col - start_col) == 1:
                # Regular Capture
                if board[end_row][end_col] != '--' and board[end_row][end_col][0] == bottom_color:
                    return True
                # En Passant Capture
                if last_move and last_move[0][0] == 6 and last_move[1][0] == 4 and last_move[1][1] == end_col and board[end_row - 1][end_col] == bottom_color + 'p':
                    return True

    if move_piece == 'r':  # Rook Logic
        # Prevent Self Capture
        if start_row == end_row and start_col == end_col:
            return False
        # Horizontal or Vertical Move
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:  # Horizontal Move
                step = 1 if start_col < end_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '--':
                        return False
            if start_col == end_col:  # Vertical Move
                step = 1 if start_row < end_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '--':
                        return False
            if piece_color == 'w':  # White Rook
                if board[end_row][end_col][0] != 'w':
                    return True
            else:  # Black Rook
                if board[end_row][end_col][0] != 'b':
                    return True

    if move_piece == 'n':  # Knight Logic
        if piece_color == 'w':  # White Knight
            if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)] and board[end_row][end_col][0] != 'w':
                return True
        else:  # Black Knight
            if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)] and board[end_row][end_col][0] != 'b':
                return True

    if move_piece == 'b':  # Bishop Logic
        # Prevent Self Capture
        if start_row == end_row and start_col == end_col:
            return False
        if abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal Movement
            step_row = 1 if start_row < end_row else -1
            step_col = 1 if start_col < end_col else -1
            for step in range(1, abs(start_row - end_row)):
                if board[start_row + step * step_row][start_col + step * step_col] != '--':
                    return False
            if piece_color == 'w':  # White Bishop
                if board[end_row][end_col][0] != 'w':
                    return True
            else:  # Black Bishop
                if board[end_row][end_col][0] != 'b':
                    return True

    if move_piece == 'q':  # Queen Logic
        # Prevent Self Capture
        if start_row == end_row and start_col == end_col:
            return False
        # Horizontal, Vertical, or Diagonal Movement
        if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col):
            # Horizontal Movement
            if start_row == end_row:
                step = 1 if start_col < end_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '--':
                        return False
            # Vertical Movement
            if start_col == end_col:
                step = 1 if start_row < end_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '--':
                        return False
            # Diagonal Movement
            if abs(start_row - end_row) == abs(start_col - end_col):
                step_row = 1 if start_row < end_row else -1
                step_col = 1 if start_col < end_col else -1
                for step in range(1, abs(start_row - end_row)):
                    if board[start_row + step * step_row][start_col + step * step_col] != '--':
                        return False
            if piece_color == 'w':  # White Queen
                if board[end_row][end_col][0] != 'w':
                    return True
            else:  # Black Queen
                if board[end_row][end_col][0] != 'b':
                    return True

    if move_piece == 'k':  # King Logic
        return valid_king_move(board, start_pos, end_pos, piece, castling_rights)

    return False  # Return False if invalid move


def valid_king_move(board, start_pos, end_pos, piece, castling_rights):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    # Normal King Move
    if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
        if not (start_row != end_row and start_col != end_col):
            if piece[0] == 'w':  # White King
                if board[end_row][end_col][0] != 'w':
                    return True
            else:  # Black King
                if board[end_row][end_col][0] != 'b':
                    return True

    # Castling King Move
    if piece[0] == 'w':
        # King-side
        if start_row == end_row and end_col >= start_col + 2 and board[7][7] == 'wr' and castling_rights['white_king_side']:
            for col in range(5, 6):
                if board[start_row][col] != '--':
                    return False
                else:
                    return True
        # White Queen-side
        if start_row == end_row and end_col <= start_col - 2 and board[7][0] == 'wr' and castling_rights['white_queen_side']:
            for col in range(1, 3):
                if board[start_row][col] != '--':
                    return False
                else:
                    return True
    else:
        # Black King-side
        if start_row == end_row and end_col >= start_col + 2 and board[7][7] == 'br' and castling_rights['black_king_side']:
            for col in range(5, 6):
                if board[start_row][col] != '--':
                    return False
                else:
                    return True
        # Black Queen-side
        if start_row == end_row and end_col <= start_col - 2 and board[7][0] == 'br' and castling_rights['black_queen_side']:
            for col in range(1, 3):
                if board[start_row][col] != '--':
                    return False
                else:
                    return True


def get_all_moves(turn, board, last_move, castling_rights, bottom_color, top_color):
    pieces = []
    moves = []
    for row in range(8):
        for col in range(8):
            if board[row][col] != '--' and board[row][col][0] == turn:
                pieces.append([board[row][col], (row, col)]) # ['piece', [row, col]]
    for piece in pieces:
        for row in range(8):
            for col in range(8):
                move = [piece[1], (row, col)] # [(start_pos), (end_pos)]
                if is_valid_move(piece[0], move, board, last_move, castling_rights, bottom_color, top_color):
                    moves.append(move)
    return moves



def simulate_move(piece, move, board, last_move, simulate_type, turn, castling_rights, bottom_color, top_color, king_pos):
    temp_board = copy.deepcopy(board)
    temp_board[move[1][0]][move[1][1]] = piece
    temp_board[move[0][0]][move[0][1]] = '--'
    opposing_turn = 'w' if turn == 'b' else 'b'
    if simulate_type == 'check':
        moves = get_all_moves(opposing_turn, temp_board, last_move, castling_rights, bottom_color, top_color)
        for pos in king_pos:
            if temp_board[pos[0]][pos[1]][0] == turn:
                for potential_move in moves:
                    if pos == potential_move[1]:
                        return True
        return False


def make_move(start_pos, end_pos, selected_piece, board, castling_rights):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = selected_piece
    castling = False

    # En Passant Handling
    if piece[1] == 'p' and abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1 and board[end_row][end_col] == '--':
        if piece[0] == 'w':
            board[end_row + 1][end_col] = '--'
        else:
            board[end_row - 1][end_col] = '--'

    # Castle Handling
    if piece[1] == 'k' and abs(start_col - end_col) >= 2 and start_row == end_row:
        castling = True
        # White Castle
        if piece[0] == 'w':
            # Queen Side
            if start_col - end_col < 0:
                for col in range(start_col, 8):
                    board[start_row][col] = '--'
                board[start_row][start_col + 2] = 'wk'
                board[start_row][start_col + 1] = 'wr'

            # King Side
            else:
                for col in range(0, start_col):
                    board[start_row][col] = '--'
                board[start_row][start_col - 2] = 'wk'
                board[start_row][start_col - 1] = 'wr'

        # Black Castle
        else:
            # Queen Side
            if start_col - end_col < 0:
                for col in range(start_col, 7):
                    board[start_row][col] = '--'
                board[start_row][start_col + 2] = 'bk'
                board[start_row][start_col + 1] = 'br'

            # King Side
            else:
                for col in range(start_col, 0, -1):
                    board[start_row][col] = '--'
                board[start_row][start_col - 2] = 'bk'
                board[start_row][start_col - 1] = 'br'

    if not castling:
        board[end_row][end_col] = piece
    board[start_row][start_col] = '--'
    last_move = (start_pos, end_pos)

    update_castling_rights(castling_rights, (start_pos, end_pos), piece)

    return board, last_move, (start_pos, end_pos)


# NPC Decision Process
def make_random_move(turn, board, last_move, castling_rights, bottom_color, top_color):
    valid_moves_available = False
    valid_moves = None
    while not valid_moves_available:
        valid_moves = get_all_moves(turn, board, last_move, castling_rights, bottom_color, top_color)
        if valid_moves:
            valid_moves_available = True
    move = random.choice(valid_moves)
    start_pos, end_pos = move
    piece = board[start_pos[0]][start_pos[1]]
    board[end_pos[0]][end_pos[1]] = piece
    board[start_pos[0]][start_pos[1]] = '--'
    last_move = start_pos, end_pos

    return board, last_move, move


# Update Castling Rights
def update_castling_rights(castling_rights, move, selected_piece):
    start_pos, end_pos = move
    piece = selected_piece

    if piece == 'wk':
        castling_rights['white_king_side'] = False
        castling_rights['white_queen_side'] = False
    elif piece == 'wr':
        if start_pos == (7, 0):
            castling_rights['white_queen_side'] = False
        elif start_pos == (7, 7):
            castling_rights['white_king_side'] = False
    elif piece == 'bk':
        castling_rights['black_king_side'] = False
        castling_rights['black_queen_side'] = False
    elif piece == 'br':
        if start_pos == (0, 0):
            castling_rights['black_queen_side'] = False
        elif start_pos == (0, 7):
            castling_rights['black_king_side'] = False
