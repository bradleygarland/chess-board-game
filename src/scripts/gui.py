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
PANEL_WIDTH = 300

# Menu Constants
MENU_HEIGHT = 300
MENU_MARGIN = 20

# Move History Constants
MOVE_SECTION_HEIGHT = HEIGHT - MENU_HEIGHT
MOVE_SECTION_WIDTH = PANEL_WIDTH
MOVE_SECTION_COLOR = (70, 70, 70)
PADDING = 10

# Button Constants
BUTTONS = ["Reset", "Flip", "Player/CPU"]
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_X = WIDTH + (abs(PANEL_WIDTH - BUTTON_WIDTH) // 2)
BUTTON_Y = (MENU_HEIGHT - 30 - BUTTON_HEIGHT * len(BUTTONS)) // 2
BUTTON_COLOR = WHITE
BUTTON_TEXT_COLOR = BLACK


# Set up Font
font = pygame.font.SysFont(None, FONT_SIZE)
border_font = pygame.font.SysFont(None, FONT_SIZE + BORDER_SIZE)
button_font = pygame.font.SysFont(None, 36)
history_font = pygame.font.SysFont(None, 24)


# Load Images
def load_images():
    pieces = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'../images/{piece}.png'), (SQUARE_SIZE * 0.8, SQUARE_SIZE * 0.8))
    return images


# Display Move History
def display_move_history(win, move_history):
    pygame.draw.rect(win, MOVE_SECTION_COLOR, (WIDTH, MENU_HEIGHT, MOVE_SECTION_WIDTH, MOVE_SECTION_HEIGHT))
    j = 0
    if len(move_history) <= 25:
        for i, (start, end) in enumerate(move_history):
            move_text = f"{i + 1}. ({start[0]}, {start[1]}) -> ({end[0]}, {end[1]})"
            text_surface = history_font.render(move_text, True, BLACK)
            win.blit(text_surface, (WIDTH + PADDING, (MENU_HEIGHT + PADDING) + i * 20))
    else:
        for i in range(len(move_history) - 25, len(move_history)):
            move_text = f"{i + 1}. ({move_history[i][0][0]}, {move_history[i][0][1]}) -> ({move_history[i][1][0]}, {move_history[i][1][1]})"
            text_surface = history_font.render(move_text, True, BLACK)
            win.blit(text_surface, (WIDTH + PADDING, (MENU_HEIGHT + PADDING) + j * 20))
            j += 1
