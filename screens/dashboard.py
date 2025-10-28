import tkinter as tk
from config import BACKGROUND, PRIMARY, SECONDARY, ACCENT, TEXT_DARK, TEXT_LIGHT

class DashboardScreen:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(root, bg=BACKGROUND)
        self._build_ui()

    def show(self):
        self.frame.pack(expand=True, fill="both")

    def _build_ui(self):
        # card size
        self.card_w, self.card_h = 440, 500
        self.r = 25
        margin = 60  

        # canvas size
        self.canvas = tk.Canvas(
            self.frame,
            bg=BACKGROUND,
            highlightthickness=0,
            width=self.card_w + margin*2,
            height=self.card_h + margin*2
        )
        self.canvas.pack(expand=True, anchor="center")

        # card coordinates
        self.card_x1, self.card_y1 = margin, margin
        self.card_x2, self.card_y2 = self.card_w + margin, self.card_h + margin

        # card center
        self.cx = (self.card_x1 + self.card_x2) // 2
        self.cy = (self.card_y1 + self.card_y2) // 2

        self._draw_background()
        self._draw_card()

        # Welcome text
        self.canvas.create_text(
            self.cx, self.card_y1 + 55,
            text=f"✨ Welcome, {self.app.current_user['name']}! ✨",
            font=("Inter", 26, "bold"),
            fill=PRIMARY
        )

        # XP and Level badges
        xp = self.app.current_user["xp"]
        level = max(1, min(xp // 100, 10))
        self._badge("XP", xp, self.cx - 110, self.card_y1 + 150)
        self._badge("Level", level, self.cx + 110, self.card_y1 + 150)

        # Buttons
        self._round_button("🚀 Start Quizzing", PRIMARY, TEXT_LIGHT,
                           self.cx, self.card_y1 + 280,
                           lambda: self.app.show_screen("quiz"))
        self._round_button("🏆 Top Users", SECONDARY, TEXT_LIGHT,
                           self.cx, self.card_y1 + 350,
                           lambda: self.app.show_screen("top_users"))
        self._round_button("🔒 Logout", ACCENT, TEXT_LIGHT,
                           self.cx, self.card_y1 + 420,
                           lambda: self.app.show_screen("login"))

    def _draw_background(self):
        # decorative circles
        self.canvas.create_oval(self.cx-250, self.cy-250, self.cx-50, self.cy-50,
                                fill=PRIMARY, outline="", stipple="gray50")
        self.canvas.create_oval(self.cx+50, self.cy+50, self.cx+250, self.cy+250,
                                fill=ACCENT, outline="", stipple="gray50")

    def _draw_card(self):
        # Shadow
        self.canvas.create_roundrect(
            self.card_x1+6, self.card_y1+6,
            self.card_x2+6, self.card_y2+6,
            radius=self.r, fill="#000000", stipple="gray25"
        )
        # Main card
        self.canvas.create_roundrect(
            self.card_x1, self.card_y1,
            self.card_x2, self.card_y2,
            radius=self.r, fill="#ffffff", outline=SECONDARY, width=2
        )

    def _badge(self, title, value, x, y):
        r = 55
        # outer glow
        self.canvas.create_oval(x-r-4, y-r-4, x+r+4, y+r+4, fill=PRIMARY, outline="")
        # main circle
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=ACCENT, outline="")
        # glossy highlight (fixed - no invalid alpha hex!)
        self.canvas.create_oval(x-r+10, y-r+10, x+r-20, y-r+25,
                                fill="#ffffff", outline="", stipple="gray50")
        # texts
        self.canvas.create_text(x, y-8, text=str(value),
                                font=("Inter", 22, "bold"), fill=TEXT_LIGHT)
        self.canvas.create_text(x, y+20, text=title,
                                font=("Inter", 12, "bold"), fill=TEXT_LIGHT)

    def _round_button(self, text, bg, fg, x, y, cmd):
        w, h, rx = 220, 50, 22
        btn = self.canvas.create_roundrect(x-w//2, y-h//2, x+w//2, y+h//2,
                                           radius=rx, fill=bg, outline="")
        lbl = self.canvas.create_text(x, y, text=text, font=("Inter", 14, "bold"), fill=fg)

        def on_enter(e):
            self.canvas.itemconfig(btn, fill=SECONDARY)

        def on_leave(e):
            self.canvas.itemconfig(btn, fill=bg)

        for item in (btn, lbl):
            self.canvas.tag_bind(item, "<Button-1>", lambda e: cmd())
            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)

# Helper: rounded rectangle
def _create_roundrect(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1+radius, y1, x2-radius, y1,
        x2, y1, x2, y1+radius,
        x2, y2-radius, x2, y2,
        x2-radius, y2, x1+radius, y2,
        x1, y2, x1, y2-radius,
        x1, y1+radius, x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

# attach to tk.Canvas
tk.Canvas.create_roundrect = _create_roundrect
