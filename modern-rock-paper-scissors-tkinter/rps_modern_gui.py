import tkinter as tk
from PIL import Image, ImageTk
import random
import pyttsx3
import threading

root = tk.Tk()
root.title('Rock Paper Scissors — Modern UI')
root.geometry('420x400')
root.configure(bg="#f0f4f9")  # soft background

# Load images (match your files and folder)
rock_img = ImageTk.PhotoImage(Image.open('Rock.jpg').resize((100,100)))
paper_img = ImageTk.PhotoImage(Image.open('Paper.jpg').resize((100,100)))
scissors_img = ImageTk.PhotoImage(Image.open('Scissors.jpg').resize((100,100)))
choice_imgs = {'Rock': rock_img, 'Paper': paper_img, 'Scissors': scissors_img}

score = {'Player': 0, 'Friend': 0, 'Tie': 0}

# List available voices (run separately if you want to see full options)
# import pyttsx3
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# for idx, voice in enumerate(voices):
#     print(idx, voice.name, voice.id)

def speak(text, voice_idx=1):
    def _speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)  # Max volume
        voices = engine.getProperty('voices')
        if voice_idx < len(voices):
            engine.setProperty('voice', voices[voice_idx].id)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

def play(player_choice):
    comp_choice = random.choice(['Rock', 'Paper', 'Scissors'])
    choices_label.configure(image=choice_imgs[player_choice])
    comp_label.configure(image=choice_imgs[comp_choice])
    if player_choice == comp_choice:
        result = "Tie!"
        score['Tie'] += 1
        speak("tie Play again!", voice_idx=1)  # Female
    elif (
        (player_choice == "Rock" and comp_choice == "Scissors") or
        (player_choice == "Paper" and comp_choice == "Rock") or
        (player_choice == "Scissors" and comp_choice == "Paper")
    ):
        result = "You Win!"
        score['Player'] += 1
        speak(" you won!", voice_idx=0)  # Male
    else:
        result = "Friend Wins!"
        score['Friend'] += 1
        speak("your friend won!", voice_idx=1)  # Female
    result_label.config(text=result)
    update_scoreboard()

def update_scoreboard():
    scoreboard.config(text=f"You: {score['Player']}   Friend: {score['Friend']}   Ties: {score['Tie']}")

def reset():
    choices_label.configure(image='')
    comp_label.configure(image='')
    result_label.config(text="Make your move!")
    for k in score:
        score[k] = 0
    update_scoreboard()

def on_enter(e):
    e.widget['background'] = '#c8dafc'  # Light blue highlight

def on_leave(e):
    e.widget['background'] = '#e3e8f1'  # Original color

title = tk.Label(root, text="Rock Paper Scissors", font=("Segoe UI", 22, "bold"), bg="#f0f4f9", fg="#202124")
title.pack(pady=12)

scoreboard = tk.Label(root, text="You: 0   Friend: 0   Ties: 0", font=("Segoe UI", 14), bg="#f0f4f9")
scoreboard.pack(pady=10)

frame = tk.Frame(root, bg="#f0f4f9")
frame.pack(pady=10)

choices_label = tk.Label(frame, bg="#f0f4f9")
choices_label.grid(row=0, column=0, padx=18)
vs_label = tk.Label(frame, text="   vs   ", font=("Segoe UI", 14, "bold"), bg="#f0f4f9", fg="#1967d2")
vs_label.grid(row=0, column=1)
comp_label = tk.Label(frame, bg="#f0f4f9")
comp_label.grid(row=0, column=2, padx=18)

result_label = tk.Label(root, text="Make your move!", font=("Segoe UI", 15, "italic"), bg="#f0f4f9", fg="#5c6bc0")
result_label.pack(pady=16)

btn_frame = tk.Frame(root, bg="#f0f4f9")
btn_frame.pack(pady=10)
btn_images = []
for col, choice in enumerate(['Rock', 'Paper', 'Scissors']):
    img = choice_imgs[choice]
    btn = tk.Button(btn_frame, image=img, command=lambda c=choice: play(c), relief='flat', bg="#e3e8f1", bd=2)
    btn.grid(row=0, column=col, padx=10, ipadx=6, ipady=6)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn_images.append(img)

reset_btn = tk.Button(root, text="Reset", command=reset, font=("Segoe UI", 12), bg="#ef5350", fg="white", relief='raised')
reset_btn.pack(pady=22)

root.mainloop()
