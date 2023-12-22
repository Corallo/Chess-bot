import chess

class ChessBoardHandler:
    def __init__(self, _color="white"):
        self.move_str = ""
        self.my_color = chess.WHITE if _color == "white" else chess.BLACK

    def make_move(self, move : chess.Move):
        self.move_str += " " + move.uci()

    def undo_move(self):
        self.move_str = " ".join(self.move_str.split(" ")[:-1])

    def update_board(self, move_str):
        self.move_str = move_str

    def get_board(self):
        board = chess.Board()
        for move in self.move_str.split(" "):
            if move != "":
                board.push_san(move)
        return board

    def get_legal_moves(self):
        board = self.get_board()
        return board.legal_moves

    def ismyturn(self):
        board = self.get_board()
        return board.turn == self.my_color

    def check_draw(self):
        board = self.get_board()
        return board.is_variant_draw()
    def check_mate(self):
        board = self.get_board()
        return board.is_checkmate()

