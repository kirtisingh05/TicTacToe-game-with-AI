import tkinter as tk
import math

# ---------- Game Logic (Minimax + Alpha-Beta) ----------

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
    """Return True if 'player' (X or O) has a winning line on the board."""
    return any(all(board[i] == player for i in combo) for combo in WIN_COMBINATIONS)

def check_draw(board):
    """Return True if the board is full and no one has won."""
    return " " not in board

def get_available_moves(board):
    """Return indices of all empty spots."""
    return [i for i, cell in enumerate(board) if cell == " "]

def evaluate(board):
    """Return +1 if O wins, -1 if X wins, else 0."""
    if check_win(board, "O"):
        return 1
    elif check_win(board, "X"):
        return -1
    return 0

def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    """Alpha-Beta Pruning to evaluate board states."""
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
    """Find the best move for 'O' (the AI)."""
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

# ---------- Tkinter GUI ----------

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe (Tkinter)")

        # The game board is a list of 9 cells: " ", "X", or "O".
        self.board = [" "] * 9
        self.current_player = "X"  # Human goes first

        # Create a status label
        self.status_label = tk.Label(self.root, text="Your turn (X)", font=("Arial", 14))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=5)

        # Create 9 buttons for the 3x3 grid
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.root, text=" ", font=("Arial", 20), width=5, height=2,
                            command=lambda idx=i: self.on_button_click(idx))
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Create a reset button
        reset_btn = tk.Button(self.root, text="Reset", font=("Arial", 12),
                              command=self.reset_game)
        reset_btn.grid(row=4, column=0, columnspan=3, pady=5)

    def on_button_click(self, index):
        """Handle a click on cell 'index' by the human player."""
        if self.board[index] != " ":
            return  # Already taken

        # Human move
        self.board[index] = "X"
        self.buttons[index].config(text="X")
        # Check if human just won
        if check_win(self.board, "X"):
            self.status_label.config(text="You win!")
            self.disable_all_buttons()
            return
        # Check draw
        if check_draw(self.board):
            self.status_label.config(text="It's a draw!")
            self.disable_all_buttons()
            return

        # Switch to computer's turn
        self.status_label.config(text="Computer thinking...")
        self.root.update_idletasks()

        # Computer (O) uses alpha-beta to pick a move
        comp_move = get_best_move(self.board)
        if comp_move is not None:
            self.board[comp_move] = "O"
            self.buttons[comp_move].config(text="O")
            # Check if computer won
            if check_win(self.board, "O"):
                self.status_label.config(text="Computer wins!")
                self.disable_all_buttons()
                return
            # Check draw
            if check_draw(self.board):
                self.status_label.config(text="It's a draw!")
                self.disable_all_buttons()
                return

        self.status_label.config(text="Your turn (X)")

    def disable_all_buttons(self):
        """Disable the grid buttons (game ends)."""
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def reset_game(self):
        """Reset board and UI for a new game."""
        self.board = [" "] * 9
        self.current_player = "X"
        self.status_label.config(text="Your turn (X)")
        for btn in self.buttons:
            btn.config(text=" ", state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
