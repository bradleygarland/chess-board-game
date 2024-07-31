# Import Libraries and Functions
import pygame
import sys
from utils import get_square_under_mouse, is_valid_move, check_winner, make_random_move, make_move
from gui import display_move_history
from board import draw_board, draw_pieces
from buttons import Button, handle_button_clicks
from game_state import GameState

# Initialize pygame
successes, failures = pygame.init()
print(f"Pygame initialized with {successes} successes and {failures} failures.")

# Constants
WIDTH, HEIGHT = 800, 800
PANEL_WIDTH = 300
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Display
window = pygame.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
pygame.display.set_caption(f"Chess Board({WIDTH + PANEL_WIDTH},{HEIGHT})")

# Initialize Game State
game_state = GameState()


# Main Loop
def main():
    run = True

    # Define Buttons/Actions
    buttons = [
        Button((WIDTH + 50, 40, 200, 60), 'Reset', game_state.reset_board),
        Button((WIDTH + 50, 120, 200, 60), 'Swap Colors', game_state.swap_colors),
        Button((WIDTH + 50, 200, 200, 60), 'Swap Mode', game_state.swap_mode)
    ]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            else:
                handle_button_clicks(buttons, event)

            if game_state.turn == 'w' and event.type == pygame.MOUSEBUTTONDOWN:
                row, col = None, None
                if game_state.selected_piece:
                    if pygame.mouse.get_pos()[0] <= WIDTH:
                        row, col = get_square_under_mouse()
                    if game_state.selected_piece[0] == game_state.turn and is_valid_move(game_state.selected_piece, game_state.selected_pos, (row, col), game_state.board, game_state.last_move, game_state.castling_rights):
                        game_state.board, game_state.last_move, move = make_move(game_state.selected_pos, (row, col), game_state.selected_piece,  game_state.board, game_state.castling_rights)
                        game_state.move_history.append(move)
                        game_state.selected_piece = None
                        game_state.selected_pos = None
                        game_state.turn = 'b' if game_state.turn == 'w' else 'w'
                        winner = check_winner(game_state.board)
                        if winner:
                            print(f'{winner} wins!')
                            run = False
                    else:
                        game_state.board[game_state.selected_pos[0]][game_state.selected_pos[1]] = game_state.selected_piece
                        game_state.selected_piece = None
                        game_state.selected_pos = None
                else:
                    if pygame.mouse.get_pos()[0] <= WIDTH:
                        row, col = get_square_under_mouse()
                    if row or col:
                        if game_state.board[row][col] != '--' and game_state.board[row][col][0] == game_state.turn:
                            game_state.selected_piece = game_state.board[row][col]
                            game_state.selected_pos = (row, col)
                            game_state.board[row][col] = '--'
        if game_state.turn == 'b':
            game_state.board, game_state.last_move, move = make_random_move(game_state.turn, game_state.board, game_state.last_move, game_state.castling_rights)
            game_state.turn = 'w'
            winner = check_winner(game_state.board)
            if winner:
                print(f'{winner} wins!')
                run = False
        draw_board(window)
        draw_pieces(window, game_state.board)
        display_move_history(window, game_state.move_history)
        for button in buttons:
            button.draw(window)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
