# Import Libraries
import random
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
BORDER_SIZE = 5

# Green/Cream Color Scheme
GREEN = (118, 150, 86)
CREAM = (238, 238, 210)

PANEL_WIDTH = 300

# Menu Constants
MENU_HEIGHT = 300
MENU_MARGIN = 20

# Move History Constants
MOVE_SECTION_HEIGHT = HEIGHT - MENU_HEIGHT
MOVE_SECTION_WIDTH = PANEL_WIDTH
MOVE_SECTION_COLOR = (70, 70, 70)


# Global Move History
move_history = []

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

# Display
window = pygame.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
pygame.display.set_caption(f"Chess Board({WIDTH + PANEL_WIDTH},{HEIGHT})")


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


# Get Mouse Square Position
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] <= WIDTH:
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
def draw_move_history(win):
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
        draw_move_history(window)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()