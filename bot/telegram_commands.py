import json
import os
import requests

STATE_PATH = os.path.join(os.path.dirname(__file__), "..", "state", "positions.json")
OFFSET_PATH = os.path.join(os.path.dirname(__file__), "..", "state", "telegram_offset.json")

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path, data):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def send(token, chat_id, msg):
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": msg},
        timeout=10,
    )

def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    offset_data = load_json(OFFSET_PATH, {"offset": None})
    params = {}
    if offset_data.get("offset"):
        params["offset"] = offset_data["offset"]

    resp = requests.get(
        f"https://api.telegram.org/bot{token}/getUpdates", params=params, timeout=15
    ).json()

    state = load_json(STATE_PATH, {"enabled": True, "position": None, "paper_balance": None})

    for update in resp.get("result", []):
        offset_data["offset"] = update["update_id"] + 1
        msg = update.get("message", {})
        text = msg.get("text", "").strip().lower()
        chat_id = msg.get("chat", {}).get("id")
        if not chat_id:
            continue

        if text == "/start":
            state["enabled"] = True
            send(token, chat_id, "Bot enabled. Trading resumed.")
        elif text == "/stop":
            state["enabled"] = False
            send(token, chat_id, "Bot disabled. Trading paused.")
        elif text == "/status":
            pos = state.get("position")
            bal = state.get("paper_balance")
            pos_txt = f"{pos['side']} @ {pos['entry']:.2f}" if pos else "none"
            enabled_txt = "ON" if state.get("enabled", True) else "OFF"
            send(token, chat_id, f"Bot: {enabled_txt}\nPosition: {pos_txt}\nPaper balance: {bal}")
        elif text == "/help":
            send(
                token,
                chat_id,
                "/start - resume trading\n/stop - pause trading\n/status - show status\n/help - this list",
            )

    save_json(OFFSET_PATH, offset_data)
    save_json(STATE_PATH, state)

if __name__ == "__main__":
    main()
