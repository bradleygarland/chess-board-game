
# Import Libraries
import random
import pygame
import sys

# Initialize Pygame
successes, failures = pygame.init()
print(f"Pygame initialized with {successes} successes and {failures} failures.")

# Constants
WIDTH, HEIGHT = 1000, 1000
BORDER = 100
SQUARE_SIZE = (WIDTH - (2 * BORDER)) // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)

# Display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Chess Board({WIDTH},{HEIGHT})")

# Main Draw Function
def draw_board(window):
    colors = [WHITE, BLACK]
    pygame.draw.rect(window, GREY, (0, 0, WIDTH, HEIGHT))
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(window, color, (BORDER + (col * SQUARE_SIZE), BORDER + (row * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))

# Main Loop
def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_board(window)
        pygame.display.update()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

