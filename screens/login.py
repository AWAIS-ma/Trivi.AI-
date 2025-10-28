import tkinter as tk
from tkinter import messagebox
from config import BACKGROUND, PRIMARY, ACCENT, TEXT_DARK, TEXT_LIGHT
from users import load_users

class LoginScreen:
    def __init__(self, root, app):
        self.root, self.app = root, app
        self.frame = tk.Frame(root, bg=BACKGROUND, pady=30, padx=30)
        self.build()

    def build(self):
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Welcome to trivi.AI", font=("Inter", 28, "bold"),
                 bg=BACKGROUND, fg=PRIMARY).pack(pady=10)
        container = tk.Frame(self.frame, bg=BACKGROUND)
        container.pack(pady=10)

        tk.Label(container, text="Email:", bg=BACKGROUND, fg=TEXT_DARK,
                 font=("Inter", 12)).grid(row=0, column=0, sticky="w", pady=(6, 0))
        self.email = tk.Entry(container, width=36, font=("Inter", 12),
                              bg=ACCENT, fg=TEXT_DARK, relief="flat")
        self.email.grid(row=1, column=0, pady=6)

        tk.Label(container, text="Password:", bg=BACKGROUND, fg=TEXT_DARK,
                 font=("Inter", 12)).grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.pwd = tk.Entry(container, width=36, show="*", font=("Inter", 12),
                            bg=ACCENT, fg=TEXT_DARK, relief="flat")
        self.pwd.grid(row=3, column=0, pady=6)

        btn_frame = tk.Frame(self.frame, bg=BACKGROUND)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Login", bg=PRIMARY, fg=TEXT_LIGHT,
                  font=("Inter", 12, "bold"), command=self.attempt_login,
                  relief="flat", padx=20, pady=8).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Sign Up", bg=PRIMARY, fg=TEXT_LIGHT,
                  font=("Inter", 12), command=lambda: self.app.show_screen("signup"),
                  relief="flat", padx=18, pady=8).pack(side="left", padx=8)
        tk.Button(self.frame, text="Forgot Password?", bg=BACKGROUND, fg=TEXT_DARK,
                  font=("Inter", 10), command=lambda: self.app.show_screen("forgot"),
                  relief="flat").pack()

    def attempt_login(self):
        email, pwd = self.email.get().strip(), self.pwd.get().strip()
        users = load_users()
        if email in users and users[email]["password"] == pwd:
            self.app.current_user = {"email": email, **users[email]}
            self.app.show_screen("dashboard")
        else:
            messagebox.showerror("Error", "Invalid email or password")