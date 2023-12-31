from engine import chessEngine
from game_handler import ChessBoardHandler

move_list = []

game = ChessBoardHandler("white")
engine = chessEngine()

move_str = " ".join(move_list)
game.update_board(move_str)
board = game.get_board()
move = engine.search_best_move(board)
print(move)

move_list = ["g1h3", "d7d5"]
move_str = " ".join(move_list)
game.update_board(move_str)
board = game.get_board()
move = engine.search_best_move(board)
print(move)


move_str="Nc3 d5 Nf3 Qd6 Nb5 Qb6 Nc3 d4 Nd5 Qh6 Nxc7+ Kd7 Nxa8 Ke8 Nc7+ Kd8 Nd5 Bd7 d3 b5 Bxh6 Nxh6 Nxd4 e5 Nf3 g5 Nxe5 Bb4+ Nxb4 Ke8 Qc1 Rg8 Nd5 f5 Nf6+ Kd8 Nxg8 Nxg8 Qxg5+ Ne7 Nf7+ Kc8 Qxe7 h5 Nd6+ Kc7 Nxb5+ Kb7 Nd6+ Ka6 Qd8 Ba4 Qc8+ Kb6 Qxb8+ Ka6 Qc8+ Kb6 b3 f4 bxa4 Ka5 Qc4 a6 Qxf4 Kb6 Qh4 Kc7 Ne4 Kc8 Rb1 Kc7 Rb2 Kd7 Qh3+ Ke7 Qxh5 Kd8 Qa5+ Ke8 Qxa6 Kf8 Qg6 Ke7 Qf5 Kd8 Kd1 Ke7"
game.update_board(move_str)
board = game.get_board()
move = engine.search_best_move(board)
print(move)

move_str ="Nc3 d5 Nf3 b6 Nd4 Bd7 Nxd5 Nh6 Rb1 f6 Ra1 Qc8 Rb1 g5 d3 Nf5 Nxf5 Bxf5 e4 Bg6 Qf3 Kf7 Bxg5 c5 Be2 Nc6 O-O c4 dxc4 b5 cxb5 Nd4 Qd3 Nxe2+ Qxe2 Rb8 Bf4 Rb7 Kh1 Rxb5 Qxb5 Bxe4 Rbc1 Bxg2+ Kxg2 Qg4+ Bg3 Qe4+ f3 Qg6 Qb8 f5 Nf4 Qb6 Qa8 Bh6 Qxh8 Bg7 Qxh7 a6 Rb1 e5 Nd5 Qg6 Qxg6+ Kxg6 Rf2 Kf7 Kh1 Bf6 Nxf6 Kxf6 Ra1 Kg7 Bxe5+ Kg8 Rg1+ Kf8 Rg5 Ke7 Rxf5 Ke8 Rf6 a5 Ra6 Kf7 Ra8 Ke6 Rxa5 Ke7 Ra8 Ke6 Re2 Kf5 Ra6 Kg5 Rd6 Kh4 Rf2 Kg5 Re2 Kh4 Rf2 Kg5"
game.update_board(move_str)
board = game.get_board()
move = engine.search_best_move(board)
print(move)

move_str = "Nc3 d5 Nf3 Qd6 Nb5 Qb6 Nc3 d4 Nd5 Qa6 Nxc7+ Kd8 Nxa6 Nxa6 Rb1 Nh6 Ra1 Rg8"
game.update_board(move_str)
board = game.get_board()
move = engine.search_best_move(board)
print(move)

move_str = "Nc3 d5"
game.update_board(move_str)
board = game.get_board()
move = engine.search_best_move(board)
print(move)