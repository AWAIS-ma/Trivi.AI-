API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4.1"
API_KEY = "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"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
MAX_TOKENS = 300
USER_FILE = "assets/user_data.json"

PROGRAMMING_LANGS = [
    "python", "java", "c++", "c", "c#", "javascript",
    "html", "css", "php", "ruby", "go", "swift",
    "kotlin", "typescript", "sql", "r"
]

PRIMARY = "#064232"
SECONDARY = "#568F87"
ACCENT = "#F5BABB"
BACKGROUND = "#FFF5F2"
TEXT_DARK = "#064232"
TEXT_LIGHT = "#ffffff"