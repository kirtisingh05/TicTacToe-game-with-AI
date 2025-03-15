from flask import Flask, request, redirect, url_for
import math

app = Flask(__name__)

# ---------- Game Logic (Minimax with Alpha-Beta) ----------
WIN_COMBINATIONS = [
    [0, 1, 2],  # Top row
    [3, 4, 5],  # Middle row
    [6, 7, 8],  # Bottom row
    [0, 3, 6],  # Left column
    [1, 4, 7],  # Middle column
    [2, 5, 8],  # Right column
    [0, 4, 8],  # Diagonal
    [2, 4, 6]   # Diagonal
]

def check_win(board, player):
    return any(all(board[i] == player for i in combo) for combo in WIN_COMBINATIONS)

def check_draw(board):
    return " " not in board

def get_available_moves(board):
    return [i for i, spot in enumerate(board) if spot == " "]

def evaluate(board):
    if check_win(board, "O"):
        return 1
    elif check_win(board, "X"):
        return -1
    return 0

def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    score = evaluate(board)
    if depth == 0 or score != 0 or check_draw(board):
        return score
    if maximizingPlayer:
        maxEval = -math.inf
        for move in get_available_moves(board):
            board[move] = "O"
            val = alphabeta(board, depth - 1, alpha, beta, False)
            board[move] = " "
            maxEval = max(maxEval, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = math.inf
        for move in get_available_moves(board):
            board[move] = "X"
            val = alphabeta(board, depth - 1, alpha, beta, True)
            board[move] = " "
            minEval = min(minEval, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return minEval

def get_best_move(board):
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        board[move] = "O"
        score = alphabeta(board, depth=len(get_available_moves(board)),
                          alpha=-math.inf, beta=math.inf, maximizingPlayer=False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def new_board():
    return [" " for _ in range(9)]

# ---------- Flask Routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    board_str = request.args.get("board")
    if board_str and len(board_str) == 9:
        board = list(board_str)
    else:
        board = new_board()

    message = request.args.get("message", "")
    # If message indicates game over, disable moves.
    game_over = message in ["You win!", "Computer wins!", "Draw!"]
    disabled_attr = "disabled" if game_over else ""

    if request.method == "POST" and not game_over:
        try:
            move = int(request.form["move"])
        except (KeyError, ValueError):
            return redirect(url_for("index", board="".join(board), message="Invalid move"))
        if board[move] != " ":
            return redirect(url_for("index", board="".join(board), message="Cell already taken"))
        
        # Human move (X)
        board[move] = "X"
        if check_win(board, "X"):
            return redirect(url_for("index", board="".join(board), message="You win!"))
        if check_draw(board):
            return redirect(url_for("index", board="".join(board), message="Draw!"))
        
        # Computer move (O)
        comp_move = get_best_move(board)
        if comp_move is not None:
            board[comp_move] = "O"
            if check_win(board, "O"):
                return redirect(url_for("index", board="".join(board), message="Computer wins!"))
            if check_draw(board):
                return redirect(url_for("index", board="".join(board), message="Draw!"))
        
        return redirect(url_for("index", board="".join(board)))

    # Updated HTML using a single form for the board
    html = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Tic Tac Toe</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
          .ttt-board {{
            margin: 20px auto;
            width: 300px;
          }}
          .ttt-board table {{
            width: 300px;
            height: 300px;
            border-collapse: collapse;
            table-layout: fixed;
          }}
          .ttt-board td {{
            border: 2px solid #343a40;
            padding: 0;
            text-align: center;
            vertical-align: middle;
          }}
          .ttt-board button {{
            width: 100%;
            height: 100%;
            font-size: 2rem;
            background-color: #f8f9fa;
            border: none;
            cursor: pointer;
            transition: background-color 0.2s;
          }}
          .ttt-board button:hover {{
            background-color: #dee2e6;
          }}
          .ttt-board button:disabled {{
            background-color: #e9ecef;
            cursor: not-allowed;
          }}
          .status-message {{
            text-align: center;
            font-size: 1.5rem;
            margin-top: 10px;
          }}
          .reset-btn {{
            display: block;
            margin: 20px auto 0 auto;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1 class="text-center mt-4">Tic Tac Toe</h1>
          <div class="status-message text-center text-danger">{message if game_over else "Your turn (X)"}</div>
          <form method="post">
            <div class="ttt-board">
              <table>
                <tbody>
                  <tr>
                    <td><button type="submit" name="move" value="0" {disabled_attr}>{board[0]}</button></td>
                    <td><button type="submit" name="move" value="1" {disabled_attr}>{board[1]}</button></td>
                    <td><button type="submit" name="move" value="2" {disabled_attr}>{board[2]}</button></td>
                  </tr>
                  <tr>
                    <td><button type="submit" name="move" value="3" {disabled_attr}>{board[3]}</button></td>
                    <td><button type="submit" name="move" value="4" {disabled_attr}>{board[4]}</button></td>
                    <td><button type="submit" name="move" value="5" {disabled_attr}>{board[5]}</button></td>
                  </tr>
                  <tr>
                    <td><button type="submit" name="move" value="6" {disabled_attr}>{board[6]}</button></td>
                    <td><button type="submit" name="move" value="7" {disabled_attr}>{board[7]}</button></td>
                    <td><button type="submit" name="move" value="8" {disabled_attr}>{board[8]}</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </form>
          <a href="/" class="btn btn-danger reset-btn">Restart Game</a>
        </div>
        <!-- Optional JavaScript -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
      </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
