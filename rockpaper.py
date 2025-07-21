import tkinter as tk
import random

OPTIONS = ["Rock", "Paper", "Scissors"]

class RPSGame:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissor Game")
        self.player_choice = None
        self.computer_choice = None
        self.label = tk.Label(master, text="Choose your move!", font=("Arial", 14))
        self.label.pack(pady=10)
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)
        self.rock_button = tk.Button(button_frame, text="Rock", width=10, command=lambda: self.play("Rock"))
        self.rock_button.grid(row=0, column=0, padx=5)
        self.paper_button = tk.Button(button_frame, text="Paper", width=10, command=lambda: self.play("Paper"))
        self.paper_button.grid(row=0, column=1, padx=5)
        self.scissors_button = tk.Button(button_frame, text="Scissors", width=10, command=lambda: self.play("Scissors"))
        self.scissors_button.grid(row=0, column=2, padx=5)
        self.reset_button = tk.Button(master, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(pady=10)
        self.result_label = tk.Label(master, text="", font=("Arial", 12))
        self.result_label.pack()

    def play(self, player_move):
        self.player_choice = player_move
        self.computer_choice = random.choice(OPTIONS)
        self.display_choices()
        self.determine_winner()

    def display_choices(self):
        self.result_label.config(text=f"Player chose: {self.player_choice}\nComputer chose: {self.computer_choice}")

    def determine_winner(self):
        if self.player_choice == self.computer_choice:
            result = "It's a Tie!"
        elif (self.player_choice == "Rock" and self.computer_choice == "Scissors") or \
             (self.player_choice == "Scissors" and self.computer_choice == "Paper") or \
             (self.player_choice == "Paper" and self.computer_choice == "Rock"):
            result = "You Win!"
        else:
            result = "Computer Wins!"
        self.result_label.config(text=f"{self.result_label.cget('text')}\nResult: {result}")

    def reset_game(self):
        self.result_label.config(text="Choose your move!")

if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGame(root)
    root.mainloop()