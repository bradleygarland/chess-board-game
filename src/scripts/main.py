# Import Libraries and Functions
import pygame
import sys
from utils import get_square_under_mouse, is_valid_move, check_winner, make_random_move
from gui import draw_move_history, draw_flip_button, draw_mode_button, draw_reset_button, draw_move_history_section
from board import draw_board, draw_pieces, create_initial_board

# Initialize pygame
successes, failures = pygame.init()
print(f"Pygame initialized with {successes} successes and {failures} failures.")

# Constants
WIDTH, HEIGHT = 800, 800
PANEL_WIDTH = 300
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 50
BORDER_SIZE = 5


# Menu Constants
MENU_HEIGHT = 300
MENU_MARGIN = 20

# Button Constants
BUTTONS = ["Reset", "Flip", "Player/CPU"]
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_X = WIDTH + (abs(PANEL_WIDTH - BUTTON_WIDTH) // 2)
BUTTON_Y = (MENU_HEIGHT - 30 - BUTTON_HEIGHT * len(BUTTONS)) // 2
BUTTON_COLOR = WHITE
BUTTON_TEXT_COLOR = BLACK

# Display
window = pygame.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
pygame.display.set_caption(f"Chess Board({WIDTH + PANEL_WIDTH},{HEIGHT})")

# Global Move History
move_history = []


# Main Loop
def main():
    board = create_initial_board()
    selected_piece = None
    selected_pos = None
    global move_history
    turn = 'w'
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = None, None
                if pygame.mouse.get_pos()[0] <= WIDTH:
                    row, col = get_square_under_mouse()
                if BUTTON_X <= pygame.mouse.get_pos()[0] <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= pygame.mouse.get_pos()[1] <= BUTTON_Y + BUTTON_HEIGHT:
                    board = create_initial_board()
                    selected_piece = None
                    selected_pos = None
                    turn = 'w'
                    move_history = []
                elif turn == 'w':
                    if selected_piece:
                        if selected_piece[0] == turn and is_valid_move(selected_piece, selected_pos, (row, col), board):
                            board[row][col] = selected_piece
                            board[selected_pos[0]][selected_pos[1]] = '--'
                            move_history.append((selected_pos, (row, col)))
                            turn = 'b' if turn == 'w' else 'w'  # Switch turn
                            winner = check_winner(board)
                            if winner:
                                print(f"{winner} wins!")
                                run = False
                        else:  # Return Piece if Invalid Move
                            board[selected_pos[0]][selected_pos[1]] = selected_piece
                        selected_piece = None
                        selected_pos = None
                    else:
                        if row or col:
                            if board[row][col] != '--':
                                selected_piece = board[row][col]
                                selected_pos = (row, col)
                                board[row][col] = '--'
        if turn == 'b':
            make_random_move(turn, board)
            turn = 'w'
            winner = check_winner(board)
            if winner:
                print(f"{winner} wins!")
                run = False

        draw_board(window)
        draw_pieces(window, board)
        draw_reset_button(window)
        draw_flip_button(window)
        draw_mode_button(window)
        draw_move_history_section(window)
        draw_move_history(window, move_history)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
