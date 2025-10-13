import tkinter as tk
import random

# Choices
choices = ["rock", "paper", "scissors"]

# Scores
user_score = 0
comp_score = 0

# Function to play game
def play(user_choice):
    global user_score, comp_score

    comp_choice = random.choice(choices)

    if user_choice == comp_choice:
        result = f"🤝 Tie! Both chose {user_choice}"
    elif (user_choice == "rock" and comp_choice == "scissors") or \
         (user_choice == "scissors" and comp_choice == "paper") or \
         (user_choice == "paper" and comp_choice == "rock"):
        result = f"🎉 You Win! {user_choice} beats {comp_choice}"
        user_score += 1
    else:
        result = f"😢 You Lose! {comp_choice} beats {user_choice}"
        comp_score += 1

    # Update labels
    result_label.config(text=result)
    score_label.config(text=f"Score → You: {user_score} | Computer: {comp_score}")

# GUI setup
root = tk.Tk()
root.title("Rock Paper Scissors Game")

# Title
title = tk.Label(root, text="🎮 Rock, Paper, Scissors 🎮", font=("Arial", 20))
title.pack(pady=10)

# Buttons
frame = tk.Frame(root)
frame.pack()

rock_btn = tk.Button(frame, text="✊ Rock", font=("Arial", 16), width=12, command=lambda: play("rock"))
rock_btn.grid(row=0, column=0, padx=5, pady=5)

paper_btn = tk.Button(frame, text="✋ Paper", font=("Arial", 16), width=12, command=lambda: play("paper"))
paper_btn.grid(row=0, column=1, padx=5, pady=5)

scissors_btn = tk.Button(frame, text="✌ Scissors", font=("Arial", 16), width=12, command=lambda: play("scissors"))
scissors_btn.grid(row=0, column=2, padx=5, pady=5)

# Result label
result_label = tk.Label(root, text="Make your move!", font=("Arial", 16))
result_label.pack(pady=15)

# Score label
score_label = tk.Label(root, text="Score → You: 0 | Computer: 0", font=("Arial", 14))
score_label.pack()

# Run game
root.mainloop()
