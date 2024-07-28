# Import Libraries
# import random
import pygame
import sys

# Initialize Pygame
successes, failures = pygame.init()
print(f"Pygame initialized with {successes} successes and {failures} failures.")

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 50
# Green/Cream Color Scheme
GREEN = (118, 150, 86)
CREAM = (238, 238, 210)

# Set up Font
font = pygame.font.SysFont(None, FONT_SIZE)

# Display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Chess Board({WIDTH},{HEIGHT})")


# Draw Board Function
def draw_board(win):
    colors = [GREEN, CREAM]

    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(win, color,
                             ((col * SQUARE_SIZE), (row * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))


# Draw Pieces Function
def draw_pieces(win, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':
                piece_color = WHITE if piece[0] == 'w' else BLACK
                text_surface = font.render(piece[1], True, piece_color)
                text_rect = text_surface.get_rect(
                    center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                win.blit(text_surface, text_rect)


# Create Initial Board
def create_initial_board():
    board = [
        ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
        ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]
    return board


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


# Main Loop
def main():
    board = create_initial_board()
    selected_piece = None
    selected_pos = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square_under_mouse()
                if selected_piece:
                    if is_valid_move(selected_piece, selected_pos, (row, col), board):
                        board[row][col] = selected_piece
                        board[selected_pos[0]][selected_pos[1]] = '--'
                    selected_piece = None
                else:
                    if board[row][col] != '--':
                        selected_piece = board[row][col]
                        selected_pos = (row, col)
                        board[row][col] = '--'

        draw_board(window)
        draw_pieces(window, board)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
