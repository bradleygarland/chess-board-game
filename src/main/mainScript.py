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
        if piece_color == 'w':
            # Initial Two-Step Move
            if start_row == 6 and end_row == 4 and start_col == end_col and board[5][start_col] == '--' and board[4][start_col] == '--':
                return True
            # One-Step Move
            if end_row == start_row - 1 and start_col == end_col and board[end_row][end_col] == '--':
                return True
            # Capture Move
            if end_row == start_row - 1 and abs(end_col - start_col) == 1 and board[end_row][end_col] != '--' and board[end_row][end_col][0] == 'b':
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
