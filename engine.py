import chess
from functools import lru_cache
from game_handler import ChessBoardHandler

class ChessEvaluator:

    def __init__(self):
        self.bh = ChessBoardHandler()
        self.piece_tables ={chess.PAWN:
                [ 0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
                5, -5,-10,  0,  0,-10, -5,  5,
                5, 10, 10,-20,-20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0],
                chess.KNIGHT:
                [-50,-40,-30,-30,-30,-30,-40,-50,
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50],
                chess.BISHOP:
                [-20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20],
                chess.ROOK:
                [0,  0,  0,  0,  0,  0,  0,  0,
                 5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                 0,  0,  0,  5,  5,  0,  0,  0],
                chess.QUEEN:
                [-20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                 -5,  0,  5,  5,  5,  5,  0, -5,
                  0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20],
                chess.KING:
                [-30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                20, 20,  0,  0,  0,  0, 20, 20,
                20, 30, 10,  0,  0, 10, 30, 20]
                }
    @lru_cache(maxsize=100000)
    def evaluate_board(self, move_str: str) -> int:
        self.bh.update_board(move_str)
        board = self.bh.get_board()
        #return if checkmate
        if board.is_checkmate():
            return float('inf') if board.turn else float('-inf')
        #return if draw
        if board.is_variant_draw():
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
                    tmp_table.reverse()
                score += (piece_values[piece.piece_type] + tmp_table[square]) * color
        return score


class chessEngine:
    def __init__(self):
        self.evaluator = ChessEvaluator()
        self.bh = ChessBoardHandler()

    def search_best_move(self, moves_str, depth=3, is_maximizing=True):

        self.bh.update_board(moves_str)
        best_move = None
        best_score = float('-inf') if is_maximizing else float('inf')
        for move in self.bh.get_legal_moves():
            self.bh.make_move(move)

            if self.bh.check_draw():
                score = 0
            elif self.bh.check_mate():
                score = float('inf') if is_maximizing else float('-inf')
            else:
                score = self._alpha_beta(self.bh.move_str, depth-1, float('-inf'), float('inf'), not is_maximizing)
            self.bh.undo_move()
            if (is_maximizing and score >= best_score) or (not is_maximizing and score <= best_score):
                best_move = move
                best_score = score
        return best_move, best_score

    @lru_cache(maxsize=100000)
    def _minimax(self, move_str, depth, is_maximizing):
        self.bh.update_board(move_str)
        if depth == 0:
            return self.evaluator.evaluate_board(move_str)
        if is_maximizing:
            best_score = float('-inf')
            for move in self.bh.get_legal_moves():
                self.bh.make_move(move)
                score = self._minimax(self.bh.move_str, depth-1, False)
                self.bh.undo_move()
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.bh.get_legal_moves():
                self.bh.make_move(move)
                score = self._minimax(self.bh.move_str, depth-1, True)
                self.bh.undo_move()
                best_score = min(score, best_score)
            return best_score

    @lru_cache(maxsize=100000)
    def _alpha_beta(self, move_str, depth, alpha, beta, is_maximizing):
        self.bh.update_board(move_str)
        if depth == 0:
            return self.evaluator.evaluate_board(move_str)
        if is_maximizing:
            best_score = float('-inf')
            for move in self.bh.get_legal_moves():
                self.bh.make_move(move)
                score = self._alpha_beta(self.bh.move_str, depth-1, alpha, beta, False)
                self.bh.undo_move()
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in self.bh.get_legal_moves():
                self.bh.make_move(move)
                score = self._alpha_beta(self.bh.move_str, depth-1, alpha, beta, True)
                self.bh.undo_move()
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score