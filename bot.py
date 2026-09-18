import os
import time
import requests
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================================================
# تنظیمات
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

TEHRAN = ZoneInfo("Asia/Tehran")


# =========================================================
# لیگ‌ها
# =========================================================

COMPETITIONS = {
    "PL": {
        "name": "لیگ برتر انگلیس",
        "flag": "🏴",
    },
    "PD": {
        "name": "لالیگا",
        "flag": "🇪🇸",
    },
    "SA": {
        "name": "سری آ",
        "flag": "🇮🇹",
    },
    "BL1": {
        "name": "بوندسلیگا",
        "flag": "🇩🇪",
    },
    "FL1": {
        "name": "لیگ ۱ فرانسه",
        "flag": "🇫🇷",
    },
    "DED": {
        "name": "اردیویسه",
        "flag": "🇳🇱",
    },
    "PPL": {
        "name": "لیگ برتر پرتغال",
        "flag": "🇵🇹",
    },
    "BSA": {
        "name": "سری آ برزیل",
        "flag": "🇧🇷",
    },
    "CL": {
        "name": "لیگ قهرمانان اروپا",
        "flag": "🇪🇺",
    },
}


# =========================================================
# نام تیم‌ها
# =========================================================

TEAM_NAMES = {

    # -------------------------
    # England
    # -------------------------

    "Arsenal FC": "آرسنال",
    "Aston Villa FC": "استون ویلا",
    "AFC Bournemouth": "بورنموث",
    "Brentford FC": "برنتفورد",
    "Brighton & Hove Albion": "برایتون",
    "Chelsea FC": "چلسی",
    "Crystal Palace FC": "کریستال پالاس",
    "Everton FC": "اورتون",
    "Fulham FC": "فولام",
    "Leeds United FC": "لیدز یونایتد",
    "Liverpool FC": "لیورپول",
    "Manchester City FC": "منچسترسیتی",
    "Manchester United FC": "منچستریونایتد",
    "Newcastle United FC": "نیوکاسل",
    "Nottingham Forest FC": "ناتینگهام فارست",
    "Sunderland AFC": "ساندرلند",
    "Tottenham Hotspur FC": "تاتنهام",
    "West Ham United FC": "وستهم",
    "Wolverhampton Wanderers FC": "ولورهمپتون",

    # -------------------------
    # Spain
    # -------------------------

    "Real Madrid CF": "رئال مادرید",
    "FC Barcelona": "بارسلونا",
    "Club Atlético de Madrid": "اتلتیکومادرید",
    "Club Atletico de Madrid": "اتلتیکومادرید",
    "Athletic Club": "اتلتیک بیلبائو",
    "Real Sociedad de Fútbol": "رئال سوسیداد",
    "Real Betis Balompié": "رئال بتیس",
    "Real Betis": "رئال بتیس",
    "Sevilla FC": "سویا",
    "Villarreal CF": "ویارئال",
    "Valencia CF": "والنسیا",
    "Girona FC": "ژیرونا",
    "RCD Espanyol de Barcelona": "اسپانیول",
    "RCD Espanyol": "اسپانیول",
    "Elche CF": "الچه",

    # -------------------------
    # Italy
    # -------------------------

    "Inter": "اینتر",
    "FC Internazionale Milano": "اینتر",
    "AC Milan": "آث میلان",
    "Juventus FC": "یوونتوس",
    "SSC Napoli": "ناپولی",
    "AS Roma": "رم",
    "SS Lazio": "لاتزیو",
    "Atalanta BC": "آتالانتا",
    "ACF Fiorentina": "فیورنتینا",
    "AC Monza": "مونزا",
    "US Sassuolo Calcio": "ساسولو",

    # -------------------------
    # Germany
    # -------------------------

    "FC Bayern München": "بایرن مونیخ",
    "FC Bayern Munich": "بایرن مونیخ",
    "Borussia Dortmund": "بوروسیا دورتموند",
    "Bayer 04 Leverkusen": "بایرلورکوزن",
    "RB Leipzig": "لایپزیگ",
    "Eintracht Frankfurt": "آینتراخت فرانکفورت",
    "VfB Stuttgart": "اشتوتگارت",
    "Union Berlin": "یونیون برلین",
    "1. FC Union Berlin": "یونیون برلین",

    # -------------------------
    # France
    # -------------------------

    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
    "Olympique de Marseille": "مارسی",
    "Olympique Lyonnais": "لیون",
    "AS Monaco FC": "موناکو",
    "LOSC Lille": "لیل",
    "OGC Nice": "نیس",
    "Racing Club de Lens": "لنس",
    "RC Lens": "لنس",

    # -------------------------
    # Netherlands
    # -------------------------

    "Ajax": "آژاکس",
    "PSV": "پی‌اس‌وی",
    "PSV Eindhoven": "پی‌اس‌وی آیندهوون",
    "Feyenoord": "فاینورد",
    "FC Utrecht": "اوترخت",
    "FC Groningen": "گرونینگن",
    "PEC Zwolle": "زووله",

    # -------------------------
    # Portugal
    # -------------------------

    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting CP": "اسپورتینگ",
    "SC Braga": "براگا",

    # -------------------------
    # Brazil
    # -------------------------

    "Flamengo": "فلامینگو",
    "Palmeiras": "پالمیراس",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
    "Santos FC": "سانتوس",
}


# =========================================================
# پرچم تیم
# =========================================================

TEAM_FLAGS = {

    # England
    "Arsenal FC": "🇬🇧",
    "Aston Villa FC": "🇬🇧",
    "AFC Bournemouth": "🇬🇧",
    "Brentford FC": "🇬🇧",
    "Brighton & Hove Albion": "🇬🇧",
    "Chelsea FC": "🇬🇧",
    "Crystal Palace FC": "🇬🇧",
    "Everton FC": "🇬🇧",
    "Fulham FC": "🇬🇧",
    "Leeds United FC": "🇬🇧",
    "Liverpool FC": "🇬🇧",
    "Manchester City FC": "🇬🇧",
    "Manchester United FC": "🇬🇧",
    "Newcastle United FC": "🇬🇧",
    "Nottingham Forest FC": "🇬🇧",
    "Sunderland AFC": "🇬🇧",
    "Tottenham Hotspur FC": "🇬🇧",
    "West Ham United FC": "🇬🇧",
    "Wolverhampton Wanderers FC": "🇬🇧",

    # Spain
    "Real Madrid CF": "🇪🇸",
    "FC Barcelona": "🇪🇸",
    "Club Atlético de Madrid": "🇪🇸",
    "Club Atletico de Madrid": "🇪🇸",
    "Athletic Club": "🇪🇸",
    "Real Sociedad de Fútbol": "🇪🇸",
    "Real Betis Balompié": "🇪🇸",
    "Real Betis": "🇪🇸",
    "Sevilla FC": "🇪🇸",
    "Villarreal CF": "🇪🇸",
    "Valencia CF": "🇪🇸",
    "Girona FC": "🇪🇸",
    "RCD Espanyol de Barcelona": "🇪🇸",
    "RCD Espanyol": "🇪🇸",
    "Elche CF": "🇪🇸",

    # Italy
    "Inter": "🇮🇹",
    "FC Internazionale Milano": "🇮🇹",
    "AC Milan": "🇮🇹",
    "Juventus FC": "🇮🇹",
    "SSC Napoli": "🇮🇹",
    "AS Roma": "🇮🇹",
    "SS Lazio": "🇮🇹",
    "Atalanta BC": "🇮🇹",
    "ACF Fiorentina": "🇮🇹",
    "AC Monza": "🇮🇹",
    "US Sassuolo Calcio": "🇮🇹",

    # Germany
    "FC Bayern München": "🇩🇪",
    "FC Bayern Munich": "🇩🇪",
    "Borussia Dortmund": "🇩🇪",
    "Bayer 04 Leverkusen": "🇩🇪",
    "RB Leipzig": "🇩🇪",
    "Eintracht Frankfurt": "🇩🇪",
    "VfB Stuttgart": "🇩🇪",
    "Union Berlin": "🇩🇪",
    "1. FC Union Berlin": "🇩🇪",

    # France
    "Paris Saint-Germain FC": "🇫🇷",
    "Olympique de Marseille": "🇫🇷",
    "Olympique Lyonnais": "🇫🇷",
    "AS Monaco FC": "🇫🇷",
    "LOSC Lille": "🇫🇷",
    "OGC Nice": "🇫🇷",
    "Racing Club de Lens": "🇫🇷",
    "RC Lens": "🇫🇷",

    # Netherlands
    "Ajax": "🇳🇱",
    "PSV": "🇳🇱",
    "PSV Eindhoven": "🇳🇱",
    "Feyenoord": "🇳🇱",
    "FC Utrecht": "🇳🇱",
    "FC Groningen": "🇳🇱",
    "PEC Zwolle": "🇳🇱",

    # Portugal
    "SL Benfica": "🇵🇹",
    "FC Porto": "🇵🇹",
    "Sporting CP": "🇵🇹",
    "SC Braga": "🇵🇹",

    # Brazil
    "Flamengo": "🇧🇷",
    "Palmeiras": "🇧🇷",
    "Corinthians": "🇧🇷",
    "São Paulo FC": "🇧🇷",
    "Santos FC": "🇧🇷",
}


# =========================================================
# توابع
# =========================================================

def get_today():
    """
    تاریخ امروز به وقت تهران
    """
    return datetime.now(TEHRAN).date()


def get_team_name(team):
    """
    تبدیل نام انگلیسی تیم به نام فارسی
    """
    if not team:
        return "نامشخص"

    name = team.get("name", "").strip()

    return TEAM_NAMES.get(name, name)


def get_team_flag(team):
    """
    گرفتن پرچم کشور تیم
    """
    if not team:
        return "🌍"

    name = team.get("name", "").strip()

    return TEAM_FLAGS.get(name, "🌍")


def get_match_time(utc_date):
    """
    تبدیل زمان UTC به وقت تهران
    و خروجی با اعداد انگلیسی
    """

    if not utc_date:
        return "--:--"

    try:
        dt = datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )

        tehran_time = dt.astimezone(TEHRAN)

        return tehran_time.strftime("%H:%M")

    except Exception:
        return "--:--"


def get_match_datetime(utc_date):
    """
    برای مرتب‌سازی مسابقات
    """

    try:
        return datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )

    except Exception:
        return datetime.max


# =========================================================
# دریافت مسابقات
# =========================================================

def fetch_matches(competition_code, date_obj):

    date_string = date_obj.strftime("%Y-%m-%d")

    url = API_URL.format(
        competition_code
    )

    params = {
        "dateFrom": date_string,
        "dateTo": date_string,
    }

    headers = {
        "X-Auth-Token": FOOTBALL_API_TOKEN
    }

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30,
            )

            # موفق
            if response.status_code == 200:

                data = response.json()

                return data.get(
                    "matches",
                    []
                )

            # محدودیت API
            if response.status_code == 429:

                print(
                    f"محدودیت API برای {competition_code}"
                )

                time.sleep(45)

                continue

            print(
                f"خطای API {competition_code}: "
                f"{response.status_code}"
            )

        except requests.RequestException as error:

            print(
                f"خطای اتصال {competition_code}: "
                f"{error}"
            )

        if attempt < 2:
            time.sleep(5)

    return []


# =========================================================
# جمع‌آوری مسابقات
# =========================================================

def collect_matches(today):

    matches_by_league = {}

    for competition_code, league_info in COMPETITIONS.items():

        print(
            f"دریافت مسابقات {competition_code}..."
        )

        matches = fetch_matches(
            competition_code,
            today
        )

        valid_matches = []

        for match in matches:

            status = match.get(
                "status",
                ""
            )

            # بازی‌های لغوشده را حذف کن
            if status in (
                "CANCELLED",
                "POSTPONED"
            ):
                continue

            home = match.get(
                "homeTeam",
                {}
            )

            away = match.get(
                "awayTeam",
                {}
            )

            if not home.get("name"):
                continue

            if not away.get("name"):
                continue

            valid_matches.append(match)

        # مرتب‌سازی بر اساس ساعت
        valid_matches.sort(
            key=lambda match: get_match_datetime(
                match.get("utcDate")
            )
        )

        if valid_matches:
            matches_by_league[
                competition_code
            ] = valid_matches

    return matches_by_league


# =========================================================
# ساخت پیام
# =========================================================

def build_message(
    matches_by_league,
    today
):

    date_string = today.strftime(
        "%Y-%m-%d"
    )

    lines = [
        "⚽ بازی‌های امروز",
        f"📅 تاریخ: {date_string}",
        "",
    ]

    total_matches = 0

    for competition_code, league_info in COMPETITIONS.items():

        matches = matches_by_league.get(
            competition_code,
            []
        )

        if not matches:
            continue

        league_name = league_info["name"]
        league_flag = league_info["flag"]

        # نام لیگ
        lines.append(
            f"{league_flag} {league_name}"
        )

        for match in matches:

            home_team = match.get(
                "homeTeam",
                {}
            )

            away_team = match.get(
                "awayTeam",
                {}
            )

            home_name = get_team_name(
                home_team
            )

            away_name = get_team_name(
                away_team
            )

            home_flag = get_team_flag(
                home_team
            )

            away_flag = get_team_flag(
                away_team
            )

            game_time = get_match_time(
                match.get("utcDate")
            )

            lines.append(
                f"⚽ {home_flag} {home_name} - "
                f"{away_flag} {away_name}"
            )

            lines.append(
                f"🕐 {game_time}"
            )

            lines.append("")

            total_matches += 1

        # فاصله بین لیگ‌ها
        lines.append("")

    if total_matches == 0:

        return (
            "⚽ بازی‌های امروز\n"
            f"📅 تاریخ: {date_string}\n\n"
            "❌ امروز مسابقه‌ای پیدا نشد."
        )

    return "\n".join(lines).rstrip()


# =========================================================
# ارسال به تلگرام
# =========================================================

def send_message(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": message,
    }

    response = requests.post(
        url,
        data=data,
        timeout=30,
    )

    if not response.ok:

        raise RuntimeError(
            "خطا در ارسال پیام به تلگرام:\n"
            f"{response.text}"
        )

    return response.json()


# =========================================================
# Main
# =========================================================

def main():

    # بررسی تنظیمات
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN تنظیم نشده است."
        )

    if not CHAT_ID:
        raise RuntimeError(
            "CHAT_ID تنظیم نشده است."
        )

    if not FOOTBALL_API_TOKEN:
        raise RuntimeError(
            "FOOTBALL_API_TOKEN تنظیم نشده است."
        )

    today = get_today()

    print(
        f"تاریخ: {today}"
    )

    # دریافت مسابقات
    matches_by_league = collect_matches(
        today
    )

    # ساخت پیام
    message = build_message(
        matches_by_league,
        today
    )

    print("\n" + "=" * 50)
    print(message)
    print("=" * 50 + "\n")

    # ارسال
    send_message(message)

    print(
        "✅ پیام با موفقیت ارسال شد."
    )


# =========================================================
# اجرا
# =========================================================

if __name__ == "__main__":
    main()
