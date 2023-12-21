import chess
from functools import lru_cache
from game_handler import ChessBoardHandler

class ChessEvaluator:

    def __init__(self):
        self.bh = ChessBoardHandler()

    @lru_cache(maxsize=1000000)
    def evaluate_board(self, move_list: tuple) -> int:
        self.bh.update_board(move_list)
        board = self.bh.get_board()
        #return if checkmate
        if board.is_checkmate():
            return 1000 if board.turn else -1000
        #return if draw
        if board.is_variant_draw():
            return 0
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                score += piece_values[piece.piece_type] * (1 if piece.color else -1)
        return score


class chessEngine:
    def __init__(self):
        self.evaluator = ChessEvaluator()
        self.bh = ChessBoardHandler()
    def search_best_move(self, move_list, depth=3):
        self.bh.update_board(move_list)
        best_move = None
        best_score = -1000
        #_minimax.cache_clear()
        for move in self.bh.get_legal_moves():
            self.bh.make_move(move)
            score = self._minimax(self.bh.move_list, depth-1, False)
            self.bh.undo_move()
            if score > best_score:
                best_move = move
                best_score = score
        return best_move, best_score

    @lru_cache(maxsize=1000000)
    def _minimax(self, move_list, depth, is_maximizing):
        self.bh.update_board(move_list)
        if depth == 0:
            return self.evaluator.evaluate_board(move_list)
        if is_maximizing:
            best_score = -1000
            for move in self.bh.get_legal_moves():
                self.bh.make_move(move)
                score = self._minimax(self.bh.move_list, depth-1, False)
                self.bh.undo_move()
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = 1000
            for move in self.bh.get_legal_moves():
                self.bh.make_move(move)
                score = self._minimax(self.bh.move_list, depth-1, True)
                self.bh.undo_move()
                best_score = min(score, best_score)
            return best_score