# -*- coding: utf-8 -*-

import os
import requests
import jdatetime

from datetime import datetime
from zoneinfo import ZoneInfo


# ============================================================
# تنظیمات
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "YOUR_CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv(
    "FOOTBALL_API_TOKEN",
    "YOUR_FOOTBALL_DATA_API_TOKEN"
)

API_BASE = "https://api.football-data.org/v4"
TEHRAN_TZ = ZoneInfo("Asia/Tehran")


# ============================================================
# لیگ‌ها
# فقط ۶ لیگ
# ============================================================

COMPETITIONS = {
    "PL": {
        "name": "لیگ برتر انگلیس",
        "flag": "🏴"
    },

    "PD": {
        "name": "لالیگا",
        "flag": "🇪🇸"
    },

    "SA": {
        "name": "سری آ",
        "flag": "🇮🇹"
    },

    "BL1": {
        "name": "بوندسلیگا",
        "flag": "🇩🇪"
    },

    "FL1": {
        "name": "لیگ ۱ فرانسه",
        "flag": "🇫🇷"
    },

    "CL": {
        "name": "لیگ قهرمانان اروپا",
        "flag": "🇪🇺"
    }
}


# ============================================================
# نام فارسی تیم‌ها
# ============================================================

TEAM_NAMES = {

    # ========================================================
    # England
    # ========================================================

    "Chelsea FC": "چلسی",
    "Brentford FC": "برنتفورد",
    "Arsenal FC": "آرسنال",
    "Liverpool FC": "لیورپول",
    "Manchester City FC": "منچسترسیتی",
    "Manchester United FC": "منچستریونایتد",
    "Tottenham Hotspur FC": "تاتنهام",
    "Newcastle United FC": "نیوکاسل",
    "Aston Villa FC": "استون ویلا",
    "West Ham United FC": "وستهم",
    "Everton FC": "اورتون",
    "Fulham FC": "فولام",
    "Crystal Palace FC": "کریستال پالاس",
    "Brighton & Hove Albion FC": "برایتون",
    "Wolverhampton Wanderers FC": "ولورهمپتون",
    "Nottingham Forest FC": "ناتینگهام فارست",
    "AFC Bournemouth": "بورنموث",
    "Leicester City FC": "لسترسیتی",
    "Southampton FC": "ساوتهمپتون",
    "Ipswich Town": "ایپسویچ",
    "Hull City AFC": "هال سیتی",
    "Coventry City FC": "کاونتری سیتی",

    # ========================================================
    # Spain
    # ========================================================

    "FC Barcelona": "بارسلونا",
    "Real Madrid CF": "رئال مادرید",
    "Atletico Madrid": "اتلتیکومادرید",
    "Athletic Club": "اتلتیک بیلبائو",
    "Real Sociedad de Fútbol": "رئال سوسیداد",
    "Sevilla FC": "سویا",
    "Villarreal CF": "ویارئال",
    "Real Betis Balompié": "رئال بتیس",
    "Valencia CF": "والنسیا",
    "Getafe CF": "ختافه",
    "RC Celta de Vigo": "سلتاویگو",
    "RCD Mallorca": "مایورکا",
    "CA Osasuna": "اوساسونا",
    "Rayo Vallecano de Madrid": "رایو وایکانو",
    "Girona FC": "ژیرونا",
    "Deportivo Alavés": "آلاوس",
    "UD Las Palmas": "لاس پالماس",
    "CD Leganés": "لگانس",
    "RCD Espanyol de Barcelona": "اسپانیول",
    "Elche CF": "الچه",
    "Real Racing Club de Santander": "راسینگ سانتاندر",

    # ========================================================
    # Italy
    # ========================================================

    "FC Internazionale Milano": "اینتر",
    "Inter Milan": "اینتر",
    "AC Milan": "میلان",
    "Juventus FC": "یوونتوس",
    "SSC Napoli": "ناپولی",
    "AS Roma": "رم",
    "SS Lazio": "لاتزیو",
    "Atalanta BC": "آتالانتا",
    "ACF Fiorentina": "فیورنتینا",
    "Bologna FC 1909": "بولونیا",
    "Torino FC": "تورینو",
    "Genoa CFC": "جنوا",
    "Udinese Calcio": "اودینزه",
    "Cagliari Calcio": "کالیاری",
    "Empoli FC": "امپولی",
    "Hellas Verona FC": "هلاس ورونا",
    "US Lecce": "لچه",
    "Parma Calcio 1913": "پارما",
    "Como 1907": "کومو",
    "AC Monza": "مونتزا",
    "US Sassuolo Calcio": "ساسولو",
    "Venezia FC": "ونیزیا",

    # ========================================================
    # Germany
    # ========================================================

    "FC Bayern München": "بایرن مونیخ",
    "FC Bayern Munich": "بایرن مونیخ",
    "Borussia Dortmund": "بوروسیا دورتموند",
    "RB Leipzig": "لایپزیگ",
    "Bayer 04 Leverkusen": "بایرلورکوزن",
    "Eintracht Frankfurt": "آینتراخت فرانکفورت",
    "VfB Stuttgart": "اشتوتگارت",
    "SC Freiburg": "فرایبورگ",
    "1. FSV Mainz 05": "ماینتس",
    "Borussia Mönchengladbach": "مونشن‌گلادباخ",
    "TSG 1899 Hoffenheim": "هوفنهایم",
    "VfL Wolfsburg": "ولفسبورگ",
    "SV Werder Bremen": "وردربرمن",
    "FC Augsburg": "آگزبورگ",
    "1. FC Union Berlin": "یونیون برلین",
    "1. FC Heidenheim 1846": "هایدنهایم",
    "FC St. Pauli 1910": "سن پائولی",
    "Holstein Kiel": "هولشتاین کیل",
    "Hamburger SV": "هامبورگ",
    "1. FC Köln": "کلن",

    # ========================================================
    # France
    # ========================================================

    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
    "Olympique de Marseille": "مارسی",
    "AS Monaco FC": "موناکو",
    "Olympique Lyonnais": "لیون",
    "Lille OSC": "لیل",
    "OGC Nice": "نیس",
    "Stade Rennais FC": "رن",
    "Stade Rennais FC 1901": "رن",
    "RC Strasbourg Alsace": "استراسبورگ",
    "RC Lens": "لانس",
    "FC Nantes": "نانت",
    "Montpellier HSC": "مون‌پلیه",
    "Toulouse FC": "تولوز",
    "Stade Brestois 29": "برست",
    "Le Havre AC": "لو آور",
    "AJ Auxerre": "اوسر",
    "AS Saint-Étienne": "سن‌اتین",
    "Angers SCO": "آنژه",
    "Paris FC": "پاریس اف‌سی",
    "Le Mans FC": "لو مان",
    "FC Lorient": "لوریان",
    "ES Troyes AC": "تروا",

    # ========================================================
    # Champions League
    # ========================================================

    "Galatasaray SK": "گالاتاسرای",
    "Fenerbahçe SK": "فنرباغچه",
    "Olympiacos FC": "المپیاکوس",
    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting CP": "اسپورتینگ",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "Ajax": "آژاکس",
    "AFC Ajax": "آژاکس",
    "PSV": "پی‌اس‌وی",
    "Feyenoord Rotterdam": "فاینورد",
    "Inter Milan": "اینتر",
    "AC Milan": "میلان",
    "Juventus FC": "یوونتوس",
    "FC Internazionale Milano": "اینتر",
    "Real Madrid CF": "رئال مادرید",
    "FC Barcelona": "بارسلونا",
    "Manchester City FC": "منچسترسیتی",
    "Manchester United FC": "منچستریونایتد",
    "Arsenal FC": "آرسنال",
    "Liverpool FC": "لیورپول",
    "Bayern München": "بایرن مونیخ",
    "FC Bayern München": "بایرن مونیخ",
    "Borussia Dortmund": "بوروسیا دورتموند",
    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
    "AS Monaco FC": "موناکو",
    "Atletico Madrid": "اتلتیکومادرید",
    "Bayer 04 Leverkusen": "بایرلورکوزن",
    "RB Leipzig": "لایپزیگ",
}


# ============================================================
# تبدیل نام تیم
# ============================================================

def get_team_name(name):

    if not name:
        return "نامشخص"

    name = " ".join(str(name).split())

    if name in TEAM_NAMES:
        return TEAM_NAMES[name]

    name_lower = name.lower()

    for original, persian in TEAM_NAMES.items():
        if original.lower() == name_lower:
            return persian

    return name


def style_team_name(name):
    return get_team_name(name)


# ============================================================
# تاریخ شمسی
# ============================================================

def get_persian_date():

    now = datetime.now(TEHRAN_TZ)

    jalali = jdatetime.datetime.fromgregorian(
        datetime=now
    )

    months = [
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند"
    ]

    return (
        f"{jalali.day} "
        f"{months[jalali.month - 1]} "
        f"{jalali.year}"
    )


# ============================================================
# تاریخ API
# ============================================================

def get_api_date():

    now = datetime.now(TEHRAN_TZ)

    return now.strftime("%Y-%m-%d")


# ============================================================
# دریافت بازی‌ها
# ============================================================

def fetch_matches(
    competition_code,
    date_from,
    date_to
):

    url = (
        f"{API_BASE}/competitions/"
        f"{competition_code}/matches"
    )

    headers = {
        "X-Auth-Token": FOOTBALL_API_TOKEN,
        "Accept": "application/json"
    }

    params = {
        "dateFrom": date_from,
        "dateTo": date_to
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        if response.status_code != 200:

            print(
                f"خطا در لیگ "
                f"{competition_code}: "
                f"{response.status_code}"
            )

            print(response.text)

            return []

        return response.json().get(
            "matches",
            []
        )

    except requests.RequestException as e:

        print(
            "خطای اتصال:",
            e
        )

        return []


# ============================================================
# جمع‌آوری بازی‌ها
# ============================================================

def collect_matches():

    today = get_api_date()

    all_matches = []

    for code in COMPETITIONS:

        print(
            f"در حال بررسی "
            f"{COMPETITIONS[code]['name']}..."
        )

        matches = fetch_matches(
            code,
            today,
            today
        )

        for match in matches:

            status = match.get(
                "status",
                ""
            )

            if status in [
                "CANCELLED",
                "POSTPONED",
                "SUSPENDED"
            ]:
                continue

            match[
                "_competition_code"
            ] = code

            all_matches.append(match)

    return all_matches


# ============================================================
# تبدیل ساعت به تهران
# ============================================================

def get_match_time(match):

    utc_date = match.get(
        "utcDate"
    )

    if not utc_date:
        return "--:--"

    try:

        dt = datetime.fromisoformat(
            utc_date.replace(
                "Z",
                "+00:00"
            )
        )

        tehran = dt.astimezone(
            TEHRAN_TZ
        )

        return tehran.strftime(
            "%H:%M"
        )

    except Exception:

        return "--:--"


# ============================================================
# طراحی ساعت جدید
# ============================================================

def format_match_time(match):

    time = get_match_time(match)

    return f"⏰ <b>{time}</b>"


# ============================================================
# ساخت پیام
# ============================================================

def build_message(matches):

    grouped = {}

    for match in matches:

        code = match[
            "_competition_code"
        ]

        if code not in grouped:
            grouped[code] = []

        grouped[code].append(match)


    lines = []

    # --------------------------------------------------------
    # هدر
    # --------------------------------------------------------

    lines.append(
        "⚽ <b>بازی‌های امروز</b>"
    )

    lines.append(
        f"📅 {get_persian_date()} 🇮🇷"
    )

    lines.append("")


    # --------------------------------------------------------
    # لیگ‌ها
    # --------------------------------------------------------

    for code, competition in COMPETITIONS.items():

        league_matches = grouped.get(
            code,
            []
        )

        if not league_matches:
            continue

        league_matches.sort(
            key=lambda x: x.get(
                "utcDate",
                ""
            )
        )


        # عنوان لیگ

        lines.append(
            f'{competition["flag"]} '
            f'<b>{competition["name"]}</b>'
        )

        lines.append(
            "━━━━━━━━━━━━━━"
        )


        # ----------------------------------------------------
        # بازی‌ها
        # ----------------------------------------------------

        for match in league_matches:

            home_team = match.get(
                "homeTeam",
                {}
            ).get(
                "name",
                "نامشخص"
            )

            away_team = match.get(
                "awayTeam",
                {}
            ).get(
                "name",
                "نامشخص"
            )


            home = style_team_name(
                home_team
            )

            away = style_team_name(
                away_team
            )


            # بازی

            lines.append(
                f"🏟️ <b>{home}</b>"
            )

            lines.append(
                f"       🆚"
            )

            lines.append(
                f"🏟️ <b>{away}</b>"
            )


            # ساعت با طراحی جدید

            lines.append(
                f"      {format_match_time(match)}"
            )

            lines.append("")


        lines.append(
            "━━━━━━━━━━━━━━━━"
        )

        lines.append("")


    # حذف خطوط خالی آخر

    while lines and not lines[-1].strip():
        lines.pop()


    return "\n".join(lines)


# ============================================================
# ارسال به تلگرام
# ============================================================

def send_message(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:

        response = requests.post(
            url,
            data=data,
            timeout=20
        )

        if response.status_code != 200:

            print(
                "خطای تلگرام:",
                response.text
            )

            return False


        result = response.json()

        if not result.get("ok"):

            print(
                "خطای تلگرام:",
                result
            )

            return False


        print(
            "✅ پیام با موفقیت ارسال شد."
        )

        return True


    except requests.RequestException as e:

        print(
            "خطای اتصال به تلگرام:",
            e
        )

        return False


# ============================================================
# اجرای اصلی
# ============================================================

def main():

    print(
        "⏳ در حال دریافت بازی‌های امروز..."
    )

    matches = collect_matches()


    if not matches:

        message = (
            "⚽ <b>بازی‌های امروز</b>\n"
            f"📅 {get_persian_date()} 🇮🇷\n\n"
            "❌ بازی‌ای برای امروز "
            "در ۶ لیگ پیدا نشد."
        )

    else:

        message = build_message(
            matches
        )


    print()
    print(message)
    print()


    send_message(
        message
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
