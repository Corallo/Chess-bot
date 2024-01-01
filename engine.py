import chess
from functools import cache
from game_handler import ChessBoardHandler
import numpy as np


def is_variant_draw(board):
    return board.is_repetition() or board.is_stalemate() or board.is_insufficient_material()



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
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        self.piece_tables_white = {}
        self.piece_tables_black = {}
        for piece_type, piece_table in self.piece_tables.items():
            self.piece_tables_white[piece_type] = (np.flipud(piece_table) + self.piece_values[piece_type]).reshape(1,-1)[0]
            self.piece_tables_black[piece_type] = (piece_table + self.piece_values[piece_type]).reshape(1,-1)[0]
        print(self.piece_tables_white[chess.PAWN])

    def evaluate_board(self, board) -> int:
        if is_variant_draw(board):
            return 0
        if board.is_checkmate():
            return 10e6 if board.turn else -10e6
        score = 0
        for piece_type in self.piece_values.keys():
            score += sum(self.piece_tables_white[piece_type][list(board.pieces(piece_type, chess.WHITE))]) \
                  - sum(self.piece_tables_black[piece_type][list(board.pieces(piece_type, chess.BLACK))])
        return score


class chessEngine:
    def __init__(self):
        self.evaluator = ChessEvaluator()
        self.bh = ChessBoardHandler()
        self.MAX_EXTRA_MOVES = 2  # Max extra move to do deeper during search in case of capture

    def search_best_move(self, chessboard, depth=3, is_maximizing=True):
        best_move = None
        best_score = float('-inf') if is_maximizing else float('inf')
        for move in chessboard.legal_moves:
            chessboard.push(move)
            if is_variant_draw(chessboard):
                score = 0
            elif chessboard.is_checkmate():
                # Checkmate in 1 is better than checkmate in n
                score = (10e6)+1 if is_maximizing else (-10e6) - 1
            else:
                score = self._alpha_beta(
                    chessboard, depth-1, float('-inf'), float('inf'), not is_maximizing)
            chessboard.pop()
            if (is_maximizing and score >= best_score) or (not is_maximizing and score <= best_score):
                best_move = move
                best_score = score
        return best_move, best_score

    def _alpha_beta(self, chessboard, depth, alpha, beta, is_maximizing, last_move_was_capture=False):
        if depth <= -self.MAX_EXTRA_MOVES * (1 if last_move_was_capture or chessboard.is_check() else 0):
            return self.evaluator.evaluate_board(chessboard)
        if is_maximizing:
            best_score = float('-inf')
            for move in chessboard.legal_moves:
                last_move_was_capture = chessboard.is_capture(move)
                chessboard.push(move)
                if is_variant_draw(chessboard):
                    score = 0
                elif chessboard.is_checkmate():
                    score = 10e6
                else:
                    score = self._alpha_beta(
                        chessboard, depth-1, alpha, beta, False, last_move_was_capture)
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
                if is_variant_draw(chessboard):
                    score = 0
                elif chessboard.is_checkmate():
                    score = -10e6
                else:
                    score = self._alpha_beta(
                        chessboard, depth-1, alpha, beta, True, last_move_was_capture)
                chessboard.pop()
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score
