import os
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

# نام کوتاه فارسی تیم‌ها
TEAM_NAMES = {
    "Real Madrid": "رئال مادرید",
    "Barcelona": "بارسلونا",
    "Espanyol": "اسپانیول",
    "Atletico Madrid": "اتلتیکو مادرید",
    "Sevilla": "سویا",
    "Valencia": "والنسیا",
    "Villarreal": "ویارئال",
    "Athletic Club": "اتلتیک بیلبائو",
    "Real Betis": "رئال بتیس",
    "Getafe": "ختافه",
    "Girona": "ژیرونا",
    "Celta": "سلتاویگو",
    "Osasuna": "اوساسونا",
    "Rayo Vallecano": "رایو وایکانو",
    "Mallorca": "مایورکا",
    "Alaves": "آلاوس",
    "Real Sociedad": "رئال سوسیداد",
    "Las Palmas": "لاس پالماس",
    "Leganes": "لگانس",

    "Manchester City": "منچسترسیتی",
    "Manchester United": "منچستریونایتد",
    "Liverpool": "لیورپول",
    "Arsenal": "آرسنال",
    "Chelsea": "چلسی",
    "Tottenham": "تاتنهام",
    "Newcastle United": "نیوکاسل",
    "Aston Villa": "استون ویلا",
    "West Ham United": "وستهم",
    "Everton": "اورتون",
    "Brighton & Hove Albion": "برایتون",
    "Crystal Palace": "کریستال پالاس",
    "Fulham": "فولام",
    "Wolverhampton Wanderers": "ولورهمپتون",
    "Brentford": "برنتفورد",
    "Nottingham Forest": "ناتینگهام فارست",
    "Bournemouth": "بورنموث",
    "Leicester City": "لسترسیتی",
    "Ipswich Town": "ایپسویچ",

    "Inter Milan": "اینتر",
    "Inter": "اینتر",
    "AC Milan": "آث میلان",
    "Juventus": "یوونتوس",
    "Napoli": "ناپولی",
    "Roma": "رم",
    "Lazio": "لاتزیو",
    "Atalanta": "آتالانتا",
    "Fiorentina": "فیورنتینا",
    "Torino": "تورینو",
    "Bologna": "بولونیا",
    "Genoa": "جنوا",
    "Udinese": "اودینزه",
    "Monza": "مونزا",
    "Parma": "پارما",

    "Bayern Munich": "بایرن مونیخ",
    "Borussia Dortmund": "دورتموند",
    "RB Leipzig": "لایپزیگ",
    "Bayer Leverkusen": "بایرلورکوزن",
    "Eintracht Frankfurt": "آینتراخت فرانکفورت",
    "VfB Stuttgart": "اشتوتگارت",
    "Wolfsburg": "وولفسبورگ",
    "Borussia Monchengladbach": "مونشن گلادباخ",
    "Werder Bremen": "وردربرمن",
    "Mainz 05": "ماینتس",
    "Hoffenheim": "هوفنهایم",
    "Freiburg": "فرایبورگ",

    "Paris Saint-Germain": "پاری‌سن‌ژرمن",
    "Marseille": "مارسی",
    "Monaco": "موناکو",
    "Lyon": "لیون",
    "Lille": "لیل",
    "Nice": "نیس",
    "Rennes": "رن",
    "Nantes": "نانت",
    "Toulouse": "تولوز",
    "Lens": "لانس",

    "Ajax": "آژاکس",
    "PSV": "آیندهوون",
    "Feyenoord": "فاینورد",
    "AZ": "آلکمار",
    "Twente": "توئنته",

    "Benfica": "بنفیکا",
    "Porto": "پورتو",
    "Sporting CP": "اسپورتینگ",
    "Braga": "براگا",
    "Vitoria SC": "ویتوریا گیمارش",

    "Flamengo": "فلامینگو",
    "Palmeiras": "پالمیراس",
    "Botafogo": "بوتافوگو",
    "Fluminense": "فلومیننزه",
    "Corinthians": "کورینتیانس",
    "Sao Paulo": "سائوپائولو",
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

def get_team_name(name):
    return TEAM_NAMES.get(name, name)

def get_matches(competition, date):
    url = API_URL.format(competition)

    headers = {
        "X-Auth-Token": FOOTBALL_API_TOKEN
    }

    response = requests.get(
        url,
        headers=headers,
        params={
            "dateFrom": date,
            "dateTo": date
        },
        timeout=30
    )

    print(competition, "API:", response.status_code)

    if response.status_code != 200:
        print(response.text[:500])
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

    if not all_matches:

        send_message(
            f"⚽ بازی‌ای برای امروز پیدا نشد.\n\n"
            f"📅 تاریخ: {date}"
        )

        return

    message = (
        f"⚽ بازی‌های امروز\n"
        f"📅 تاریخ: {date}\n\n"
    )

    for match in all_matches:

        league = match["league_name"]

        home = get_team_name(
            match["homeTeam"]["name"]
        )

        away = get_team_name(
            match["awayTeam"]["name"]
        )

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
