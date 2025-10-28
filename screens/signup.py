import tkinter as tk
from tkinter import messagebox
from config import BACKGROUND, PRIMARY, ACCENT, TEXT_DARK, TEXT_LIGHT
from users import load_users, save_users

class SignupScreen:
    def __init__(self, root, app):
        self.root, self.app = root, app
        self.frame = tk.Frame(root, bg=BACKGROUND, pady=30, padx=30)
        self.build()

    def build(self):
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Sign Up - trivi.AI", font=("Inter", 22, "bold"),
                 bg=BACKGROUND, fg=PRIMARY).pack(pady=10)
        form = tk.Frame(self.frame, bg=BACKGROUND)
        form.pack()

        self.name_entry = tk.Entry(form, width=36, font=("Inter", 12), bg=ACCENT, fg=TEXT_DARK, relief="flat")
        self.email_entry = tk.Entry(form, width=36, font=("Inter", 12), bg=ACCENT, fg=TEXT_DARK, relief="flat")
        self.pwd_entry = tk.Entry(form, width=36, show="*", font=("Inter", 12), bg=ACCENT, fg=TEXT_DARK, relief="flat")
        self.pwd2_entry = tk.Entry(form, width=36, show="*", font=("Inter", 12), bg=ACCENT, fg=TEXT_DARK, relief="flat")

        for i, (lbl, widget) in enumerate([("Name:", self.name_entry),
                                           ("Email:", self.email_entry),
                                           ("Password:", self.pwd_entry),
                                           ("Re-enter Password:", self.pwd2_entry)]):
            tk.Label(form, text=lbl, bg=BACKGROUND, fg=TEXT_DARK,
                     font=("Inter", 12)).grid(row=2 * i, column=0, sticky="w", pady=(6, 0))
            widget.grid(row=2 * i + 1, column=0, pady=6)

        btn_frame = tk.Frame(self.frame, bg=BACKGROUND)
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="Register", bg=PRIMARY, fg=TEXT_LIGHT,
                  font=("Inter", 12, "bold"), command=self.attempt_signup,
                  relief="flat", padx=18, pady=8).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Back", bg=PRIMARY, fg=TEXT_LIGHT,
                  font=("Inter", 12), command=lambda: self.app.show_screen("login"),
                  relief="flat", padx=18, pady=8).pack(side="left", padx=6)

    def attempt_signup(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        pwd2 = self.pwd2_entry.get().strip()
        users = load_users()
        if email in users:
            messagebox.showerror("Error", "Account already exists")
            return
        if not name or not email or not pwd:
            messagebox.showerror("Error", "All fields required")
            return
        if pwd != pwd2:
            messagebox.showerror("Error", "Passwords do not match")
            return
        users[email] = {"name": name, "password": pwd, "xp": 0}
        save_users(users)
        messagebox.showinfo("Success", "Account created! Please login.")
        self.app.show_screen("login")