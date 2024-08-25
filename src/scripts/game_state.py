from board import create_initial_board


class GameState:
    def __init__(self):
        self.board = create_initial_board()
        self.selected_piece = None
        self.selected_pos = None
        self.top_color = 'b'
        self.bottom_color = 'w'
        self.turn = 'w'
        self.move_history = []
        self.swap_colors = False
        self.last_move = None
        self.king_pos = []
        self.castling_rights = {
            'white_king_side': True,
            'white_queen_side': True,
            'black_king_side': True,
            'black_queen_side': True
        }
        self.winner = None
        self.values = {
            'p': 1,
            'n': 3,
            'b': 3,
            'r': 5,
            'q': 9,
            'k': 10
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
        self.bottom_color = 'w'
        self.top_color = 'b'

    def swap_board_colors(self):
        temp_board = create_initial_board()
        r = 7
        for row in self.board:
            c = 7
            for col in row:
                temp_board[r][c] = col
                c -= 1
            r -= 1

        self.board = temp_board
        self.turn = 'w' if self.turn == 'b' else 'b'

        if self.bottom_color == 'w':
            self.bottom_color = 'b'
            self.top_color = 'w'
        else:
            self.bottom_color = 'w'
            self.top_color = 'b'

    def swap_mode(self):
        print("swaps modes")

    def check_winner(self):
        white_king = False
        black_king = False
        winner = None
        for row in self.board:
            for piece in row:
                if piece == 'wk':
                    white_king = True
                elif piece == 'bk':
                    black_king = True
        if black_king and not white_king:
            winner = 'Black'
        if white_king and not black_king:
            winner = 'White'

        if winner:
            print(winner + ' wins!')
            return True
        return False

    def swap_turn(self):
        self.turn = 'b' if self.turn == 'w' else 'w'

    def check_conditions(self):
        self.check_winner()


