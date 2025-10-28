import tkinter as tk
from config import BACKGROUND, PRIMARY, SECONDARY, ACCENT, TEXT_DARK, TEXT_LIGHT
from users import get_top_users


class TopUsersScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(root, bg=BACKGROUND)
        self._build_ui()

    def show(self):
        self.frame.pack(expand=True, fill="both")

    def _build_ui(self):
        # card size
        self.card_w, self.card_h = 500, 600
        self.r = 25
        margin = 40

        # canvas
        self.canvas = tk.Canvas(
            self.frame,
            bg=BACKGROUND,
            highlightthickness=0,
            width=self.card_w + margin * 2,
            height=self.card_h + margin * 2,
        )
        self.canvas.pack(expand=True, anchor="center")

        # card coords
        self.card_x1, self.card_y1 = margin, margin
        self.card_x2, self.card_y2 = self.card_w + margin, self.card_h + margin

        # center
        self.cx = (self.card_x1 + self.card_x2) // 2

        # draw card bg
        self._draw_card()

        # Title
        self.canvas.create_text(
            self.cx,
            self.card_y1 + 40,
            text="🏆 Top Users",
            font=("Inter", 28, "bold"),
            fill=PRIMARY,
        )

        # Get users
        users = get_top_users(10)

        # Display in rows
        start_y = self.card_y1 + 90
        row_height = 42

        for user in users:
            y = start_y + (user["rank"] - 1) * row_height

            # rank circle
            self.canvas.create_oval(
                self.card_x1 + 20,
                y - 15,
                self.card_x1 + 50,
                y + 15,
                fill=SECONDARY,
                outline="",
            )
            self.canvas.create_text(
                self.card_x1 + 35,
                y,
                text=str(user["rank"]),
                font=("Inter", 12, "bold"),
                fill=TEXT_LIGHT,
            )

            # user name
            self.canvas.create_text(
                self.card_x1 + 120,
                y,
                text=user["name"],
                font=("Inter", 14, "bold"),
                fill=TEXT_DARK,
                anchor="w",
            )

            # XP badge (right aligned)
            self.canvas.create_roundrect(
                self.card_x2 - 110,
                y - 15,
                self.card_x2 - 20,
                y + 15,
                radius=12,
                fill=ACCENT,
                outline="",
            )
            self.canvas.create_text(
                self.card_x2 - 65,
                y,
                text=f'{user["xp"]} XP',
                font=("Inter", 12, "bold"),
                fill=TEXT_DARK,
            )

        # Return button (bottom center)
        self._round_button(
            "⬅ Return",
            PRIMARY,
            TEXT_LIGHT,
            self.cx,
            self.card_y2 - 40,
            lambda: self.app.show_screen("dashboard"),
        )

    def _draw_card(self):
        self.canvas.create_roundrect(
            self.card_x1,
            self.card_y1,
            self.card_x2,
            self.card_y2,
            radius=self.r,
            fill="#ffffff",
            outline=SECONDARY,
            width=2,
        )

    def _round_button(self, text, bg, fg, x, y, cmd):
        w, h, rx = 200, 44, 18
        btn = self.canvas.create_roundrect(
            x - w // 2, y - h // 2, x + w // 2, y + h // 2, radius=rx, fill=bg, outline=""
        )
        lbl = self.canvas.create_text(
            x, y, text=text, font=("Inter", 13, "bold"), fill=fg
        )
        for item in (btn, lbl):
            self.canvas.tag_bind(item, "<Button-1>", lambda e: cmd())
            self.canvas.tag_bind(item, "<Enter>", lambda e: self.canvas.itemconfig(btn, fill=SECONDARY))
            self.canvas.tag_bind(item, "<Leave>", lambda e: self.canvas.itemconfig(btn, fill=bg))


# Keep using your create_roundrect monkey-patch
def _create_roundrect(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius,
        y1,
        x2 - radius,
        y1,
        x2,
        y1,
        x2,
        y1 + radius,
        x2,
        y2 - radius,
        x2,
        y2,
        x2 - radius,
        y2,
        x1 + radius,
        y2,
        x1,
        y2,
        x1,
        y2 - radius,
        x1,
        y1 + radius,
        x1,
        y1,
    ]
    return self.create_polygon(points, smooth=True, **kwargs)


tk.Canvas.create_roundrect = _create_roundrect
