import json, os
from config import USER_FILE

def load_users() -> dict:
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_users(users: dict):
    os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def get_top_users(limit: int = 10) -> list[dict]:
    """
    Return the top <limit> users sorted by XP (descending).
    Each entry is a dict with at least the keys:
        {'rank': int, 'id': str, 'name': str, 'xp': int}
    If the file is empty or no XP field exists, those users are ignored.
    """
    raw = load_users()
    scored = []

    for user_id, data in raw.items():
        # Support both 'xp' and 'XP' keys (case-insensitive)
        xp = data.get("xp") or data.get("XP") or 0
        scored.append({
            "id": str(user_id),
            "name": data.get("name", user_id),
            "xp": int(xp)
        })

    # Sort descending by XP
    scored.sort(key=lambda u: u["xp"], reverse=True)

    # Add rank and slice
    for idx, user in enumerate(scored[:limit], start=1):
        user["rank"] = idx

    return scored[:limit]
