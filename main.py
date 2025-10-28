import tkinter as tk
from config import BACKGROUND
from screens.login import LoginScreen
from screens.signup import SignupScreen
from screens.forgot import ForgotScreen
from screens.dashboard import DashboardScreen
from screens.quiz import QuizBotGUI
from screens.top_users import TopUsersScreen

class TriviAIApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("trivi.AI")
        self.root.geometry("880x720")
        self.root.configure(bg=BACKGROUND)

        self.current_user = None
        self.screens = {}
        self.show_screen("login")

    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_screen(self, name: str):
        self.clear_window()
        if name == "login":
            self.screens[name] = LoginScreen(self.root, self)
        elif name == "signup":
            self.screens[name] = SignupScreen(self.root, self)
        elif name == "forgot":
            self.screens[name] = ForgotScreen(self.root, self)
        elif name == "dashboard":
            self.screens[name] = DashboardScreen(self.root, self)
            self.screens[name].show()
        elif name == "top_users":
            self.screens[name] = TopUsersScreen(self.root, self)
            self.screens[name].show()
        elif name == "quiz":
            QuizBotGUI(self.root, self)

    def update_user_xp(self, won: bool):
        from users import load_users, save_users
        if not self.current_user:
            return
        users = load_users()
        email = self.current_user["email"]
        if email in users and won:
            users[email]["xp"] += 50
            self.current_user["xp"] = users[email]["xp"]
            save_users(users)

if __name__ == "__main__":
    root = tk.Tk()
    TriviAIApp(root)
    root.mainloop()