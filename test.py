from engine import chessEngine
from game_handler import ChessBoardHandler

move_list = []

game = ChessBoardHandler("white")
engine = chessEngine()

move_str = " ".join(move_list)
move = engine.search_best_move(move_str)
print(move)

move_list = ["g1h3", "d7d5"]
move_str = " ".join(move_list)
move = engine.search_best_move(move_str)
print(move)

