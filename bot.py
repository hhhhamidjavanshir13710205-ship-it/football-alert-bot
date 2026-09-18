import os
import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


# =========================================================
# تنظیمات
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "YOUR_CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv(
    "FOOTBALL_API_TOKEN",
    "YOUR_FOOTBALL_DATA_API_TOKEN"
)

TEHRAN_TZ = ZoneInfo("Asia/Tehran")

API_BASE = "https://api.football-data.org/v4"


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
        "name": "لیگ پرتغال",
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
# نام فارسی تیم‌ها
# =========================================================

TEAM_NAMES = {

    # ---------------- England ----------------

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

    # ---------------- Spain ----------------

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

    # ---------------- Italy ----------------

    "FC Internazionale Milano": "اینتر",
    "AC Milan": "آث میلان",
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

    # ---------------- Germany ----------------

    "FC Bayern München": "بایرن مونیخ",
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

    # ---------------- France ----------------

    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
    "Olympique de Marseille": "مارسی",
    "AS Monaco FC": "موناکو",
    "Olympique Lyonnais": "لیون",
    "Lille OSC": "لیل",
    "OGC Nice": "نیس",
    "Stade Rennais FC": "رن",
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

    # ---------------- Netherlands ----------------

    "Ajax": "آژاکس",
    "PSV": "پی‌اس‌وی آیندهوون",
    "Feyenoord Rotterdam": "فاینورد",
    "FC Utrecht": "اوترخت",
    "AZ": "آلکمار",
    "FC Twente '65": "تونته",
    "Go Ahead Eagles": "گو اهد ایگلز",
    "FC Groningen": "خرونینگن",
    "PEC Zwolle": "زووله",
    "SC Heerenveen": "هیرنفین",
    "N.E.C.": "نایمخن",
    "Sparta Rotterdam": "اسپارتا روتردام",

    # ---------------- Portugal ----------------

    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting CP": "اسپورتینگ",
    "SC Braga": "براگا",
}


# =========================================================
# Custom Emoji ID تیم‌ها
#
# اینجا ID واقعی Custom Emoji تلگرام را قرار بده.
#
# مثال:
#
# "Chelsea FC": "5368324170671202286",
#
# اگر خالی باشد، فقط ایموجی معمولی یا اسم تیم نمایش داده می‌شود.
# =========================================================

TEAM_EMOJI_IDS = {

    "Chelsea FC": "",
    "Brentford FC": "",

    "FC Barcelona": "",
    "Real Madrid CF": "",

    "FC Bayern München": "",
    "Borussia Dortmund": "",

    "AC Milan": "",
    "FC Internazionale Milano": "",
    "Juventus FC": "",

    "Paris Saint-Germain FC": "",
    "AS Monaco FC": "",

    "Ajax": "",
    "PSV": "",

    "SL Benfica": "",
    "FC Porto": "",
    "Sporting CP": "",
}


# =========================================================
# ایموجی جایگزین برای زمانی که Custom Emoji نداریم
# =========================================================

TEAM_FALLBACK_EMOJI = {

    "Chelsea FC": "🔵",
    "Brentford FC": "🐝",

    "FC Barcelona": "🔴🔵",
    "Real Madrid CF": "⚪",

    "FC Bayern München": "🔴",
    "Borussia Dortmund": "🟡",

    "AC Milan": "🔴⚫",
    "FC Internazionale Milano": "🔵⚫",
    "Juventus FC": "⚫⚪",

    "Paris Saint-Germain FC": "🔵🔴",
    "AS Monaco FC": "🔴⚪",

    "Ajax": "🔴⚪",
    "PSV": "🔴⚪",

    "SL Benfica": "🔴",
    "FC Porto": "🔵",
    "Sporting CP": "🟢",
}


# =========================================================
# گرفتن تاریخ امروز تهران
# =========================================================

def get_today():
    now = datetime.now(TEHRAN_TZ)
    return now.strftime("%Y-%m-%d")


# =========================================================
# تبدیل نام تیم
# =========================================================

def get_team_name(team_name):

    return TEAM_NAMES.get(team_name, team_name)


# =========================================================
# ساخت Custom Emoji
# =========================================================

def get_team_emoji(team_name):

    emoji_id = TEAM_EMOJI_IDS.get(team_name, "").strip()

    # اگر Custom Emoji ID داریم
    if emoji_id:

        # ایموجی fallback داخل تگ قرار می‌گیرد
        fallback = TEAM_FALLBACK_EMOJI.get(
            team_name,
            "⚽"
        )

        return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

    # اگر Custom Emoji نداریم
    return TEAM_FALLBACK_EMOJI.get(
        team_name,
        "⚽"
    )


# =========================================================
# نام نهایی تیم برای پیام
# =========================================================

def format_team(team_name):

    emoji = get_team_emoji(team_name)
    name = get_team_name(team_name)

    return f"{emoji} {name}"


# =========================================================
# گرفتن بازی‌های یک لیگ
# =========================================================

def fetch_competition_matches(
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
        "Accept": "application/json",
    }

    params = {
        "dateFrom": date_from,
        "dateTo": date_to,
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20,
        )

        if response.status_code != 200:

            print(
                f"API Error {competition_code}: "
                f"{response.status_code}"
            )

            print(response.text)

            return []

        data = response.json()

        return data.get("matches", [])

    except requests.RequestException as e:

        print(
            f"Request Error {competition_code}: {e}"
        )

        return []


# =========================================================
# گرفتن همه بازی‌های امروز
# =========================================================

def collect_matches():

    today = get_today()

    all_matches = []

    for competition_code in COMPETITIONS:

        matches = fetch_competition_matches(
            competition_code,
            today,
            today
        )

        for match in matches:

            status = match.get(
                "status",
                ""
            )

            # بازی‌های لغوشده و به تعویق افتاده نمایش داده نشوند
            if status in [
                "CANCELLED",
                "POSTPONED",
                "SUSPENDED",
            ]:
                continue

            match["_competition_code"] = (
                competition_code
            )

            all_matches.append(match)

    return all_matches


# =========================================================
# ساعت بازی به وقت تهران
# =========================================================

def get_match_time(match):

    utc_date = match.get("utcDate")

    if not utc_date:
        return "--:--"

    try:

        # مثال:
        # 2026-09-18T18:30:00Z

        dt = datetime.fromisoformat(
            utc_date.replace(
                "Z",
                "+00:00"
            )
        )

        tehran_time = dt.astimezone(
            TEHRAN_TZ
        )

        # اعداد انگلیسی
        return tehran_time.strftime("%H:%M")

    except Exception:

        return "--:--"


# =========================================================
# مرتب‌سازی بازی‌ها بر اساس ساعت
# =========================================================

def sort_matches(matches):

    def sort_key(match):

        utc_date = match.get(
            "utcDate",
            ""
        )

        return utc_date

    return sorted(
        matches,
        key=sort_key
    )


# =========================================================
# ساخت پیام
# =========================================================

def build_message(matches):

    today = get_today()

    lines = []

    lines.append(
        "⚽ <b>بازی‌های امروز</b>"
    )

    lines.append(
        f"📅 تاریخ: {today}"
    )

    lines.append("")

    # گروه‌بندی بر اساس لیگ
    grouped = {}

    for match in matches:

        competition_code = match.get(
            "_competition_code"
        )

        if competition_code not in grouped:

            grouped[competition_code] = []

        grouped[
            competition_code
        ].append(match)

    # ترتیب نمایش لیگ‌ها
    for competition_code, competition in COMPETITIONS.items():

        league_matches = grouped.get(
            competition_code,
            []
        )

        if not league_matches:
            continue

        league_matches = sort_matches(
            league_matches
        )

        lines.append(
            f'{competition["flag"]} '
            f'<b>{competition["name"]}</b>'
        )

        lines.append("")

        for match in league_matches:

            home_team = match.get(
                "homeTeam",
                {}
            ).get(
                "name",
                "تیم میزبان"
            )

            away_team = match.get(
                "awayTeam",
                {}
            ).get(
                "name",
                "تیم مهمان"
            )

            home = format_team(
                home_team
            )

            away = format_team(
                away_team
            )

            match_time = get_match_time(
                match
            )

            lines.append(
                f"⚽ {home} - {away}"
            )

            lines.append(
                f"🕐 {match_time}"
            )

            lines.append("")

        # فاصله بین لیگ‌ها
        lines.append("")

    # حذف خطوط خالی اضافه آخر پیام
    while lines and not lines[-1].strip():

        lines.pop()

    return "\n".join(lines)


# =========================================================
# ارسال پیام به تلگرام
# =========================================================

def send_message(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:

        response = requests.post(
            url,
            data=data,
            timeout=20,
        )

        if response.status_code != 200:

            print(
                "Telegram Error:",
                response.text
            )

            return False

        result = response.json()

        if not result.get("ok"):

            print(
                "Telegram Error:",
                result
            )

            return False

        print(
            "پیام با موفقیت ارسال شد."
        )

        return True

    except requests.RequestException as e:

        print(
            "Telegram Request Error:",
            e
        )

        return False


# =========================================================
# اجرای اصلی
# =========================================================

def main():

    print(
        "در حال دریافت بازی‌های امروز..."
    )

    matches = collect_matches()

    if not matches:

        message = (
            "⚽ <b>بازی‌های امروز</b>\n"
            f"📅 تاریخ: {get_today()}\n\n"
            "❌ امروز بازی‌ای پیدا نشد."
        )

    else:

        message = build_message(
            matches
        )

    print("\n" + message + "\n")

    send_message(
        message
    )


# =========================================================
# Start
# =========================================================

if __name__ == "__main__":
    main()
