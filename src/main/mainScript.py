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


# Create Inital Board
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


# Main Loop
def main():
    board = create_initial_board()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_board(window)
        draw_pieces(window, board)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
