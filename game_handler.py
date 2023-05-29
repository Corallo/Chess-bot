import chess


class ChessGameHandler:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        self.board.push_san(move)
    
    def get_board(self):
        return self.board
    