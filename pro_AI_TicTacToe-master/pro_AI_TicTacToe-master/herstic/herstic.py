
import tkinter as tk
from tkinter import messagebox

# Constants
EMPTY = ""
PLAYER = "X"
COMPUTER = "O"
WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]  # Diagonals
]

class TicTacToe:
    def __init__(self):
        self.board = [EMPTY] * 9
        self.current_player = PLAYER
        self.root = tk.Tk()
        self.buttons = []
        self.new_game_button = None



    def start (self):
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)

        for i in range(9):
            button = tk.Button(self.root, text=EMPTY, font=("Arial", 20), width=6, height=3)
            button.grid(row=i // 3, column=i % 3)
            button.config(command=lambda idx=i: self.make_move(idx))
            self.buttons.append(button)

        self.new_game_button = tk.Button(self.root, text="New Game", font=("Arial", 14), width=10, height=2)
        self.new_game_button.grid(row=3, columnspan=3)
        self.new_game_button.config(command=self.reset_game)

        self.root.mainloop()

    def make_move(self, index):
        if self.board[index] == EMPTY:
            self.board[index] = PLAYER
            self.buttons[index].config(text=PLAYER, state="disabled")
            if self.check_winner(PLAYER):
                self.game_over(PLAYER)
            elif EMPTY in self.board:
                self.current_player = COMPUTER
                self.root.after(500, self.computer_move)
            else:
                self.game_over(None)

    def computer_move(self):
        _, best_move = self.minimax(self.board, COMPUTER, float('-inf'), float('inf'))
        self.board[best_move] = COMPUTER
        self.buttons[best_move].config(text=COMPUTER, state="disabled")
        self.current_player = PLAYER
        if self.check_winner(COMPUTER):
            self.game_over(COMPUTER)

    def heuristic(self):
        # Simple heuristic: +1 for each COMPUTER win, -1 for each PLAYER win
        if self.check_winner(COMPUTER):
            return 1
        elif self.check_winner(PLAYER):
            return -1
        else:
            return 0

    def minimax(self, board, player, alpha, beta, depth=0):
        if self.check_winner(PLAYER):
            return -1, None
        elif self.check_winner(COMPUTER):
            return 1, None
        elif EMPTY not in board or depth == 9:  # Increase the depth limit
            return self.heuristic(), None

        best_move = None
        if player == COMPUTER:
            best_score = float('-inf')
            for move in range(len(board)):
                if board[move] == EMPTY:
                    board[move] = COMPUTER
                    score, _ = self.minimax(board, PLAYER, alpha, beta, depth + 1)
                    board[move] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = move
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break
        else:
            best_score = float('inf')
            for move in range(len(board)):
                if board[move] == EMPTY:
                    board[move] = PLAYER
                    score, _ = self.minimax(board, COMPUTER, alpha, beta, depth + 1)
                    board[move] = EMPTY
                    if score < best_score:
                        best_score = score
                        best_move = move
                    beta = min(beta, best_score)
                    if alpha >= beta:
                        break

        return best_score, best_move

    def check_winner(self, player):
        for combination in WINNING_COMBINATIONS:
            if all(self.board[idx] == player for idx in combination):
                return True
        return False

    def game_over(self, winner):
        for button in self.buttons:
            button.config(state="disabled")

        if winner is None:
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            messagebox.showinfo("Game Over", f"{winner} wins!")

        self.new_game_button.config(state="normal")

    def reset_game(self):
        self.board = [EMPTY] * 9
        self.current_player = PLAYER

        for button in self.buttons:
            button.config(text=EMPTY, state="normal")

        self.new_game_button.config(state="disabled")


if __name__ == "__main__":
    game = TicTacToe()
    game.start()
