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

    # --------------------------------------------------------
    # England
    # --------------------------------------------------------

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
    "Ipswich Town FC": "ایپسویچ",
    "Ipswich Town": "ایپسویچ",
    "Hull City AFC": "هال سیتی",
    "Coventry City FC": "کاونتری سیتی",

    # --------------------------------------------------------
    # Spain
    # --------------------------------------------------------

    "FC Barcelona": "بارسلونا",
    "Real Madrid CF": "رئال مادرید",
    "Atletico Madrid": "اتلتیکومادرید",
    "Club Atlético de Madrid": "اتلتیکومادرید",
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

    # --------------------------------------------------------
    # Italy
    # --------------------------------------------------------

    "FC Internazionale Milano": "اینتر",
    "Inter Milan": "اینتر",
    "Inter": "اینتر",

    "AC Milan": "میلان",
    "Milan": "میلان",

    "Juventus FC": "یوونتوس",
    "Juventus": "یوونتوس",

    "SSC Napoli": "ناپولی",
    "Napoli": "ناپولی",

    "AS Roma": "رم",
    "Roma": "رم",

    "SS Lazio": "لاتزیو",
    "Lazio": "لاتزیو",

    "Atalanta BC": "آتالانتا",
    "Atalanta": "آتالانتا",

    "ACF Fiorentina": "فیورنتینا",
    "Fiorentina": "فیورنتینا",

    "Bologna FC 1909": "بولونیا",
    "Bologna": "بولونیا",

    "Torino FC": "تورینو",
    "Torino": "تورینو",

    "Genoa CFC": "جنوا",
    "Genoa": "جنوا",

    "Udinese Calcio": "اودینزه",
    "Udinese": "اودینزه",

    "Cagliari Calcio": "کالیاری",
    "Cagliari": "کالیاری",

    "Empoli FC": "امپولی",
    "Empoli": "امپولی",

    "Hellas Verona FC": "هلاس ورونا",
    "Hellas Verona": "هلاس ورونا",

    "US Lecce": "لچه",
    "Lecce": "لچه",

    "Parma Calcio 1913": "پارما",
    "Parma": "پارما",

    "Como 1907": "کومو",
    "Como": "کومو",

    "AC Monza": "مونتزا",
    "Monza": "مونتزا",

    "US Sassuolo Calcio": "ساسولو",
    "Sassuolo": "ساسولو",

    "Venezia FC": "ونیزیا",
    "Venezia": "ونیزیا",

    # --------------------------------------------------------
    # Germany
    # --------------------------------------------------------

    "FC Bayern München": "بایرن مونیخ",
    "FC Bayern Munich": "بایرن مونیخ",
    "Bayern München": "بایرن مونیخ",
    "Bayern Munich": "بایرن مونیخ",

    "Borussia Dortmund": "بوروسیا دورتموند",
    "Dortmund": "بوروسیا دورتموند",

    "RB Leipzig": "لایپزیگ",
    "Leipzig": "لایپزیگ",

    "Bayer 04 Leverkusen": "بایرلورکوزن",
    "Bayer Leverkusen": "بایرلورکوزن",

    "Eintracht Frankfurt": "آینتراخت فرانکفورت",

    "VfB Stuttgart": "اشتوتگارت",
    "Stuttgart": "اشتوتگارت",

    "SC Freiburg": "فرایبورگ",
    "Freiburg": "فرایبورگ",

    "1. FSV Mainz 05": "ماینتس",
    "Mainz 05": "ماینتس",

    "Borussia Mönchengladbach": "مونشن‌گلادباخ",
    "Borussia Monchengladbach": "مونشن‌گلادباخ",

    "TSG 1899 Hoffenheim": "هوفنهایم",
    "Hoffenheim": "هوفنهایم",

    "VfL Wolfsburg": "ولفسبورگ",
    "Wolfsburg": "ولفسبورگ",

    "SV Werder Bremen": "وردربرمن",
    "Werder Bremen": "وردربرمن",

    "FC Augsburg": "آگزبورگ",
    "Augsburg": "آگزبورگ",

    "1. FC Union Berlin": "یونیون برلین",
    "Union Berlin": "یونیون برلین",

    "1. FC Heidenheim 1846": "هایدنهایم",
    "Heidenheim": "هایدنهایم",

    "FC St. Pauli 1910": "سن پائولی",
    "St. Pauli": "سن پائولی",

    "Holstein Kiel": "هولشتاین کیل",
    "Hamburger SV": "هامبورگ",

    "1. FC Köln": "کلن",
    "FC Köln": "کلن",

    # --------------------------------------------------------
    # France
    # --------------------------------------------------------

    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
    "Paris Saint-Germain": "پاری‌سن‌ژرمن",
    "PSG": "پاری‌سن‌ژرمن",

    "Olympique de Marseille": "مارسی",
    "Olympique Marseille": "مارسی",
    "Marseille": "مارسی",

    "AS Monaco FC": "موناکو",
    "AS Monaco": "موناکو",
    "Monaco": "موناکو",

    "Olympique Lyonnais": "لیون",
    "Olympique Lyon": "لیون",
    "Lyon": "لیون",

    "Lille OSC": "لیل",
    "Lille": "لیل",

    "OGC Nice": "نیس",
    "Nice": "نیس",

    "Stade Rennais FC": "رن",
    "Stade Rennais FC 1901": "رن",
    "Stade Rennais": "رن",
    "Rennes": "رن",

    "RC Strasbourg Alsace": "استراسبورگ",
    "Strasbourg": "استراسبورگ",

    "RC Lens": "لانس",
    "Lens": "لانس",

    "FC Nantes": "نانت",
    "Nantes": "نانت",

    "Montpellier HSC": "مون‌پلیه",
    "Montpellier": "مون‌پلیه",

    "Toulouse FC": "تولوز",
    "Toulouse": "تولوز",

    "Stade Brestois 29": "برست",
    "Brest": "برست",

    "Le Havre AC": "لو آور",
    "Le Havre": "لو آور",

    "AJ Auxerre": "اوسر",
    "Auxerre": "اوسر",

    "AS Saint-Étienne": "سن‌اتین",
    "Saint-Étienne": "سن‌اتین",

    "Angers SCO": "آنژه",
    "Angers": "آنژه",

    "Paris FC": "پاریس اف‌سی",
    "Le Mans FC": "لو مان",
    "FC Lorient": "لوریان",
    "ES Troyes AC": "تروا",

    # --------------------------------------------------------
    # Champions League
    # --------------------------------------------------------

    "Galatasaray SK": "گالاتاسرای",
    "Galatasaray": "گالاتاسرای",

    "Fenerbahçe SK": "فنرباغچه",
    "Fenerbahce": "فنرباغچه",

    "Olympiacos FC": "المپیاکوس",
    "Olympiacos": "المپیاکوس",

    "SL Benfica": "بنفیکا",
    "Benfica": "بنفیکا",

    "FC Porto": "پورتو",
    "Porto": "پورتو",

    "Sporting CP": "اسپورتینگ",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "Sporting CP Lisbon": "اسپورتینگ",

    "Ajax": "آژاکس",
    "AFC Ajax": "آژاکس",

    "PSV": "پی‌اس‌وی",
    "PSV Eindhoven": "پی‌اس‌وی",

    "Feyenoord Rotterdam": "فاینورد",
    "Feyenoord": "فاینورد",

    "Shakhtar Donetsk": "شاختار دونتسک",
    "FC Shakhtar Donetsk": "شاختار دونتسک",

    "Club Brugge KV": "کلوب بروژ",
    "Club Brugge": "کلوب بروژ",

    "Celtic FC": "سلتیک",
    "Celtic": "سلتیک",

    "Rangers FC": "رنجرز",
    "Rangers": "رنجرز",

    "Red Bull Salzburg": "سالزبورگ",
    "FC Salzburg": "سالزبورگ"
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
# تاریخ میلادی برای API
# ============================================================

def get_api_date():

    now = datetime.now(TEHRAN_TZ)

    return now.strftime("%Y-%m-%d")


# ============================================================
# دریافت بازی‌های یک لیگ
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
                f"خطا در لیگ {competition_code}: "
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
# جمع‌آوری تمام بازی‌ها
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

            match["_competition_code"] = code

            all_matches.append(match)

    return all_matches


# ============================================================
# تبدیل زمان UTC به تهران
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
# ساخت عنوان لیگ وسط کادر
# ============================================================

def make_league_header(
    flag,
    league_name
):

    return (
        f"━━━━━━━━ {flag} "
        f"<b>{league_name}</b> "
        f"{flag} ━━━━━━━━"
    )


# ============================================================
# ساخت پیام نهایی
# ============================================================

def build_message(matches):

    grouped = {}

    for match in matches:

        code = match[
            "_competition_code"
        ]

        if code not in grouped:
            grouped[code] = []

        grouped[code].append(
            match
        )

    lines = []

    # عنوان اصلی
    lines.append(
        "⚽ <b>بازی‌های امروز</b>"
    )

    lines.append(
        f"📅 {get_persian_date()} 🇮🇷"
    )

    lines.append("")

    # لیگ‌ها
    for code, competition in COMPETITIONS.items():

        league_matches = grouped.get(
            code,
            []
        )

        if not league_matches:
            continue

        # مرتب‌سازی بر اساس زمان
        league_matches.sort(
            key=lambda x: x.get(
                "utcDate",
                ""
            )
        )

        # عنوان لیگ وسط کادر
        lines.append(
            make_league_header(
                competition["flag"],
                competition["name"]
            )
        )

        lines.append("")

        # بازی‌ها
        for match in league_matches:

            home_team = (
                match.get(
                    "homeTeam",
                    {}
                ).get(
                    "name",
                    "نامشخص"
                )
            )

            away_team = (
                match.get(
                    "awayTeam",
                    {}
                ).get(
                    "name",
                    "نامشخص"
                )
            )

            home = get_team_name(
                home_team
            )

            away = get_team_name(
                away_team
            )

            match_time = get_match_time(
                match
            )

            lines.append(
                f"🏟️ <b>{home}</b>"
                f"    ⏰ <b>{match_time}</b>"
                f"    <b>{away}</b>"
            )

            lines.append("")

        # خط پایان لیگ
        lines.append(
            "━━━━━━━━━━━━━━━━"
        )

        lines.append("")

    # حذف خطوط خالی انتهایی
    while (
        lines
        and not lines[-1].strip()
    ):
        lines.pop()

    return "\n".join(lines)


# ============================================================
# ارسال پیام به تلگرام
# ============================================================

def send_message(message):

    url = (
        "https://api.telegram.org/"
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
        "⏳ در حال دریافت "
        "بازی‌های امروز..."
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

    send_message(message)


# ============================================================
# شروع برنامه
# ============================================================

if __name__ == "__main__":
    main()
