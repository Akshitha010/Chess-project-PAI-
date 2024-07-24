import chess
import chess.engine
import math

# Define the depth for the AI search
SEARCH_DEPTH = 2

# Evaluation function for the board state
def evaluate_board(board):
    # This is a very simple evaluation function based on material
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material_score = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    return material_score

# Minimax with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -math.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = math.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

# Function to make the AI move
def ai_move(board):
    best_move = None
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf
    for move in board.legal_moves:
        board.push(move)
        value = minimax(board, SEARCH_DEPTH - 1, alpha, beta, False)
        board.pop()
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)
    return best_move

# Main function to run the game
def main():
    board = chess.Board()
    while not board.is_game_over():
        print(board)
        print("White's turn" if board.turn == chess.WHITE else "Black's turn")

        if board.turn == chess.WHITE:
            # Player's move input
            try:
                move = input("Enter your move: ")
                move = chess.Move.from_uci(move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move! Try again.")
            except ValueError:
                print("Invalid move format! Try again.")
        else:
            # AI's move
            move = ai_move(board)
            print(f"AI's move: {move.uci()}")
            board.push(move)

    print(board)
    print("Game over")
    if board.result() == "1-0":
        print("White wins!")
    elif board.result() == "0-1":
        print("Black wins!")
    else:
        print("It's a draw!")

if _name_ == "_main_":
    main()