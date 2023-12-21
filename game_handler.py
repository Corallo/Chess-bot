import chess

class ChessBoardHandler:
    def __init__(self, _color="white"):
        self.move_list = ()
        self.my_color = chess.WHITE if _color == "white" else chess.BLACK

    def make_move(self, move : chess.Move):
        self.move_list = tuple(list(self.move_list) + [move.uci()])

    def undo_move(self):
        self.move_list = self.move_list[:-1]

    def update_board(self, move_lists):
        self.move_list = tuple(move_lists)

    def get_board(self):
        board = chess.Board()
        for move in self.move_list:
            board.push_san(move)
        return board

    def get_legal_moves(self):
        board = self.get_board()
        return board.legal_moves

    def ismyturn(self):
        board = self.get_board()
        return board.turn == self.my_color

