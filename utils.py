import requests, json, re
from config import API_URL, HEADERS, MAX_TOKENS , MODEL

def chat(messages: list) -> str:
    payload = {"model": MODEL, "messages": messages, "max_tokens": MAX_TOKENS}
    try:
        r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"__ERROR__:{e}"

def extract_json(text: str) -> dict | None:
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            pass
    m2 = re.search(r"(\{(?:.|\n)*\})", text, re.DOTALL)
    if m2:
        try:
            return json.loads(m2.group(1))
        except:
            pass
    return None