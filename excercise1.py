import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os
from datetime import datetime

# Sound effects 
try:
    from playsound import playsound
    SOUND_AVAILABLE = True
except:
    SOUND_AVAILABLE = False

# High score file exceptional feature
SCORE_FILE = "math_quiz_highscore.json"

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Math Speed Quiz ⚡")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        # Theme 
        self.dark_mode = True
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#00ff88"
        self.wrong_color = "#ff4d4d"

        # Game variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.attempts = 0
        self.time_left = 60
        self.streak = 0
        self.best_streak = 0
        self.high_score = self.load_high_score()
        self.timer_running = False

        self.confetti_canvas = None

        self.create_welcome_screen()

    def load_high_score(self):
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        return 0

    def save_high_score(self):
        data = {"high_score": self.high_score, "date": datetime.now().strftime("%Y-%m-%d")}
        with open(SCORE_FILE, "w") as f:
            json.dump(data, f)

    def play_sound(self, correct=True):
        if not SOUND_AVAILABLE:
            return

        pass

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.bg_color = "#1e1e1e"
            self.fg_color = "#ffffff"
            self.root.configure(bg="#1e1e1e")
        else:
            self.bg_color = "#f0f0f0"
            self.fg_color = "#000000"
            self.root.configure(bg="#f0f0f0")
        self.refresh_colors()

    def refresh_colors(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Frame)):
                widget.configure(bg=self.bg_color, fg=self.fg_color)
            if isinstance(widget, tk.Button):
                widget.configure(highlightbackground=self.bg_color)

    def create_welcome_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill="both", padx=40, pady=40)

        tk.Label(frame, text="⚡ Ultimate Math Quiz ⚡", font=("Helvetica", 28, "bold"),
                 bg=self.bg_color, fg=self.accent_color).pack(pady=30)

        tk.Label(frame, text="Test your arithmetic skills under pressure!", font=("Arial", 14),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        tk.Label(frame, text=f"🏆 High Score: {self.high_score}", font=("Arial", 16, "bold"),
                 bg=self.bg_color, fg="#ffd700").pack(pady=20)

        tk.Label(frame, text="Choose Difficulty Level", font=("Arial", 18, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=20)

        levels = [
            ("🟢 1. Easy (1-digit numbers)", "easy", 0, 9),
            ("🟡 2. Moderate (2-digit numbers)", "moderate", 10, 99),
            ("🔴 3. Advanced (4-digit numbers)", "advanced", 1000, 9999)
        ]

        for text, level, min_val, max_val in levels:
            btn = tk.Button(frame, text=text, font=("Arial", 14),
                           command=lambda l=level, mn=min_val, mx=max_val: self.start_quiz(l, mn, mx),
                           width=40, height=2, bg="#333333", fg="white", relief="flat")
            btn.pack(pady=10)
            btn.configure(activebackground=self.accent_color)

        # Theme toggle
        tk.Button(frame, text="🌙 Toggle Theme", command=self.toggle_theme,
                  font=("Arial", 10)).pack(pady=20)

    def start_quiz(self, difficulty, min_num, max_num):
        self.difficulty = difficulty
        self.min_num = min_num
        self.max_num = max_num
        self.score = 0
        self.current_question = 0
        self.streak = 0
        self.time_left = 60
        self.timer_running = True

        self.create_quiz_screen()
        self.next_question()
        self.start_timer()

    def create_quiz_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header
        header = tk.Frame(self.root, bg=self.bg_color)
        header.pack(fill="x", padx=20, pady=10)

        tk.Label(header, text="Math Quiz", font=("Helvetica", 24, "bold"),
                 bg=self.bg_color, fg=self.accent_color).pack(side="left")

        self.timer_label = tk.Label(header, text=f"Time: {self.time_left}s", font=("Arial", 16, "bold"),
                                    bg=self.bg_color, fg="#ff6b6b")
        self.timer_label.pack(side="right")

        # Progress
        self.progress = tk.Canvas(self.root, height=20, bg="#333", highlightthickness=0)
        self.progress.pack(fill="x", padx=40, pady=10)
        self.progress_rect = self.progress.create_rectangle(0, 0, 0, 20, fill=self.accent_color)

        # Score and Streak
        info_frame = tk.Frame(self.root, bg=self.bg_color)
        info_frame.pack(pady=10)

        self.score_label = tk.Label(info_frame, text="Score: 0", font=("Arial", 16),
                                    bg=self.bg_color, fg=self.fg_color)
        self.score_label.pack(side="left", padx=20)

        self.streak_label = tk.Label(info_frame, text="🔥 Streak: 0", font=("Arial", 16),
                                     bg=self.bg_color, fg="#ff9f1c")
        self.streak_label.pack(side="right", padx=20)

        # Question area
        self.question_frame = tk.Frame(self.root, bg=self.bg_color)
        self.question_frame.pack(expand=True, pady=50)

        self.question_label = tk.Label(self.question_frame, text="", font=("Courier", 36, "bold"),
                                       bg=self.bg_color, fg=self.fg_color)
        self.question_label.pack(pady=30)

        self.feedback_label = tk.Label(self.question_frame, text="", font=("Arial", 18),
                                       bg=self.bg_color, fg=self.wrong_color)
        self.feedback_label.pack(pady=10)

        # Answer entry
        entry_frame = tk.Frame(self.root, bg=self.bg_color)
        entry_frame.pack(pady=20)

        self.answer_entry = tk.Entry(entry_frame, font=("Arial", 24), width=12, justify="center")
        self.answer_entry.pack(side="left", padx=10)
        self.answer_entry.focus()
        self.answer_entry.bind("<Return>", lambda e: self.check_answer())

        submit_btn = tk.Button(entry_frame, text="Submit", command=self.check_answer,
                               font=("Arial", 14), bg=self.accent_color, fg="black")
        submit_btn.pack(side="left")

    def start_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}s")
            if self.time_left <= 10:
                self.timer_label.config(fg="#ff4d4d")
            self.root.after(1000, self.start_timer)
        elif self.time_left == 0:
            self.end_quiz()

    def next_question(self):
        if self.current_question >= self.total_questions:
            self.end_quiz()
            return

        self.current_question += 1
        self.attempts = 0
        self.feedback_label.config(text="")

        num1 = random.randint(self.min_num, self.max_num)
        num2 = random.randint(self.min_num, self.max_num)
        operation = random.choice(["+", "-"])

        # Prevent results
        if operation == "-" and num1 < num2:
            num1, num2 = num2, num1

        self.current_answer = num1 + num2 if operation == "+" else num1 - num2
        self.current_operation = operation

        question_text = f"{num1} {operation} {num2} ="
        self.question_label.config(text=question_text)

        # Update progress bar
        progress_width = (self.current_question / self.total_questions) * 520
        self.progress.coords(self.progress_rect, 0, 0, progress_width, 20)

        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()

    def check_answer(self):
        user_input = self.answer_entry.get().strip()
        if not user_input or not user_input.lstrip("-").isdigit():
            self.feedback_label.config(text="❌ Please enter a valid number!", fg=self.wrong_color)
            return

        user_answer = int(user_input)

        if user_answer == self.current_answer:
            self.attempts += 1
            points = 10 if self.attempts == 1 else 5
            self.score += points
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak

            self.score_label.config(text=f"Score: {self.score}")
            self.streak_label.config(text=f"🔥 Streak: {self.streak} (Best: {self.best_streak})")

            self.feedback_label.config(text="Correct! 🎉" if self.attempts == 1 else "Correct on 2nd try! 👍",
                                       fg=self.accent_color)
            self.play_sound(correct=True)
            self.root.after(1000, self.next_question)
        else:
            self.attempts += 1
            self.streak = 0
            self.streak_label.config(text=f"🔥 Streak: 0")

            if self.attempts == 1:
                self.feedback_label.config(text="❌ Wrong! Try again!", fg=self.wrong_color)
                self.play_sound(correct=False)
            else:
                self.feedback_label.config(text=f"❌ Wrong! Answer was {self.current_answer}", fg=self.wrong_color)
                self.root.after(2000, self.next_question)

    def end_quiz(self):
        self.timer_running = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            new_record = " 🏆 NEW HIGH SCORE! 🏆"
        else:
            new_record = ""

        percentage = (self.score / 100) * 100
        if percentage >= 95:
            rank = "A+ 🧠 Genius!"
        elif percentage >= 85:
            rank = "A 💡 Excellent!"
        elif percentage >= 70:
            rank = "B 👍 Good Job!"
        elif percentage >= 50:
            rank = "C 😊 Not Bad"
        else:
            rank = "D 😅 Keep Practicing!"

        result = f"""
        🎉 Quiz Complete! 🎉{new_record}
        
        Final Score: {self.score}/100
        Accuracy: {percentage:.1f}%
        Best Streak: {self.best_streak}
        
        Grade: {rank}
        """

        if self.score == 100:
            self.show_confetti()

        play_again = messagebox.askyesno("Quiz Finished", result + "\n\nDo you want to play again?")
        if play_again:
            self.create_welcome_screen()
        else:
            self.root.quit()

    def show_confetti(self):
        if self.confetti_canvas:
            self.confetti_canvas.destroy()
        self.confetti_canvas = tk.Canvas(self.root, width=600, height=700, bg=self.bg_color, highlightthickness=0)
        self.confetti_canvas.place(x=0, y=0)

        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"]
        for _ in range(200):
            x = random.randint(0, 600)
            y = random.randint(-100, 0)
            size = random.randint(5, 15)
            color = random.choice(colors)
            self.confetti_canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            dx = random.randint(-5, 5)
            dy = random.randint(3, 10)
            self.animate_confetti(x, y, dx, dy, size, color)

    def animate_confetti(self, x, y, dx, dy, size, color):
        if y < 700:
            x += dx
            y += dy
            self.confetti_canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.root.after(50, lambda: self.animate_confetti(x, y, dx, dy+0.5, size, color))


if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()