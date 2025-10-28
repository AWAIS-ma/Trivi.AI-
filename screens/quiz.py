import tkinter as tk
from tkinter import messagebox, scrolledtext, Menu
from config import *
from utils import chat, extract_json
from users import load_users, save_users   # if you need them here

class QuizBotGUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.configure(bg=BACKGROUND)

        # quiz state
        self.topic = ""
        self.q_type = "MCQ"
        self.difficulty = "Easy"
        self.total_questions = 0
        self.q_index = 0
        self.user_score = 0
        self.bot_score = 0
        self.current_q = None
        self.expecting_answer = False
        self.asked_questions = set()

        # Top options panel
        self.options_frame = tk.Frame(root, bg=BACKGROUND, pady=14, padx=14)
        self.options_frame.pack(fill="x")

        self.card = tk.Frame(self.options_frame, bg="white", bd=0, relief="flat")
        self.card.pack(padx=10, pady=10, fill="x")
        self.card.configure(highlightbackground=SECONDARY, highlightthickness=1)

        # Header
        tk.Label(self.card, text="⚡ Quiz Setup", font=("Inter", 15, "bold"),
                 bg="white", fg=PRIMARY).grid(row=0, column=0, columnspan=2, pady=(10, 15))

        # Quiz Topic
        tk.Label(self.card, text="Quiz Topic:", font=("Inter", 13, "bold"),
                 bg="white", fg=TEXT_DARK).grid(row=1, column=0, sticky="w", padx=8, pady=8)
        self.topic_entry = tk.Entry(self.card, font=("Inter", 12), bg=ACCENT,
                                    fg=TEXT_DARK, width=30, relief="flat", highlightthickness=1,
                                    highlightbackground=SECONDARY)
        self.topic_entry.grid(row=1, column=1, pady=8, padx=8, sticky="w")
        self.topic_entry.bind("<KeyRelease>", self.check_topic_for_programming)

        # Quiz Type
        tk.Label(self.card, text="Quiz Type:", font=("Inter", 13, "bold"),
                 bg="white", fg=TEXT_DARK).grid(row=2, column=0, sticky="w", padx=8, pady=6)
        self.quiz_type_var = tk.StringVar(value="MCQ")

        radio_style = {"bg": "white", "fg": TEXT_DARK, "font": ("Inter", 11),
                       "selectcolor": SECONDARY, "activebackground": "white",
                       "activeforeground": TEXT_DARK}

        self.mcq_btn = tk.Radiobutton(self.card, text="MCQ", variable=self.quiz_type_var,
                                      value="MCQ", **radio_style)
        self.mcq_btn.grid(row=2, column=1, sticky="w")
        self.tf_btn = tk.Radiobutton(self.card, text="True/False", variable=self.quiz_type_var,
                                     value="True/False", **radio_style)
        self.tf_btn.grid(row=2, column=1, sticky="w", padx=90)
        self.prog_btn = tk.Radiobutton(self.card, text="Programming", variable=self.quiz_type_var,
                                       value="Programming", **radio_style)
        self.riddle_btn = tk.Radiobutton(self.card, text="Riddle", variable=self.quiz_type_var,
                                         value="Riddle", **radio_style)
        self.riddle_btn.grid(row=2, column=1, sticky="w", padx=350)

        # Number of Questions
        tk.Label(self.card, text="Questions:", font=("Inter", 13, "bold"),
                 bg="white", fg=TEXT_DARK).grid(row=3, column=0, sticky="w", padx=8, pady=8)
        self.num_entry = tk.Spinbox(self.card, from_=1, to=30, width=4, bg=ACCENT,
                                    fg=TEXT_DARK, font=("Inter", 12), relief="flat",
                                    highlightthickness=1, highlightbackground=SECONDARY)
        self.num_entry.grid(row=3, column=1, sticky="w", padx=8)

        # Difficulty
        tk.Label(self.card, text="Difficulty:", font=("Inter", 13, "bold"),
                 bg="white", fg=TEXT_DARK).grid(row=4, column=0, sticky="w", padx=8, pady=8)
        self.diff_var = tk.StringVar(value="Easy")
        tk.Radiobutton(self.card, text="Easy", variable=self.diff_var, value="Easy", **radio_style).grid(row=4, column=1, sticky="w")
        tk.Radiobutton(self.card, text="Medium", variable=self.diff_var, value="Medium", **radio_style).grid(row=4, column=1, sticky="w", padx=80)
        tk.Radiobutton(self.card, text="Hard", variable=self.diff_var, value="Hard", **radio_style).grid(row=4, column=1, sticky="w", padx=170)
        tk.Radiobutton(self.card, text="Very Hard", variable=self.diff_var, value="Very Hard", **radio_style).grid(row=4, column=1, sticky="w", padx=260)

        # Start / Back buttons
        start_back = tk.Frame(self.card, bg="white")
        start_back.grid(row=5, column=0, columnspan=2, pady=15)
        self.start_btn = tk.Button(start_back, text="Start Quiz", command=self.start_quiz,
                                   font=("Inter", 13, "bold"), bg=PRIMARY, fg=TEXT_LIGHT,
                                   relief="flat", padx=18, pady=8, bd=0)
        self.start_btn.pack(side="left", padx=6)
        self.back_to_dash_btn = tk.Button(start_back, text="Back to Dashboard",
                                          command=lambda: self.app.show_screen("dashboard"),
                                          font=("Inter", 12), bg=SECONDARY, fg=TEXT_LIGHT,
                                          relief="flat", padx=14, pady=8, bd=0)
        self.back_to_dash_btn.pack(side="left", padx=6)




        # Chat / quiz area
        self.chat_frame = tk.Frame(root, bg=BACKGROUND)
        # Score label
        self.score_label = tk.Label(self.chat_frame, text="Your Score: 0    Agent Score: 0",
                                    font=("Inter", 13, "bold"), bg=BACKGROUND, fg=TEXT_DARK)
        self.score_label.pack(pady=(8, 6))

        # Scrolled chat area
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state="disabled",
                                                  font=("Inter", 12), bg="white", fg=TEXT_DARK, height=16,
                                                  relief="flat", padx=10, pady=10)
        self.chat_area.pack(padx=12, pady=(0,10), fill="both", expand=True)
        self.chat_area.tag_config("user", foreground=TEXT_DARK, background="#e6f2fb", lmargin1=10, lmargin2=10, rmargin=50)
        self.chat_area.tag_config("bot", foreground=TEXT_DARK, background="#f0f9ff", lmargin1=10, lmargin2=10, rmargin=50)
        self.chat_area.tag_config("question", foreground=PRIMARY, font=("Inter", 13, "bold"), lmargin1=10, lmargin2=10)

        # Context menu for chat area
        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="Copy", command=self.copy_selected)
        self.chat_area.bind("<Button-3>", self.show_context_menu)

        # MCQ buttons frame (displayed below chat area)
        self.mcq_buttons_frame = tk.Frame(self.chat_frame, bg=BACKGROUND)
        self.mcq_buttons_frame.pack(padx=8, pady=(0,10), fill="x")

        # Entry + Submit for open-answer and TF
        self.entry = tk.Entry(self.chat_frame, font=("Inter", 12), bg=ACCENT, fg=TEXT_DARK, relief="flat")
        self.entry.pack(padx=12, pady=(0, 10), fill="x")
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.chat_frame, text="Submit Answer", command=self.send_message,
                                     font=("Inter", 12, "bold"), bg=PRIMARY, fg=TEXT_LIGHT,
                                     relief="flat", padx=14, pady=8)
        self.send_button.pack(pady=(0, 10))

        # Quiz nav
        self.quiz_nav_frame = tk.Frame(self.chat_frame, bg=BACKGROUND)
        self.quiz_nav_frame.pack(fill="x", pady=(0, 10))
        tk.Button(self.quiz_nav_frame, text="End Quiz", command=self.end_quiz,
                  font=("Inter", 11), bg=SECONDARY, fg=TEXT_LIGHT, relief="flat", padx=10, pady=6).pack(side=tk.LEFT, padx=8)
        tk.Button(self.quiz_nav_frame, text="Back to Dashboard", command=lambda: self.app.show_screen("dashboard"),
                  font=("Inter", 11), bg=ACCENT, fg=TEXT_LIGHT, relief="flat", padx=10, pady=6).pack(side=tk.RIGHT, padx=8)

        # start with options visible; chat hidden
        # (we do not pack chat_frame here; start_quiz will pack it)

    def check_topic_for_programming(self, event=None):
        topic = self.topic_entry.get().strip().lower()
        if topic in PROGRAMMING_LANGS:
            self.prog_btn.grid(row=1, column=1, sticky="w", padx=220)
        else:
            try:
                self.prog_btn.grid_forget()
            except:
                pass
            if self.quiz_type_var.get() == "Programming":
                self.quiz_type_var.set("MCQ")

    def start_quiz(self):
        topic = self.topic_entry.get().strip()
        if not topic and self.quiz_type_var.get() != "Riddle":
            messagebox.showwarning("Input Required", "Please enter a quiz topic!")
            return
        try:
            total = int(self.num_entry.get())
            if total < 1: raise ValueError()
        except:
            messagebox.showwarning("Invalid", "Enter a valid number of questions")
            return

        self.topic = topic
        self.q_type = self.quiz_type_var.get()
        self.difficulty = self.diff_var.get()
        self.total_questions = total

        self.q_index = 0
        self.user_score = 0
        self.bot_score = 0
        self.current_q = None
        self.expecting_answer = False
        self.asked_questions = set()
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.configure(state="disabled")
        self.update_score_label()

        # hide options, show chat
        self.options_frame.pack_forget()
        self.chat_frame.pack(fill="both", expand=True)

        # ensure entry/button visible initially
        self.entry.pack(padx=12, pady=(0, 10), fill="x")
        self.send_button.pack(pady=(0, 10))

        self.get_question()

    def get_question(self):
        if self.q_index >= self.total_questions:
            self.end_quiz()
            return

        # build prompt depending on type
        if self.q_type == "Programming":
            prompt = f"Generate exactly one short programming quiz question in JSON format only. Keys: question, type, answer. Do not repeat: {list(self.asked_questions)}. Difficulty: {self.difficulty}. Programming Language: {self.topic}."
        elif self.q_type == "Riddle":
            prompt = f"Generate exactly one fun riddle in JSON format only. Keys: question, type, answer. Do not repeat: {list(self.asked_questions)}. Topic: {self.topic}. Difficulty: {self.difficulty}."
        else:
            prompt = f"Generate exactly one quiz question in JSON format only. Keys: question, options, answer, type. Topic: {self.topic}. Difficulty: {self.difficulty}. Type: {self.q_type}. Do not repeat: {list(self.asked_questions)}."

        # show temporary generation hint
        self.show_message("Generating question...", "bot")
        reply = chat([{"role": "system", "content": "You are a quiz master AI."}, {"role": "user", "content": prompt}])

        # remove the "Generating question..." line (last line)
        self.chat_area.configure(state="normal")
        try:
            # delete last inserted line (safe approach)
            self.chat_area.delete("end-2l", tk.END)
        except:
            pass
        self.chat_area.configure(state="disabled")

        if reply.startswith("__ERROR__"):
            self.show_message(f"Error: {reply}", "bot")
            return

        data = extract_json(reply)
        if not data or "question" not in data:
            self.show_message("Invalid question format. Retrying...", "bot")
            self.root.after(800, self.get_question)
            return

        qtext = data["question"].strip()
        if qtext in self.asked_questions:
            # try immediately again
            self.root.after(100, self.get_question)
            return
        self.asked_questions.add(qtext)

        self.current_q = data
        self.q_index += 1
        self.expecting_answer = True

        # show question in chat area
        self.show_message(f"Q{self.q_index}: {qtext}", "question")

        # clear any old mcq buttons
        for widget in self.mcq_buttons_frame.winfo_children():
            widget.destroy()

        # display options text in chat (so visually options appear right under question)
        if "options" in data and self.q_type == "MCQ":
            opts_text = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(data["options"])])
            self.show_message(opts_text, "bot")

            # hide entry and text submit UI (MCQ uses buttons)
            self.entry.pack_forget()
            self.send_button.pack_forget()

            # create buttons — full width and wrapping
            for idx, opt in enumerate(data["options"]):
                btn_text = f"{chr(65+idx)}. {opt}"
                btn = tk.Button(self.mcq_buttons_frame, text=btn_text, font=("Inter", 12),
                                anchor="w", justify="left", wraplength=820,
                                command=lambda ans=opt: self.submit_mcq(ans),
                                relief="flat", padx=10, pady=10, bg="#f4fbff")
                # make the button span full width
                btn.pack(fill="x", pady=6, padx=12)
        else:
            # show entry and send button (for open answer / TF)
            # If options exist for reference, show them as well
            if "options" in data:
                opts_text = "\n".join([f"- {o}" for o in data["options"]])
                self.show_message(opts_text, "bot")

            # ensure input widgets visible
            self.entry.pack(padx=12, pady=(0, 10), fill="x")
            self.send_button.pack(pady=(0, 10))

    def submit_mcq(self, ans):
        if not self.expecting_answer:
            return
        # show selected option as user message (A. text)
        display_text = ans
        # find the option label (A/B/C) by comparing to current_q options
        label = ""
        if self.current_q and "options" in self.current_q:
            for i, o in enumerate(self.current_q["options"]):
                if str(o).strip().lower() == str(ans).strip().lower():
                    label = chr(65+i)
                    break
        self.show_message(f"{label}. {display_text}", "user")

        correct = str(self.current_q.get("answer", "")).strip().lower()
        user_ans = str(ans).strip().lower()

        if user_ans == correct or user_ans == correct.lower():
            self.show_message("Correct!", "bot")
            self.user_score += 1
        else:
            self.show_message(f"Wrong! Correct: {self.current_q.get('answer')}", "bot")
            self.bot_score += 1

        self.expecting_answer = False
        self.update_score_label()
        for widget in self.mcq_buttons_frame.winfo_children():
            widget.destroy()
        self.root.after(900, self.get_question)

    def send_message(self, event=None):
        text = self.entry.get().strip()
        if not text or not self.expecting_answer:
            return
        self.show_message(text, "user")
        self.entry.delete(0, tk.END)

        correct = str(self.current_q.get("answer", "")).strip().lower()
        user_ans = text.lower().strip()

        if user_ans == correct:
            self.show_message("Correct!", "bot")
            self.user_score += 1
        else:
            self.show_message(f"Wrong! Correct: {self.current_q.get('answer')}", "bot")
            self.bot_score += 1

        self.expecting_answer = False
        self.update_score_label()
        self.root.after(900, self.get_question)

    def update_score_label(self):
        self.score_label.config(text=f"Your Score: {self.user_score}    Agent Score: {self.bot_score}")

    def end_quiz(self):
        won = self.user_score > self.bot_score
        if won:
            self.app.update_user_xp(True)
            messagebox.showinfo("Quiz Over", f"You won!\nFinal: You {self.user_score} - AI {self.bot_score}\n+50 XP earned")
        else:
            messagebox.showinfo("Quiz Over", f"You lost!\nFinal: You {self.user_score} - AI {self.bot_score}\nNo XP earned")

        self.chat_frame.pack_forget()
        self.app.show_screen("dashboard")

    def show_message(self, msg, tag):
        # insert message into chat area and autoscroll
        self.chat_area.configure(state="normal")
        if tag == "user":
            self.chat_area.insert(tk.END, msg + "\n", "user")
        elif tag == "question":
            self.chat_area.insert(tk.END, msg + "\n", "question")
        else:
            self.chat_area.insert(tk.END, msg + "\n", "bot")
        self.chat_area.configure(state="disabled")
        self.chat_area.yview(tk.END)

    def copy_selected(self):
        try:
            sel = self.chat_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(sel)
        except:
            pass

    def show_context_menu(self, e):
        try:
            self.menu.tk_popup(e.x_root, e.y_root)
        finally:
            self.menu.grab_release()
