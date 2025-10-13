import tkinter as tk
from tkinter import ttk, messagebox
import math

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("420x600")
        self.resizable(False, False)
        self.theme = "light"
        self.history = []

        self.style = ttk.Style(self)
        self.set_theme(self.theme)

        self.display = tk.Entry(self, font=("Consolas", 23), borderwidth=2, relief='solid', justify="right")
        self.display.pack(fill="x", padx=18, pady=(20,8), ipady=7)
        self.display.focus_set()

        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=8)

        btn_texts = [
            ["7", "8", "9", "/", "C", "sqrt"],
            ["4", "5", "6", "*", "(", ")"],
            ["1", "2", "3", "-", "ln", "log"],
            ["0", ".", "=", "+", "^", "π"],
            ["sin", "cos", "tan", "e", "Hist", "Theme"]
        ]

        for r, row in enumerate(btn_texts):
            for c, char in enumerate(row):
                action = (lambda ch=char: self.on_button_click(ch))
                b = ttk.Button(button_frame, text=char, width=5, command=action)
                b.grid(row=r, column=c, padx=3, pady=4)

        self.bind("<Return>", lambda _: self.evaluate("="))
        for k in '0123456789.+-*/()':
            self.bind(k, self.key_input)

    def set_theme(self, theme):
        if theme == "light":
            self.style.configure('TFrame', background='#F0F0FF')
            self.style.configure('TButton', background='#E0E0E0', font=('Consolas', 14))
            self.configure(bg="#F0F0FF")
        else:
            self.style.configure('TFrame', background='#22223B')
            self.style.configure('TButton', background='#4A4E69', foreground="#F2E9E4", font=('Consolas', 14))
            self.configure(bg="#22223B")

    def key_input(self, event):
        self.display.insert(tk.END, event.char)

    def on_button_click(self, char):
        if char == "C":
            self.display.delete(0, tk.END)
        elif char == "=":
            self.evaluate("=")
        elif char == "Hist":
            self.show_history()
        elif char == "Theme":
            self.toggle_theme()
        elif char == "π":
            self.display.insert(tk.END, str(math.pi))
        elif char == "e":
            self.display.insert(tk.END, str(math.e))
        elif char in ('sin', 'cos', 'tan', 'sqrt', 'log', 'ln'):
            self.display.insert(tk.END, f"{char}(")
        elif char == "^":
            self.display.insert(tk.END, "**")
        else:
            self.display.insert(tk.END, char)

    def evaluate(self, _):
        expr = self.display.get()
        try:
            # Map the math functions for eval
            allowed = {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'sqrt': math.sqrt, 'log': math.log10, 'ln': math.log,
                'pi': math.pi, 'e': math.e, 
                '__builtins__': {}
            }
            result = str(eval(expr, allowed, allowed))
            self.history.append(f"{expr} = {result}")
            self.display.delete(0, tk.END)
            self.display.insert(0, result)
        except Exception as e:
            messagebox.showerror("Error", "Invalid Expression")
            self.display.delete(0, tk.END)

    def show_history(self):
        hist = "\n".join(self.history[-10:]) if self.history else "No history yet!"
        messagebox.showinfo("Calculation History", hist)

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.set_theme(self.theme)

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
