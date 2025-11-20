import tkinter as tk
from tkinter import messagebox
import random
import os

JOKES_FILE = "randomJokes.txt"

def load_jokes():
    if not os.path.exists(JOKES_FILE):
        messagebox.showerror("Error", f"Cannot find {JOKES_FILE}!\nPlace it in the same folder as this script.")
        return []
    
    jokes = []
    with open(JOKES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "?" not in line:
                continue
            setup, punchline = line.split("?", 1)
            jokes.append((setup.strip() + "?", punchline.strip()))
    return jokes

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Alexa, Tell Me a Joke")
        self.root.geometry("575x650")
        self.root.configure(bg="#121212") 
        self.root.resizable(False, False)

        self.jokes = load_jokes()
        if not self.jokes:
            self.root.destroy()
            return

        self.current_joke = None

    
        title_font = ("Segoe UI", 24, "bold")
        setup_font = ("Segoe UI", 16)
        punch_font = ("Segoe UI", 18, "italic")
        btn_font = ("Segoe UI", 12, "bold")

        # Title
        title = tk.Label(root, text="🤖 Alexa, Tell Me a Joke!", font=title_font,
                         bg="#121212", fg="#00D4FF", pady=20)
        title.pack()

        # Joke container with subtle card effect
        card = tk.Frame(root, bg="#1E1E1E", relief="flat", bd=0, highlightthickness=2,
                        highlightbackground="#333333", padx=30, pady=30)
        card.pack(pady=20, fill="both", expand=True)

        self.setup_label = tk.Label(card, text="Click below to hear a hilarious joke!",
                                    font=setup_font, bg="#1E1E1E", fg="#E0E0E0",
                                    wraplength=580, justify="center")
        self.setup_label.pack(pady=(20, 10))

        self.punchline_label = tk.Label(card, text="", font=punch_font,
                                        bg="#1E1E1E", fg="#FF6B6B", wraplength=580,
                                        justify="center", height=3)
        self.punchline_label.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=20)

        # Gradient-style colorful buttons with high contrast
        self.tell_joke_btn = tk.Button(btn_frame, text="🎤 Alexa, Tell Me a Joke",
                                       font=btn_font, bg="#00D4FF", fg="#121212",
                                       activebackground="#00B0FF", activeforeground="white",
                                       relief="flat", width=22, height=2, command=self.tell_joke)
        self.tell_joke_btn.grid(row=0, column=0, padx=15)

        self.show_punchline_btn = tk.Button(btn_frame, text="😆 Show Punchline",
                                            font=btn_font, bg="#FF6B6B", fg="white",
                                            activebackground="#FF5252", relief="flat",
                                            width=22, height=2, command=self.show_punchline,
                                            state="disabled")
        self.show_punchline_btn.grid(row=0, column=1, padx=15)

        self.next_joke_btn = tk.Button(btn_frame, text="➜ Next Joke",
                                       font=btn_font, bg="#4ECDC4", fg="white",
                                       activebackground="#45B7AA", relief="flat",
                                       width=22, height=2, command=self.next_joke)
        self.next_joke_btn.grid(row=1, column=0, padx=15, pady=15)

        self.quit_btn = tk.Button(btn_frame, text="✖ Quit",
                                  font=btn_font, bg="#2F2F2F", fg="#FF6B6B",
                                  activebackground="#444444", relief="flat",
                                  width=22, height=2, command=root.quit)
        self.quit_btn.grid(row=1, column=1, padx=15, pady=15)

        # Hover effects 
        for btn in (self.tell_joke_btn, self.show_punchline_btn,
                    self.next_joke_btn, self.quit_btn):
            btn.bind("<Enter>", lambda e, b=btn: b.configure(relief="raised"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(relief="flat"))

    def tell_joke(self):
        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke
        self.setup_label.config(text=setup, fg="#00FF85")  #  green for setup
        self.punchline_label.config(text="")
        self.show_punchline_btn.config(state="normal")

    def show_punchline(self):
        if self.current_joke:
            _, punchline = self.current_joke
            self.punchline_label.config(text=punchline)
            self.show_punchline_btn.config(state="disabled")

    def next_joke(self):
        self.setup_label.config(text="Ready for another one? Click the button!", fg="#E0E0E0")
        self.punchline_label.config(text="")
        self.show_punchline_btn.config(state="disabled")
        self.current_joke = None


if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()