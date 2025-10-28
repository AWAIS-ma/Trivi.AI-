import tkinter as tk
from tkinter import messagebox
from config import BACKGROUND, PRIMARY, ACCENT, TEXT_DARK, TEXT_LIGHT
from users import load_users, save_users

class ForgotScreen:
    def __init__(self, root, app):
        self.root, self.app = root, app
        self.frame = tk.Frame(root, bg=BACKGROUND, pady=30, padx=30)
        self.build()

    def build(self):
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Reset Password - trivi.AI",
                 font=("Inter", 20, "bold"), bg=BACKGROUND, fg=PRIMARY).pack(pady=8)
        form = tk.Frame(self.frame, bg=BACKGROUND)
        form.pack()

        self.email_entry = tk.Entry(form, width=36, font=("Inter", 12), bg=ACCENT, fg=TEXT_DARK, relief="flat")
        self.pwd_entry = tk.Entry(form, width=36, show="*", font=("Inter", 12), bg=ACCENT, fg=TEXT_DARK, relief="flat")

        for i, (lbl, widget) in enumerate([("Email:", self.email_entry),
                                           ("New Password:", self.pwd_entry)]):
            tk.Label(form, text=lbl, bg=BACKGROUND, fg=TEXT_DARK,
                     font=("Inter", 12)).grid(row=2 * i, column=0, sticky="w", pady=(6, 0))
            widget.grid(row=2 * i + 1, column=0, pady=6)

        btn_frame = tk.Frame(self.frame, bg=BACKGROUND)
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="Reset", bg=PRIMARY, fg=TEXT_LIGHT,
                  font=("Inter", 12, "bold"), command=self.reset_password,
                  relief="flat", padx=18, pady=8).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Back", bg=PRIMARY, fg=TEXT_LIGHT,
                  font=("Inter", 12), command=lambda: self.app.show_screen("login"),
                  relief="flat", padx=18, pady=8).pack(side="left", padx=6)

    def reset_password(self):
        email, new_pwd = self.email_entry.get().strip(), self.pwd_entry.get().strip()
        users = load_users()
        if email not in users:
            messagebox.showerror("Error", "Email not found")
            return
        users[email]["password"] = new_pwd
        save_users(users)
        messagebox.showinfo("Success", "Password reset successfully!")
        self.app.show_screen("login")