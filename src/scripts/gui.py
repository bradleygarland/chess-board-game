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


# Draw Reset Button
def draw_reset_button(win):
    button_index = BUTTONS.index("Reset")
    pygame.draw.rect(win, BUTTON_COLOR, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    text_surface = button_font.render(BUTTONS[button_index], True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    win.blit(text_surface, text_rect)


# Draw Flip Button
def draw_flip_button(win):
    button_index = BUTTONS.index("Flip")
    pygame.draw.rect(win, BUTTON_COLOR, (BUTTON_X, BUTTON_Y + BUTTON_HEIGHT + 15, BUTTON_WIDTH, BUTTON_HEIGHT))
    text_surface = button_font.render(BUTTONS[button_index], True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, (BUTTON_Y + BUTTON_HEIGHT + 15) + BUTTON_HEIGHT // 2))
    win.blit(text_surface, text_rect)


# Draw Mode Button
def draw_mode_button(win):
    button_index = BUTTONS.index("Player/CPU")
    pygame.draw.rect(win, BUTTON_COLOR, (BUTTON_X, BUTTON_Y + BUTTON_HEIGHT * 2 + 30, BUTTON_WIDTH, BUTTON_HEIGHT))
    text_surface = button_font.render(BUTTONS[button_index], True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + (BUTTON_HEIGHT + 15) * 2 + BUTTON_HEIGHT // 2))
    win.blit(text_surface, text_rect)


# Draw Move History Section
def draw_move_history_section(win):
    pygame.draw.rect(win, MOVE_SECTION_COLOR, (WIDTH, MENU_HEIGHT, MOVE_SECTION_WIDTH, MOVE_SECTION_HEIGHT))


# Draw Move History
def draw_move_history(win, move_history):
    start_y = MENU_HEIGHT
    padding = 10
    j = 0
    if len(move_history) <= 25:
        for i, (start, end) in enumerate(move_history):
            move_text = f"{i + 1}. ({start[0]}, {start[1]}) -> ({end[0]}, {end[1]})"
            text_surface = history_font.render(move_text, True, BLACK)
            win.blit(text_surface, (WIDTH + padding, start_y + i * 20))
    else:
        for i in range(len(move_history) - 25, len(move_history)):
            move_text = f"{i + 1}. ({move_history[i][0][0]}, {move_history[i][0][1]}) -> ({move_history[i][1][0]}, {move_history[i][1][1]})"
            text_surface = history_font.render(move_text, True, BLACK)
            win.blit(text_surface, (WIDTH + padding, start_y + j * 20))
            j += 1
