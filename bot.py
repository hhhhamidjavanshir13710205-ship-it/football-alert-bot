import os
import requests
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/PL/matches"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )

    print("Telegram:", response.status_code)
    print(response.text)


def test_football_api():
    headers = {
        "X-Auth-Token": FOOTBALL_API_TOKEN
    }

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    response = requests.get(
        API_URL,
        headers=headers,
        params={
            "dateFrom": today,
            "dateTo": today
        },
        timeout=30
    )

    print("Football API status:", response.status_code)
    print("Football API response:", response.text[:2000])

    response.raise_for_status()

    data = response.json()

    matches = data.get("matches", [])

    if matches:
        message = (
            "⚽ تست API فوتبال موفق بود!\n\n"
            f"📅 تاریخ: {today}\n"
            f"🏆 Premier League\n"
            f"تعداد بازی امروز: {len(matches)}"
        )
    else:
        message = (
            "⚽ اتصال به API فوتبال موفق بود!\n\n"
            f"📅 تاریخ: {today}\n"
            "امروز در Premier League بازی پیدا نشد."
        )

    send_message(message)


if __name__ == "__main__":
    test_football_api()
