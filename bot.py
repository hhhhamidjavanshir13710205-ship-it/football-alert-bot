import os
import requests
import jdatetime

from datetime import datetime
from zoneinfo import ZoneInfo


# =========================================================
# تنظیمات
# =========================================================

BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    "YOUR_TELEGRAM_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "CHAT_ID",
    "YOUR_CHAT_ID"
)

FOOTBALL_API_TOKEN = os.getenv(
    "FOOTBALL_API_TOKEN",
    "YOUR_FOOTBALL_DATA_API_TOKEN"
)

API_BASE = "https://api.football-data.org/v4"

TEHRAN_TZ = ZoneInfo("Asia/Tehran")


# =========================================================
# لیگ‌ها
# =========================================================

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

    "DED": {
        "name": "اردیویسه",
        "flag": "🇳🇱"
    },

    "PPL": {
        "name": "لیگ پرتغال",
        "flag": "🇵🇹"
    },

    "BSA": {
        "name": "سری آ برزیل",
        "flag": "🇧🇷"
    },

    "CL": {
        "name": "لیگ قهرمانان اروپا",
        "flag": "🇪🇺"
    }
}


# =========================================================
# نام فارسی تیم‌ها
# =========================================================

TEAM_NAMES = {

    # =====================================================
    # ENGLAND
    # =====================================================

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
    "Hull City": "هال سیتی",
    "Coventry City FC": "کاونتری سیتی",
    "Coventry City": "کاونتری سیتی",

    # =====================================================
    # SPAIN
    # =====================================================

    "FC Barcelona": "بارسلونا",
    "Real Madrid CF": "رئال مادرید",
    "Real Madrid": "رئال مادرید",
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
    "Racing Santander": "راسینگ سانتاندر",

    # =====================================================
    # ITALY
    # =====================================================

    "FC Internazionale Milano": "اینتر",
    "Inter Milan": "اینتر",
    "Inter": "اینتر",
    "AC Milan": "میلان",
    "Juventus FC": "یوونتوس",
    "SSC Napoli": "ناپولی",
    "AS Roma": "رم",
    "SS Lazio": "لاتزیو",
    "Atalanta BC": "آتالانتا",
    "ACF Fiorentina": "فیورنتینا",
    "Bologna FC 1909": "بولونیا",
    "Bologna": "بولونیا",
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
    "Venezia": "ونیزیا",

    # =====================================================
    # GERMANY
    # =====================================================

    "FC Bayern München": "بایرن مونیخ",
    "FC Bayern Munich": "بایرن مونیخ",
    "Bayern Munich": "بایرن مونیخ",
    "Borussia Dortmund": "بوروسیا دورتموند",
    "RB Leipzig": "لایپزیگ",
    "Bayer 04 Leverkusen": "بایرلورکوزن",
    "Bayer Leverkusen": "بایرلورکوزن",
    "Eintracht Frankfurt": "آینتراخت فرانکفورت",
    "VfB Stuttgart": "اشتوتگارت",
    "SC Freiburg": "فرایبورگ",
    "1. FSV Mainz 05": "ماینتس",
    "Mainz 05": "ماینتس",
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
    "Hamburger SV II": "هامبورگ",
    "1. FC Köln": "کلن",
    "FC Cologne": "کلن",

    # =====================================================
    # FRANCE
    # =====================================================

    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
    "Paris Saint-Germain": "پاری‌سن‌ژرمن",
    "Olympique de Marseille": "مارسی",
    "AS Monaco FC": "موناکو",
    "Olympique Lyonnais": "لیون",
    "Lille OSC": "لیل",
    "OGC Nice": "نیس",
    "Stade Rennais FC": "رن",
    "Stade Rennais FC 1901": "رن",
    "RC Strasbourg Alsace": "استراسبورگ",
    "RC Strasbourg": "استراسبورگ",
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

    # =====================================================
    # NETHERLANDS
    # =====================================================

    "Ajax": "آژاکس",
    "AFC Ajax": "آژاکس",
    "PSV": "پی‌اس‌وی",
    "PSV Eindhoven": "پی‌اس‌وی",
    "Feyenoord Rotterdam": "فاینورد",
    "Feyenoord": "فاینورد",
    "FC Utrecht": "اوترخت",
    "AZ": "آلکمار",
    "AZ Alkmaar": "آلکمار",
    "FC Twente '65": "تونته",
    "FC Twente": "تونته",
    "Go Ahead Eagles": "گو اهد ایگلز",
    "FC Groningen": "خرونینگن",
    "PEC Zwolle": "زووله",
    "SC Heerenveen": "هیرنفین",
    "N.E.C.": "نایمخن",
    "NEC Nijmegen": "نایمخن",
    "Sparta Rotterdam": "اسپارتا روتردام",
    "Sparta Rotterdam": "اسپارتا روتردام",
    "ADO Den Haag": "آدو دن هاخ",
    "ADO Den Haag FC": "آدو دن هاخ",
    "SC Cambuur-Leeuwarden": "کامبور",
    "SC Cambuur": "کامبور",
    "SBV Excelsior": "اکسلسیور",
    "Excelsior": "اکسلسیور",
    "Willem II Tilburg": "ویلم دوم",
    "Willem II": "ویلم دوم",
    "Fortuna Sittard": "فورتونا سیتارد",

    # =====================================================
    # PORTUGAL
    # =====================================================

    "SL Benfica": "بنفیکا",
    "Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Porto": "پورتو",
    "Sporting CP": "اسپورتینگ",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "Sporting Portugal": "اسپورتینگ",
    "SC Braga": "براگا",
    "Braga": "براگا",
    "CD Nacional": "ناسیونال",
    "Nacional": "ناسیونال",
    "FC Famalicão": "فامالیکائو",
    "Famalicao": "فامالیکائو",
    "Gil Vicente FC": "ژیل ویسنته",
    "Gil Vicente": "ژیل ویسنته",
    "CS Marítimo": "ماریتیمو",
    "Maritimo": "ماریتیمو",
    "FC Alverca": "آلورکا",
    "Alverca": "آلورکا",
    "Rio Ave FC": "ریو آوه",
    "Rio Ave": "ریو آوه",
    "FC Arouca": "آروکا",
    "Arouca": "آروکا",

    # =====================================================
    # BRAZIL
    # =====================================================

    "CR Flamengo": "فلامنگو",
    "Flamengo": "فلامنگو",
    "SE Palmeiras": "پالمیراس",
    "Palmeiras": "پالمیراس",
    "Santos FC": "سانتوس",
    "Santos": "سانتوس",
    "São Paulo FC": "سائوپائولو",
    "Sao Paulo": "سائوپائولو",
    "SC Corinthians Paulista": "کورینتیانس",
    "Corinthians": "کورینتیانس",
    "Fluminense FC": "فلومیننزه",
    "Fluminense": "فلومیننزه",
    "Botafogo FR": "بوتافوگو",
    "Botafogo": "بوتافوگو",
    "CR Vasco da Gama": "واسکو دوگاما",
    "Vasco da Gama": "واسکو دوگاما",
    "Grêmio FBPA": "گرمیو",
    "Gremio": "گرمیو",
    "SC Internacional": "اینترناسیونال",
    "Internacional": "اینترناسیونال",
    "Cruzeiro EC": "کروزیرو",
    "Cruzeiro": "کروزیرو",
    "EC Bahia": "باهیا",
    "Bahia": "باهیا",
    "Fortaleza EC": "فورتالزا",
    "Fortaleza": "فورتالزا",
    "Athletico Paranaense": "اتلتیکو پارانائنزه",
    "Athletico-PR": "اتلتیکو پارانائنزه",
    "RB Bragantino": "ردبول براگانتیـنو",
    "Bragantino": "براگانتیـنو",
    "Cuiabá EC": "کویابا",
    "Cuiaba": "کویابا",
    "Atlético Mineiro": "اتلتیکو مینیرو",
    "Atletico Mineiro": "اتلتیکو مینیرو",
    "Vitoria SC": "وینتوریا",
    "Vitória": "وینتوریا",

    # =====================================================
    # CHAMPIONS LEAGUE / EUROPE
    # =====================================================

    "Manchester City": "منچسترسیتی",
    "Manchester United": "منچستریونایتد",
    "Liverpool": "لیورپول",
    "Arsenal": "آرسنال",
    "Chelsea": "چلسی",
    "Tottenham": "تاتنهام",
    "Newcastle United": "نیوکاسل",
    "Aston Villa": "استون ویلا",
    "Real Madrid": "رئال مادرید",
    "Barcelona": "بارسلونا",
    "Atletico Madrid": "اتلتیکومادرید",
    "Bayern Munich": "بایرن مونیخ",
    "Borussia Dortmund": "بوروسیا دورتموند",
    "Bayer Leverkusen": "بایرلورکوزن",
    "Inter Milan": "اینتر",
    "AC Milan": "میلان",
    "Juventus": "یوونتوس",
    "Napoli": "ناپولی",
    "Paris Saint-Germain": "پاری‌سن‌ژرمن",
    "Benfica": "بنفیکا",
    "Porto": "پورتو",
    "Sporting CP": "اسپورتینگ",
    "Ajax": "آژاکس",
    "PSV Eindhoven": "پی‌اس‌وی",
    "Feyenoord": "فاینورد",
    "RB Leipzig": "لایپزیگ",
    "Atalanta": "آتالانتا",
    "Monaco": "موناکو",
    "Marseille": "مارسی",
    "Club Brugge": "کلوب بروژ",
    "Shakhtar Donetsk": "شاختار دونتسک",
    "Galatasaray": "گالاتاسرای",
    "Fenerbahçe": "فنرباغچه",
    "Fenerbahce": "فنرباغچه",
    "PSV": "پی‌اس‌وی",
    "Celtic": "سلتیک",
    "Rangers": "رنجرز",
    "Red Bull Salzburg": "ردبول سالزبورگ",
    "Salzburg": "سالزبورگ",
    "Dinamo Zagreb": "دینامو زاگرب",
    "Young Boys": "یانگ بویز",
    "Benfica": "بنفیکا",
    "Olympiacos": "المپیاکوس",
    "Olympiacos FC": "المپیاکوس",
    "Club Brugge KV": "کلوب بروژ",
    "PSV Eindhoven": "پی‌اس‌وی",
    "Slavia Praha": "اسلاویا پراگ",
    "Sparta Praha": "اسپارتا پراگ",
    "Bologna FC 1909": "بولونیا",
    "Girona FC": "ژیرونا",
    "Lille OSC": "لیل",
    "Stuttgart": "اشتوتگارت",
    "Monaco": "موناکو",
}


# =========================================================
# تبدیل نام تیم
# =========================================================

def get_team_name(name):

    if not name:
        return "نامشخص"

    # حذف فاصله‌های اضافی
    name = " ".join(str(name).split())

    # ابتدا تطبیق مستقیم
    if name in TEAM_NAMES:
        return TEAM_NAMES[name]

    # تطبیق بدون حساسیت به حروف
    name_lower = name.lower()

    for original, persian in TEAM_NAMES.items():

        if original.lower() == name_lower:
            return persian

    # اگر نام پیدا نشد، فعلاً همان نام API برگردد
    # تا اسم ناشناخته مشخص شود
    return name


# =========================================================
# استایل اسم تیم
# =========================================================

def style_team_name(name):

    return get_team_name(name)


# =========================================================
# تاریخ شمسی ایران
# =========================================================

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


# =========================================================
# تاریخ میلادی برای API
# =========================================================

def get_api_date():

    now = datetime.now(TEHRAN_TZ)

    return now.strftime("%Y-%m-%d")


# =========================================================
# دریافت بازی‌های یک لیگ
# =========================================================

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


# =========================================================
# جمع‌آوری بازی‌ها
# =========================================================

def collect_matches():

    today = get_api_date()

    all_matches = []

    for code in COMPETITIONS:

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


# =========================================================
# ساعت تهران
# =========================================================

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


# =========================================================
# ساخت پیام
# =========================================================

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

    # =====================================================
    # عنوان
    # =====================================================

    lines.append(
        "🏆 <b>بازی‌های امروز</b>"
    )

    lines.append(
        f"📅 {get_persian_date()} 🇮🇷"
    )

    lines.append("")

    # =====================================================
    # لیگ‌ها
    # =====================================================

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

        lines.append(
            f'{competition["flag"]} '
            f'<b>━━━ {competition["name"]} ━━━</b>'
        )

        lines.append("")

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

            time = get_match_time(
                match
            )

            lines.append(
                f"🏟️ <b>{home}</b>  🆚  <b>{away}</b>"
            )

            lines.append(
                f"🕐 {time}"
            )

            lines.append("")

        lines.append(
            "━━━━━━━━━━━━━━━━"
        )

        lines.append("")

    # حذف خطوط خالی انتهایی
    while lines and not lines[-1].strip():
        lines.pop()

    return "\n".join(lines)


# =========================================================
# ارسال به تلگرام
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


# =========================================================
# اجرای اصلی
# =========================================================

def main():

    print(
        "⏳ در حال دریافت بازی‌های امروز..."
    )

    matches = collect_matches()

    if not matches:

        message = (
            "🏆 <b>بازی‌های امروز</b>\n"
            f"📅 {get_persian_date()} 🇮🇷\n\n"
            "❌ بازی‌ای برای امروز پیدا نشد."
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


if __name__ == "__main__":
    main()
