import tkinter as tk
from tkinter import messagebox
import random
import os

# Basic user data handling (saving and loading users)
def save_user(username, password):
    with open("users.txt", "a") as f:
        f.write(f"{username},{password}\n")

def load_users():
    users = {}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                username, password = line.strip().split(",")
                users[username] = password
    return users

# Questions for each quiz
quizzes = {
    "DSA": [
        ("What does DSA stand for?", ["Data Science and Analysis", "Data Structures and Algorithms", "Data Storage and Analysis", "Dynamic System Analysis"],  "Data Structures and Algorithms"),
        ( "Which of these is a linear data structure?", ["Tree", "Graph", "Array", "Hash Table"], "Array"),
        ( "What is the time complexity of binary search?", ["O(1)", "O(log n)", "O(n)", "O(n^2)"],   "O(log n)"),
        ( "Which data structure uses LIFO principle?", ["Queue", "Stack", "Array", "Linked List"],  "Stack" ),
        ("Which algorithm is used to solve the shortest path problem?", ["DFS", "BFS", "Dijkstra's Algorithm", "Merge Sort"],  "Dijkstra's Algorithm"),
    ],
    "DBMS": [
       ("What does DBMS stand for?",  ["Database Management System", "Data Backup Management System", "Dynamic Base Management System", "Direct Base Management System"], "Database Management System" ),
        ( "Which of the following is a type of database?",  ["Flat File", "Hierarchical", "Relational", "All of the above"],  "All of the above" ),
        ( "What is SQL?",  ["Structured Query Language", "System Query Language", "Standard Query Language", "Structured Query Loop"], "Structured Query Language"),
        ( "Which one of these is used for defining relationships in DBMS?",  ["Foreign Key", "Primary Key", "Unique Key", "All of the above"],"Foreign Key" ),
       ("Which of the following is not a DBMS?",  ["MySQL", "PostgreSQL", "SQLite", "Excel"],  "Excel"),
    ],
    "Python": [
         ( "Which of the following is a valid Python variable name?",  ["1variable", "_variable", "@variable", "$variable"], "_variable" ),
         ( "Which of the following is used for comments in Python?", ["//", "#", "/* */", "--"],  "#" ),
         ( "Which data type is used to store decimal numbers?", ["int", "float", "str", "bool"], "float" ),
         ( "Which of the following is a Python library for data analysis?",  ["NumPy", "Matplotlib", "Pandas", "All of the above"], "Pandas"  ),
         ( "What is the output of 3 + 2 * 2 in Python?", ["10", "7", "8", "5"], "7" ),
       
    ]
}

# Main application class
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")
        self.username = ""
        self.user_answers = []
        
        self.start_page()
    
    def start_page(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Start Page Options
        tk.Label(self.root, text="Quiz Application", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def register(self):
        def save_and_back():
            username = entry_username.get()
            password = entry_password.get()
            if username and password:
                save_user(username, password)
                messagebox.showinfo("Success", "Registration Successful")
                self.start_page()
            else:
                messagebox.showwarning("Error", "Please enter both username and password")
        
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Register", font=("Helvetica", 16)).pack(pady=20)
        tk.Label(self.root, text="Username").pack()
        entry_username = tk.Entry(self.root)
        entry_username.pack()
        tk.Label(self.root, text="Password").pack()
        entry_password = tk.Entry(self.root, show="*")
        entry_password.pack()
        tk.Button(self.root, text="Register", command=save_and_back).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.start_page).pack()

    def login(self):
        def verify_login():
            username = entry_username.get()
            password = entry_password.get()
            users = load_users()
            if users.get(username) == password:
                self.username = username
                messagebox.showinfo("Success", "Login Successful")
                self.quiz_selection()
            else:
                messagebox.showwarning("Error", "Invalid Username or Password")

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Helvetica", 16)).pack(pady=20)
        tk.Label(self.root, text="Username").pack()
        entry_username = tk.Entry(self.root)
        entry_username.pack()
        tk.Label(self.root, text="Password").pack()
        entry_password = tk.Entry(self.root, show="*")
        entry_password.pack()
        tk.Button(self.root, text="Login", command=verify_login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.start_page).pack()

    def quiz_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select a Quiz", font=("Helvetica", 16)).pack(pady=20)
        for quiz in quizzes.keys():
            tk.Button(self.root, text=quiz, command=lambda q=quiz: self.start_quiz(q)).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.start_page).pack(pady=10)

    def start_quiz(self, subject):
        self.current_subject = subject
        self.questions = quizzes[subject]
        self.current_question_index = 0
        self.correct_answers = 0
        self.user_answers = []  # Reset previous answers
        self.show_question()

    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display question number and question
        question, options, correct_answer = self.questions[self.current_question_index]
        question_number = self.current_question_index + 1
        tk.Label(self.root, text=f"Q{question_number}: {question}", font=("Helvetica", 14)).pack(pady=20)

        # Create a frame to center the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Set a fixed width for all buttons
        button_width = 30  # Adjust this to suit your needs
        
        # Display numbered options in a grid to center them
        for idx, option in enumerate(options):
            tk.Button(button_frame, text=f"{idx+1}. {option}", width=button_width, command=lambda o=option: self.check_answer(o)).grid(row=idx, column=0, pady=5)

    def check_answer(self, selected_option):
        question, options, correct_answer = self.questions[self.current_question_index]

        # Save user answer and move to the next question
        self.user_answers.append((question, options, selected_option, correct_answer))
        if selected_option == correct_answer:
            self.correct_answers += 1

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Quiz Completed!", font=("Helvetica", 16)).pack(pady=20)
        tk.Label(self.root, text=f"Correct Answers: {self.correct_answers}/{len(self.questions)}", font=("Helvetica", 14)).pack(pady=10)

        # Show incorrect answers
        for question, options, user_answer, correct_answer in self.user_answers:
            question_number = self.user_answers.index((question, options, user_answer, correct_answer)) + 1
            if user_answer != correct_answer:
                tk.Label(self.root, text=f"Q{question_number}: {question}", font=("Helvetica", 12)).pack(pady=5)
                for idx, option in enumerate(options):
                    color = "green" if option == correct_answer else "red"
                    tk.Label(self.root, text=f"{idx+1}. {option}", fg=color).pack(pady=2)
                tk.Label(self.root, text=f"Your Answer: {user_answer}", fg="red").pack(pady=5)

        tk.Button(self.root, text="Back to Quiz Selection", command=self.quiz_selection).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.start_page).pack(pady=5)

# Initialize the app
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
