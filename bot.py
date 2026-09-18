import os
import time
import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

COMPETITIONS = {
    "PL": "🏴 لیگ برتر انگلیس",
    "PD": "🇪🇸 لالیگا",
    "SA": "🇮🇹 سری آ",
    "BL1": "🇩🇪 بوندسلیگا",
    "FL1": "🇫🇷 لیگ ۱ فرانسه",
    "DED": "🇳🇱 اردیویسه",
    "PPL": "🇵🇹 لیگ پرتغال",
    "BSA": "🇧🇷 سری آ برزیل",
    "CL": "🏆 لیگ قهرمانان اروپا",
}

TEAM_NAMES = {
    # England
    "Brentford FC": "برنتفورد",
    "Chelsea FC": "چلسی",
    "Arsenal FC": "آرسنال",
    "Liverpool FC": "لیورپول",
    "Manchester City FC": "منچسترسیتی",
    "Manchester United FC": "منچستریونایتد",
    "Tottenham Hotspur FC": "تاتنهام",
    "Newcastle United FC": "نیوکاسل",
    "Aston Villa FC": "استون ویلا",
    "Everton FC": "اورتون",
    "West Ham United FC": "وستهم",
    "Fulham FC": "فولام",
    "Crystal Palace FC": "کریستال پالاس",
    "Brighton & Hove Albion FC": "برایتون",
    "Wolverhampton Wanderers FC": "ولورهمپتون",
    "Nottingham Forest FC": "ناتینگهام فارست",
    "AFC Bournemouth": "بورنموث",
    "Burnley FC": "برنلی",
    "Leeds United FC": "لیدز",
    "Sunderland AFC": "ساندرلند",

    # Spain
    "Real Madrid CF": "رئال مادرید",
    "FC Barcelona": "بارسلونا",
    "RCD Espanyol de Barcelona": "اسپانیول",
    "Elche CF": "الچه",
    "Club Atlético de Madrid": "اتلتیکو مادرید",
    "Sevilla FC": "سویا",
    "Valencia CF": "والنسیا",
    "Villarreal CF": "ویارئال",
    "Athletic Club": "اتلتیک بیلبائو",
    "Real Betis Balompié": "رئال بتیس",
    "Getafe CF": "ختافه",
    "Girona FC": "ژیرونا",
    "RC Celta de Vigo": "سلتاویگو",
    "CA Osasuna": "اوساسونا",
    "Rayo Vallecano de Madrid": "رایو وایکانو",
    "RCD Mallorca": "مایورکا",
    "Deportivo Alavés": "آلاوس",
    "Real Sociedad de Fútbol": "رئال سوسیداد",

    # Italy
    "FC Internazionale Milano": "اینتر",
    "AC Milan": "آث میلان",
    "Juventus FC": "یوونتوس",
    "SSC Napoli": "ناپولی",
    "AS Roma": "رم",
    "SS Lazio": "لاتزیو",
    "Atalanta BC": "آتالانتا",
    "ACF Fiorentina": "فیورنتینا",
    "Torino FC": "تورینو",
    "Bologna FC 1909": "بولونیا",
    "Genoa CFC": "جنوا",
    "Udinese Calcio": "اودینزه",
    "Parma Calcio 1913": "پارما",
    "US Lecce": "لچه",
    "Cagliari Calcio": "کالیاری",
    "Como 1907": "کومو",

    # Germany
    "FC Bayern München": "بایرن مونیخ",
    "Borussia Dortmund": "دورتموند",
    "RB Leipzig": "لایپزیگ",
    "Bayer 04 Leverkusen": "بایرلورکوزن",
    "Eintracht Frankfurt": "آینتراخت فرانکفورت",
    "VfB Stuttgart": "اشتوتگارت",
    "VfL Wolfsburg": "وولفسبورگ",
    "Borussia Mönchengladbach": "مونشن گلادباخ",
    "SV Werder Bremen": "وردربرمن",
    "1. FSV Mainz 05": "ماینتس",
    "TSG 1899 Hoffenheim": "هوفنهایم",
    "Sport-Club Freiburg": "فرایبورگ",
    "FC Augsburg": "آگسبورگ",
    "1. FC Union Berlin": "یونیون برلین",
    "1. FC Köln": "کلن",
    "Hamburger SV": "هامبورگ",

    # France
    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
    "Olympique de Marseille": "مارسی",
    "AS Monaco FC": "موناکو",
    "Olympique Lyonnais": "لیون",
    "Lille OSC": "لیل",
    "OGC Nice": "نیس",
    "Stade Rennais FC 1901": "رن",
    "FC Nantes": "نانت",
    "Toulouse FC": "تولوز",
    "RC Lens": "لانس",
    "RC Strasbourg Alsace": "استراسبورگ",

    # Netherlands
    "AFC Ajax": "آژاکس",
    "PSV": "آیندهوون",
    "Feyenoord Rotterdam": "فاینورد",
    "AZ": "آلکمار",
    "FC Twente '65": "توئنته",
    "FC Utrecht": "اوترخت",

    # Portugal
    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "SC Braga": "براگا",
    "Vitória SC": "ویتوریا گیمارش",

    # Brazil
    "CR Flamengo": "فلامینگو",
    "SE Palmeiras": "پالمیراس",
    "Botafogo FR": "بوتافوگو",
    "Fluminense FC": "فلومیننزه",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
}

COUNTRY_FLAGS = {
    "PL": "🇬🇧",
    "PD": "🇪🇸",
    "SA": "🇮🇹",
    "BL1": "🇩🇪",
    "FL1": "🇫🇷",
    "DED": "🇳🇱",
    "PPL": "🇵🇹",
    "BSA": "🇧🇷",
    "CL": "🇪🇺",
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
    return datetime.now(
        ZoneInfo("Asia/Tehran")
    ).strftime("%Y-%m-%d")


def get_team_name(name):
    return TEAM_NAMES.get(name, name)


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
        print(response.text[:500])
        return []

    data = response.json()

    return data.get("matches", [])


def main():
    date = get_today()

    print("================================")
    print("FOOTBALL ALERT BOT")
    print("IRAN DATE:", date)
    print("================================")

    all_matches = []

    for competition, league_name in COMPETITIONS.items():

        print("Checking:", league_name)

        matches = get_matches(
            competition,
            date
        )

        for match in matches:
            match["league_code"] = competition
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

    iran_timezone = ZoneInfo("Asia/Tehran")

    for match in all_matches:

        competition = match["league_code"]
        league = match["league_name"]

        home_original = match["homeTeam"]["name"]
        away_original = match["awayTeam"]["name"]

        home = get_team_name(home_original)
        away = get_team_name(away_original)

        flag = COUNTRY_FLAGS.get(
            competition,
            "⚽"
        )

        utc_date = match["utcDate"]

        dt = datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )

        iran_time = dt.astimezone(
            iran_timezone
        )

        time_text = iran_time.strftime("%H:%M")

        message += (
            f"{league}\n"
            f"⚽ {flag} {home} - {flag} {away}\n"
            f"🕐 {time_text}\n\n"
        )

    send_message(message)


if __name__ == "__main__":
    main()
