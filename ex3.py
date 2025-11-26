import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# ====================== Student Class ======================
class Student:
    def __init__(self, code, name, cw1, cw2, cw3, exam):
        self.code = int(code)
        self.name = name.strip()
        self.cw = [int(cw1), int(cw2), int(cw3)]
        self.exam = int(exam)

    def total_cw(self):
        return sum(self.cw)

    def total_score(self):
        return self.total_cw() + self.exam

    def percentage(self):
        return (self.total_score() / 160) * 100

    def grade(self):
        p = self.percentage()
        if p >= 70: return 'A'
        elif p >= 60: return 'B'
        elif p >= 50: return 'C'
        elif p >= 40: return 'D'
        else: return 'F'


# ====================== File Handling ======================
FILENAME = "studentMarks.txt"

def load_students():
    if not os.path.exists(FILENAME):
        messagebox.showerror("File Error", f"{FILENAME} not found!\nUsing sample data.")
        return []  # Will load from document if needed

    students = []
    try:
        with open(FILENAME, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if not lines:
            return []
        n = int(lines[0])
        for line in lines[1:1+n]:
            parts = line.split(',')
            if len(parts) == 6:
                code, name, c1, c2, c3, exam = parts
                students.append(Student(code, name, c1, c2, c3, exam))
    except Exception as e:
        messagebox.showerror("Load Error", f"Error reading file:\n{e}")
    return students


def save_students(students):
    try:
        with open(FILENAME, 'w') as f:
            f.write(f"{len(students)}\n")
            for s in students:
                f.write(f"{s.code},{s.name},{s.cw[0]},{s.cw[1]},{s.cw[2]},{s.exam}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save file:\n{e}")


# ====================== Main App ======================
class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Records System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#f4f6f9")

        self.students = load_students()
        self.setup_styles()
        self.create_layout()
        self.update_status(f"Loaded {len(self.students)} student records")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Professional Color Palette
        self.colors = {
            'primary': '#0d47a1',      # Deep Blue
            'primary_light': '#5472d3',
            'primary_dark': '#002171',
            'accent': '#1565c0',
            'success': '#2e7d32',
            'warning': '#ff8f00',
            'danger': '#c62828',
            'bg': '#f4f6f9',
            'surface': '#ffffff',
            'text': '#263238',
            'text_light': '#546e7a',
            'border': '#dfe6e9'
        }

        # Configure Treeview
        style.configure("Custom.Treeview", 
                        background="white",
                        foreground=self.colors['text'],
                        rowheight=40,
                        fieldbackground="white",
                        font=("Segoe UI", 10))
        
        style.configure("Custom.Treeview.Heading",
                        font=("Helvetica", 11, "bold"),
                        background=self.colors['primary'],
                        foreground="white")

        style.map("Custom.Treeview",
                  background=[('selected', self.colors['primary_light'])],
                  foreground=[('selected', 'white')])

        # Alternating row colors
        style.configure("evenrow", background="#fafafa")
        style.configure("oddrow", background="white")

        # Button Style
        style.configure("Action.TButton",
                        font=("Helvetica", 11, "bold"),
                        padding=(20, 14),
                        background=self.colors['primary'],
                        foreground="white")
        
        style.map("Action.TButton",
                  background=[('active', self.colors['primary_light'])],
                  foreground=[('active', 'white')])

    def create_layout(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="Academic Records System", 
                        font=("Helvetica", 28, "bold"), fg="white", bg=self.colors['primary'])
        title.pack(pady=20)

        subtitle = tk.Label(header, text="Department of Computer Science • Grade Management Portal", 
                           font=("Helvetica", 11), fg="#bbdefb", bg=self.colors['primary'])
        subtitle.pack(pady=(0, 10))

        # Main Container
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left Sidebar - Actions
        sidebar = tk.Frame(main, bg="white", relief=tk.RIDGE, bd=1, width=320)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Actions", font=("Helvetica", 16, "bold"), 
                bg="white", fg=self.colors['primary'], anchor="w").pack(fill=tk.X, padx=25, pady=(30, 15))

        actions = [
            ("All Students", self.view_all),
            ("Search Student", self.view_individual),
            ("Top Performer", self.show_highest),
            ("Lowest Performer", self.show_lowest),
            ("Sort Records", self.sort_records),
            ("Add New Student", self.add_student),
            ("Update Record", self.update_student),
            ("Delete Student", self.delete_student),
        ]

        for text, cmd in actions:
            btn = ttk.Button(sidebar, text=text, style="Action.TButton", command=cmd)
            btn.pack(fill=tk.X, padx=25, pady=8)

        # Right Panel - Data Table
        data_panel = tk.Frame(main, bg="white", relief=tk.RIDGE, bd=1)
        data_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(data_panel, text="Student Performance Records", 
                font=("Helvetica", 14, "bold"), bg="white", fg=self.colors['primary'], anchor="w")\
                .pack(fill=tk.X, padx=20, pady=(20, 10))

        # Treeview
        columns = ("Name", "ID", "CW/60", "Exam/100", "Total", "%", "Grade")
        self.tree = ttk.Treeview(data_panel, columns=columns, show="headings", style="Custom.Treeview")
        
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        
        self.tree.column("Name", width=220, anchor=tk.W)
        self.tree.column("Grade", width=90)

        # Scrollbars
        v_scroll = ttk.Scrollbar(data_panel, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(data_panel, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready • System initialized successfully")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, padx=10, pady=5,
                             bg="#263238", fg="#ecf0f1", font=("Segoe UI", 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, msg):
        self.status_var.set(f"Status • {msg}")

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def display_students(self, stu_list):
        self.clear_tree()
        if not stu_list:
            self.update_status("No records to display")
            return

        avg = sum(s.percentage() for s in stu_list) / len(stu_list)

        for idx, s in enumerate(stu_list):
            perc = s.percentage()
            grade = s.grade()
            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
            grade_color = {
                'A': '#1b5e20', 'B': '#0d47a1', 'C': '#e65100',
                'D': '#e65100', 'F': '#b71c1c'
            }.get(grade, '#546e7a')

            self.tree.insert("", tk.END, values=(
                s.name,
                s.code,
                s.total_cw(),
                s.exam,
                s.total_score(),
                f"{perc:.1f}",
                grade
            ), tags=(row_tag, f"grade_{grade}"))

            self.tree.tag_configure(f"grade_{grade}", foreground=grade_color, font=("Segoe UI", 10, "bold"))

        self.update_status(f"Displaying {len(stu_list)} records • Class Average: {avg:.2f}%")

    def view_all(self):
        self.display_students(self.students)

    def find_student(self):
        query = simpledialog.askstring("Search Student", "Enter Student ID or Full Name:")
        if not query:
            return None
        query = query.strip()
        for s in self.students:
            if str(s.code) == query or s.name.lower() == query.lower():
                return s
        messagebox.showwarning("Not Found", "Student not found.")
        return None

    def view_individual(self):
        s = self.find_student()
        if s:
            self.display_students([s])
            self.update_status(f"Showing record for {s.name}")

    def show_highest(self):
        if not self.students:
            messagebox.showinfo("Empty", "No student records.")
            return
        best = max(self.students, key=lambda x: x.percentage())
        self.display_students([best])
        self.tree.tag_configure("highlight", background="#e8f5e8")
        self.tree.get_children()[0] and self.tree.item(self.tree.get_children()[0], tags=("highlight",))

    def show_lowest(self):
        if not self.students:
            messagebox.showinfo("Empty", "No student records.")
            return
        worst = min(self.students, key=lambda x: x.percentage())
        self.display_students([worst])
        self.tree.tag_configure("lowlight", background="#ffebee")
        self.tree.get_children()[0] and self.tree.item(self.tree.get_children()[0], tags=("lowlight",))

    def sort_records(self):
        if not self.students:
            return
        options = {"1": ("Name", lambda s: s.name.lower()),
                   "2": ("ID", lambda s: s.code),
                   "3": ("Percentage", lambda s: s.percentage())}
        
        choice = simpledialog.askstring("Sort Records", 
            "Sort by:\n1. Name\n2. Student ID\n3. Percentage\n\nEnter 1, 2 or 3:")
        if choice not in options:
            messagebox.showerror("Invalid", "Please select 1, 2, or 3")
            return
        
        reverse = messagebox.askyesno("Sort Order", "Descending? (Highest first)")
        field_name, key_func = options[choice]
        sorted_students = sorted(self.students, key=key_func, reverse=reverse)
        self.display_students(sorted_students)
        self.update_status(f"Sorted by {field_name} ({'Descending' if reverse else 'Ascending'})")

    def add_student(self):
        # Same logic as before but with better prompts
        code = simpledialog.askinteger("New Student", "Student ID (1000–9999):", minvalue=1000, maxvalue=9999)
        if not code or any(s.code == code for s in self.students):
            messagebox.showerror("Invalid", "ID already exists or invalid!")
            return

        name = simpledialog.askstring("New Student", "Full Name:")
        if not name or not name.strip():
            return

        def get_mark(prompt, max_val):
            while True:
                val = simpledialog.askinteger("Input Mark", prompt, minvalue=0, maxvalue=max_val)
                if val is not None:
                    return val
                if messagebox.askyesno("Cancel", "Cancel adding student?"):
                    return None

        cw1 = get_mark("Coursework 1 (0–20):", 20)
        if cw1 is None: return
        cw2 = get_mark("Coursework 2 (0–20):", 20)
        if cw2 is None: return
        cw3 = get_mark("Coursework 3 (0–20):", 20)
        if cw3 is None: return
        exam = get_mark("Exam Mark (0–100):", 100)
        if exam is None: return

        new_student = Student(code, name, cw1, cw2, cw3, exam)
        self.students.append(new_student)
        save_students(self.students)
        self.update_status(f"Added student: {name}")
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")

    def update_student(self):
        s = self.find_student()
        if not s: return

        fields = ["Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam Mark"]
        choice = simpledialog.askstring("Update Field", 
            "Select field to update:\n" + "\n".join(f"{i+1}. {f}" for i, f in enumerate(fields)))
        if not choice or not choice.isdigit() or int(choice) not in range(1, 6):
            return
        idx = int(choice) - 1

        if idx == 0:
            new = simpledialog.askstring("Update Name", "New name:", initialvalue=s.name)
            if new: s.name = new.strip()
        elif idx <= 3:
            new = simpledialog.askinteger("Update Mark", f"New Coursework {idx} (0–20):", minvalue=0, maxvalue=20)
            if new is not None: s.cw[idx-1] = new
        else:
            new = simpledialog.askinteger("Update Exam", "New Exam Mark (0–100):", minvalue=0, maxvalue=100)
            if new is not None: s.exam = new

        save_students(self.students)
        self.display_students(self.students)
        messagebox.showinfo("Updated", "Student record updated successfully!")

    def delete_student(self):
        s = self.find_student()
        if not s: return
        if messagebox.askyesno("Confirm Delete", f"Delete {s.name} ({s.code}) permanently?"):
            self.students.remove(s)
            save_students(self.students)
            self.display_students(self.students)
            messagebox.showinfo("Deleted", "Student record has been removed.")


# ====================== Launch App ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()