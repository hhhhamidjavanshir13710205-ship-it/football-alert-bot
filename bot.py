import os
import time
import requests
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

COMPETITIONS = {
    "PL": "🏴 Premier League",
    "PD": "🇪🇸 La Liga",
    "SA": "🇮🇹 Serie A",
    "BL1": "🇩🇪 Bundesliga",
    "FL1": "🇫🇷 Ligue 1",
    "DED": "🇳🇱 Eredivisie",
    "PPL": "🇵🇹 Primeira Liga",
    "BSA": "🇧🇷 Brasileirão Série A",
    "CL": "🏆 Champions League",
}


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


def get_today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get_matches(competition, date):
    url = API_URL.format(competition)

    headers = {
        "X-Auth-Token": FOOTBALL_API_TOKEN
    }

    params = {
        "dateFrom": date,
        "dateTo": date
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    print(competition, "API:", response.status_code)

    # اگر محدودیت درخواست خورد
    if response.status_code == 429:

        print("Rate limit reached. Waiting 45 seconds...")

        time.sleep(45)

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        print(
            competition,
            "API after waiting:",
            response.status_code
        )

    if response.status_code != 200:

        print(
            "API Error:",
            response.text[:500]
        )

        return []

    data = response.json()

    return data.get("matches", [])


def main():

    date = get_today()

    print("================================")
    print("FOOTBALL ALERT BOT")
    print("DATE:", date)
    print("================================")

    all_matches = []

    for competition, league_name in COMPETITIONS.items():

        print("Checking:", league_name)

        matches = get_matches(
            competition,
            date
        )

        for match in matches:

            match["league_name"] = league_name

            all_matches.append(match)

    print("TOTAL MATCHES:", len(all_matches))

    # اگر هیچ بازی پیدا نشد
    if not all_matches:

        send_message(
            f"⚽ بازی‌ای برای امروز پیدا نشد.\n\n"
            f"📅 تاریخ: {date}"
        )

        return

    # ساخت پیام
    message = (
        f"⚽ بازی‌های امروز\n"
        f"📅 تاریخ: {date}\n\n"
    )

    for match in all_matches:

        league = match["league_name"]

        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]

        utc_date = match["utcDate"]

        dt = datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )

        time_text = dt.strftime("%H:%M")

        message += (
            f"{league}\n"
            f"⚽ {home} - {away}\n"
            f"🕐 {time_text}\n\n"
        )

    send_message(message)


if __name__ == "__main__":
    main()
