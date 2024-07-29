# Import Libraries
import pygame

# Initialize Pygame Font
pygame.font.init()

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 50
BORDER_SIZE = 5

# Green/Cream Color Scheme
GREEN = (118, 150, 86)
CREAM = (238, 238, 210)

# Set up Font
font = pygame.font.SysFont(None, FONT_SIZE)
border_font = pygame.font.SysFont(None, FONT_SIZE + BORDER_SIZE)
button_font = pygame.font.SysFont(None, 36)
history_font = pygame.font.SysFont(None, 24)


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
                piece_letter = piece[1]

                # Draw the Border
                text_surface_border = border_font.render(piece_letter, True, BLACK)
                text_rect_border = text_surface_border.get_rect(
                    center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                win.blit(text_surface_border, text_rect_border)

                # Draw the Piece Letter
                text_surface = font.render(piece_letter, True, piece_color)
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
