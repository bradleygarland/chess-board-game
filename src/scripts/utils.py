import pygame
import random

# Constants
SQUARE_SIZE = 100

# Global Move History
move_history = []


# Get Mouse Square Position
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    return mouse_pos[1] // SQUARE_SIZE, mouse_pos[0] // SQUARE_SIZE


# Check for Legal Move
def is_valid_move(piece, start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    move_piece = piece[1]
    piece_color = piece[0]

    if move_piece == 'p':   # Pawn Logic
        if piece_color == 'w':  # White Pawn
            # Initial Two-Step Move
            if start_row == 6 and end_row == 4 and start_col == end_col and board[5][start_col] == '--' and board[4][start_col] == '--':
                return True
            # One-Step Move
            if end_row == start_row - 1 and start_col == end_col and board[end_row][end_col] == '--':
                return True
            # Capture Move
            if end_row == start_row - 1 and abs(end_col - start_col) == 1 and board[end_row][end_col] != '--' and board[end_row][end_col][0] == 'b':
                return True
        else:  # Black Pawn
            # Initial Two-Step Move
            if start_row == 1 and end_row == 3 and start_col == end_col and board[2][start_col] == '--' and board[3][start_col] == '--':
                return True
            # One-Step Move
            if end_row == start_row + 1 and end_col == start_col and board[end_row][end_col] == '--':
                return True
            # Capture Move
            if end_row == start_row + 1 and abs(end_col - start_col) == 1 and board[end_row][end_col] != '--' and board[end_row][end_col][0] == 'w':
                return True
            # Capture En Passant Move

    if move_piece == 'r':  # Rook Logic
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
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            if piece_color == 'w':  # White King
                if board[end_row][end_col][0] != 'w':
                    return True
            else:  # Black King
                if board[end_row][end_col][0] != 'b':
                    return True

    return False  # Return False if invalid move


# Find all valid moves
def get_all_valid_moves(turn, board):
    moves = []
    pieces = []
    for row in range(8):
        for col in range(8):
            if board[row][col][0] == turn:
                pieces.append([board[row][col], [row, col]])
    piece = random.choice(pieces)
    for r in range(8):
        for c in range(8):
            if is_valid_move(piece[0], (piece[1][0], piece[1][1]), (r, c), board):
                moves.append(((piece[1][0], piece[1][1]), (r, c)))
    return moves


# NPC Decision Process
def make_random_move(turn, board):
    valid_moves_available = False
    valid_moves = None
    while not valid_moves_available:
        valid_moves = get_all_valid_moves(turn, board)
        if valid_moves:
            valid_moves_available = True
    move = random.choice(valid_moves)
    start_pos, end_pos = move
    piece = board[start_pos[0]][start_pos[1]]
    board[end_pos[0]][end_pos[1]] = piece
    board[start_pos[0]][start_pos[1]] = '--'
    move_history.append((start_pos, end_pos))


# Check for Winner
def check_winner(board):
    white_king = False
    black_king = False
    for row in board:
        for piece in row:
            if piece == 'wk':
                white_king = True
            if piece == 'bk':
                black_king = True
    if not white_king:
        return "Black"
    if not black_king:
        return "White"
    return None
