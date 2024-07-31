from board import create_initial_board
from utils import swap_board_colors


class GameState:
    def __init__(self):
        self.board = create_initial_board()
        self.selected_piece = None
        self.selected_pos = None
        self.turn = 'w'
        self.move_history = []
        self.swap_colors = False
        self.last_move = None
        self.castling_rights = {
            'white_king_side': True,
            'white_queen_side': True,
            'black_king_side': True,
            'black_queen_side': True
        }


    def reset_board(self):
        self.board = create_initial_board()
        self.selected_piece = None
        self.selected_pos = None
        self.turn = 'w'
        self.move_history = []
        self.last_move = None
        self.castling_rights['white_king_side'] = True
        self.castling_rights['white_queen_side'] = True
        self.castling_rights['black_king_side'] = True
        self.castling_rights['black_queen_side'] = True

    def swap_colors(self):
        self.swap_colors = not self.swap_colors
        swap_board_colors(self.board)

    def swap_mode(self):
        print("swaps modes")
