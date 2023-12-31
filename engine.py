import chess
from functools import lru_cache
from game_handler import ChessBoardHandler
import numpy as np

def is_variant_draw(board):
    if board.is_variant_draw():
        return True
    if board.is_repetition():
        return True
    if board.is_stalemate():
        return True
    if board.is_insufficient_material():
        return True
    return False
class ChessEvaluator:

    def __init__(self):
        self.bh = ChessBoardHandler()
        self.piece_tables = {
            chess.PAWN: np.array([
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5, 5, 10, 25, 25, 10, 5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, -5, -10, 0, 0, -10, -5, 5,
                5, 10, 10, -20, -20, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ]).reshape(8, 8),
            chess.KNIGHT: np.array([
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50
            ]).reshape(8, 8),
            chess.BISHOP: np.array([
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20
            ]).reshape(8, 8),
            chess.ROOK: np.array([
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ]).reshape(8, 8),
            chess.QUEEN: np.array([
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ]).reshape(8, 8),
            chess.KING: np.array([
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 30, 10, 0, 0, 10, 30, 20
            ]).reshape(8, 8),
        }

    def evaluate_board(self, board) -> int:
        if board.is_checkmate():
            return float('inf') if board.turn else float('-inf')
        #return if draw
        if is_variant_draw(board):
            return 0
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                color = 1 if piece.color else -1
                tmp_table = self.piece_tables[piece.piece_type]
                if color == 0: #black
                    tmp_table = np.flipud(tmp_table)
                score += (piece_values[piece.piece_type] + tmp_table[square % 8][square // 8]) * color
        return score


class chessEngine:
    def __init__(self):
        self.evaluator = ChessEvaluator()
        self.bh = ChessBoardHandler()
        self.MAX_EXTRA_MOVES = 3 # Max extra move to do deeper during search in case of capture

    def search_best_move(self, chessboard, depth=3, is_maximizing=True):
        best_move = None
        best_score = float('-inf') if is_maximizing else float('inf')
        for move in chessboard.legal_moves:
            chessboard.push(move)
            if is_variant_draw(chessboard):
                score = 0
            elif chessboard.is_checkmate():
                score = float('inf') if is_maximizing else float('-inf')
            else:
                score = self._alpha_beta(chessboard, depth-1, float('-inf'), float('inf'), not is_maximizing)
            chessboard.pop()
            if (is_maximizing and score >= best_score) or (not is_maximizing and score <= best_score):
                best_move = move
                best_score = score
        return best_move, best_score

    def _alpha_beta(self, chessboard, depth, alpha, beta, is_maximizing, last_move_was_capture=False):
        if is_variant_draw(chessboard):
            return 0
        if chessboard.is_checkmate():
            return float('inf') if is_maximizing else float('-inf')
        if depth <= -self.MAX_EXTRA_MOVES * (1 if last_move_was_capture or chessboard.is_check() else 0):
            return self.evaluator.evaluate_board(chessboard)
        if is_maximizing:
            best_score = float('-inf')
            for move in chessboard.legal_moves:
                last_move_was_capture = chessboard.is_capture(move)
                chessboard.push(move)
                score = self._alpha_beta(chessboard, depth-1, alpha, beta, False, last_move_was_capture)
                chessboard.pop()
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in chessboard.legal_moves:
                last_move_was_capture = chessboard.is_capture(move)
                chessboard.push(move)
                score = self._alpha_beta(chessboard, depth-1, alpha, beta, True, last_move_was_capture)
                chessboard.pop()
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score