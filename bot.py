# -*- coding: utf-8 -*-

import os
import time
import requests

from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# SETTINGS
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"


# ============================================================
# LEAGUES
# ============================================================

COMPETITIONS = {
    "PL": "لیگ برتر انگلیس",
    "PD": "لالیگا",
    "SA": "سری آ ایتالیا",
    "BL1": "بوندسلیگا",
    "FL1": "لیگ ۱ فرانسه",
    "DED": "اردیویسه",
    "PPL": "لیگ پرتغال",
    "BSA": "سری آ برزیل",
    "CL": "لیگ قهرمانان اروپا",
}


# ============================================================
# TEAM NAMES
# ============================================================

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
    "Inter Milan": "اینتر",
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
    "Paris Saint-Germain FC": "پاری سن ژرمن",
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


# ============================================================
# LOGO CACHE
# ============================================================

logo_cache = {}


# ============================================================
# FONT
# ============================================================

def get_font(size, bold=False):

    if bold:
        paths = [
            "/usr/share/fonts/truetype/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for path in paths:

        if os.path.exists(path):

            try:
                return ImageFont.truetype(
                    path,
                    size
                )
            except:
                pass

    return ImageFont.load_default()


# ============================================================
# PERSIAN TEXT
# ============================================================

def draw_fa(
    draw,
    position,
    text,
    font,
    fill,
    stroke_width=0
):

    try:

        draw.text(
            position,
            text,
            font=font,
            fill=fill,
            anchor="mm",
            direction="rtl",
            language="fa",
            stroke_width=stroke_width,
            stroke_fill=fill
        )

    except:

        draw.text(
            position,
            text,
            font=font,
            fill=fill,
            anchor="mm",
            stroke_width=stroke_width,
            stroke_fill=fill
        )


# ============================================================
# LOGO
# ============================================================

def download_logo(url):

    if not url:
        return None

    if url in logo_cache:
        return logo_cache[url]

    try:

        response = requests.get(
            url,
            timeout=20
        )

        if response.status_code != 200:
            return None

        logo = Image.open(
            BytesIO(response.content)
        ).convert("RGBA")

        logo.thumbnail(
            (90, 90),
            Image.Resampling.LANCZOS
        )

        logo_cache[url] = logo

        return logo

    except Exception as e:

        print("Logo error:", e)

        return None


# ============================================================
# TIME
# ============================================================

def get_match_time(match):

    utc_date = match.get("utcDate")

    if not utc_date:
        return "--:--"

    try:

        dt = datetime.fromisoformat(
            utc_date.replace(
                "Z",
                "+00:00"
            )
        )

        tehran = ZoneInfo(
            "Asia/Tehran"
        )

        iran_time = dt.astimezone(
            tehran
        )

        return iran_time.strftime(
            "%H:%M"
        )

    except:

        return "--:--"


# ============================================================
# TODAY
# ============================================================

def get_today():

    return datetime.now(
        ZoneInfo("Asia/Tehran")
    ).strftime(
        "%Y-%m-%d"
    )


# ============================================================
# API
# ============================================================

def get_matches(
    competition,
    date
):

    url = API_URL.format(
        competition
    )

    headers = {
        "X-Auth-Token":
        FOOTBALL_API_TOKEN
    }

    params = {
        "dateFrom": date,
        "dateTo": date
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        print(
            competition,
            response.status_code
        )

        if response.status_code == 429:

            print(
                "Rate limit - waiting..."
            )

            time.sleep(45)

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

        if response.status_code != 200:

            print(
                response.text[:500]
            )

            return []

        data = response.json()

        return data.get(
            "matches",
            []
        )

    except Exception as e:

        print(
            "API error:",
            competition,
            e
        )

        return []


# ============================================================
# CREATE IMAGE
# ============================================================

def create_matches_image(matches):

    width = 1200

    header_height = 250

    league_height = 72

    match_height = 165

    bottom = 40

    grouped = {}

    for match in matches:

        code = match.get(
            "league_code",
            ""
        )

        if code not in grouped:
            grouped[code] = []

        grouped[code].append(
            match
        )

    height = header_height + bottom

    for league_code, league_matches in grouped.items():

        height += league_height

        height += (
            len(league_matches)
            * match_height
        )

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    image = Image.new(
        "RGB",
        (
            width,
            height
        ),
        (246, 248, 251)
    )

    draw = ImageDraw.Draw(
        image
    )

    # --------------------------------------------------------
    # FONTS
    # --------------------------------------------------------

    title_font = get_font(
        58,
        bold=True
    )

    subtitle_font = get_font(
        34,
        bold=True
    )

    date_font = get_font(
        24,
        bold=False
    )

    league_font = get_font(
        29,
        bold=True
    )

    team_font = get_font(
        34,
        bold=True
    )

    time_font = get_font(
        38,
        bold=True
    )

    vs_font = get_font(
        18,
        bold=True
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    # هدر سفید
    draw.rounded_rectangle(
        (
            25,
            20,
            width - 25,
            header_height - 15
        ),
        radius=30,
        fill=(255, 255, 255),
        outline=(225, 229, 235),
        width=2
    )

    # خط سبز بالای هدر
    draw.rounded_rectangle(
        (
            90,
            20,
            width - 90,
            30
        ),
        radius=5,
        fill=(25, 170, 100)
    )

    # عنوان اصلی
    draw_fa(
        draw,
        (
            width // 2,
            75
        ),
        "بازی‌های امروز",
        title_font,
        (25, 32, 45),
        stroke_width=1
    )

    # متن دوم
    draw_fa(
        draw,
        (
            width // 2,
            135
        ),
        "۹ لیگ معتبر",
        subtitle_font,
        (25, 145, 90),
        stroke_width=1
    )

    # متن سوم
    draw_fa(
        draw,
        (
            width // 2,
            190
        ),
        "زمان‌ها به وقت تهران",
        date_font,
        (95, 102, 112)
    )

    # تاریخ کوچک
    draw_fa(
        draw,
        (
            width // 2,
            220
        ),
        get_today(),
        date_font,
        (145, 150, 158)
    )

    # --------------------------------------------------------
    # MATCHES
    # --------------------------------------------------------

    y = header_height

    for league_code, league_matches in grouped.items():

        league_name = COMPETITIONS.get(
            league_code,
            "مسابقات"
        )

        # ----------------------------------------------------
        # LEAGUE BAR
        # ----------------------------------------------------

        draw.rounded_rectangle(
            (
                45,
                y + 10,
                width - 45,
                y + league_height - 5
            ),
            radius=18,
            fill=(232, 236, 242)
        )

        # خط سبز کوچک
        draw.rounded_rectangle(
            (
                65,
                y + 25,
                72,
                y + 52
            ),
            radius=4,
            fill=(25, 170, 100)
        )

        draw_fa(
            draw,
            (
                width // 2,
                y + 39
            ),
            league_name,
            league_font,
            (35, 42, 52),
            stroke_width=1
        )

        y += league_height

        # ----------------------------------------------------
        # MATCH CARDS
        # ----------------------------------------------------

        for match in league_matches:

            top = y + 8
            bottom_card = (
                y + match_height - 8
            )

            # سایه
            draw.rounded_rectangle(
                (
                    48,
                    top + 4,
                    width - 42,
                    bottom_card + 5
                ),
                radius=24,
                fill=(225, 228, 233)
            )

            # کارت اصلی
            draw.rounded_rectangle(
                (
                    45,
                    top,
                    width - 45,
                    bottom_card
                ),
                radius=24,
                fill=(255, 255, 255),
                outline=(225, 229, 235),
                width=2
            )

            home_data = match.get(
                "homeTeam",
                {}
            )

            away_data = match.get(
                "awayTeam",
                {}
            )

            home_original = home_data.get(
                "name",
                "میزبان"
            )

            away_original = away_data.get(
                "name",
                "مهمان"
            )

            home = TEAM_NAMES.get(
                home_original,
                home_original
            )

            away = TEAM_NAMES.get(
                away_original,
                away_original
            )

            home_logo = download_logo(
                home_data.get("crest")
            )

            away_logo = download_logo(
                away_data.get("crest")
            )

            center_y = y + 82

            # ------------------------------------------------
            # HOME LOGO
            # ------------------------------------------------

            if home_logo:

                logo = home_logo.copy()

                logo.thumbnail(
                    (82, 82),
                    Image.Resampling.LANCZOS
                )

                image.paste(
                    logo,
                    (
                        950 -
                        logo.width // 2,
                        center_y -
                        logo.height // 2
                    ),
                    logo
                )

            # ------------------------------------------------
            # HOME NAME
            # ------------------------------------------------

            draw_fa(
                draw,
                (
                    805,
                    center_y
                ),
                home,
                team_font,
                (25, 30, 40),
                stroke_width=1
            )

            # ------------------------------------------------
            # AWAY LOGO
            # ------------------------------------------------

            if away_logo:

                logo = away_logo.copy()

                logo.thumbnail(
                    (82, 82),
                    Image.Resampling.LANCZOS
                )

                image.paste(
                    logo,
                    (
                        250 -
                        logo.width // 2,
                        center_y -
                        logo.height // 2
                    ),
                    logo
                )

            # ------------------------------------------------
            # AWAY NAME
            # ------------------------------------------------

            draw_fa(
                draw,
                (
                    395,
                    center_y
                ),
                away,
                team_font,
                (25, 30, 40),
                stroke_width=1
            )

            # ------------------------------------------------
            # TIME
            # ------------------------------------------------

            match_time = get_match_time(
                match
            )

            # زمان - کادر سبز
            draw.rounded_rectangle(
                (
                    525,
                    center_y - 35,
                    675,
                    center_y + 35
                ),
                radius=20,
                fill=(235, 249, 242),
                outline=(25, 170, 100),
                width=2
            )

            draw.text(
                (
                    600,
                    center_y
                ),
                match_time,
                font=time_font,
                fill=(20, 120, 75),
                anchor="mm"
            )

            # VS
            draw.text(
                (
                    600,
                    center_y + 47
                ),
                "VS",
                font=vs_font,
                fill=(145, 150, 158),
                anchor="mm"
            )

            y += match_height

    return image


# ============================================================
# SEND IMAGE
# ============================================================

def send_matches_image(matches):

    try:

        image = create_matches_image(
            matches
        )

        output = BytesIO()

        image.save(
            output,
            format="JPEG",
            quality=94,
            optimize=True
        )

        output.seek(0)

        url = (
            f"https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendPhoto"
        )

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": (
                    "⚽ بازی‌های امروز\n"
                    "۹ لیگ معتبر\n"
                    "🕐 زمان‌ها به وقت تهران"
                )
            },
            files={
                "photo": (
                    "today_matches.jpg",
                    output,
                    "image/jpeg"
                )
            },
            timeout=60
        )

        print(
            "Telegram image:",
            response.status_code
        )

        print(
            response.text
        )

        return response.ok

    except Exception as e:

        print(
            "Image error:",
            e
        )

        return False


# ============================================================
# TELEGRAM TEXT
# ============================================================

def send_message(text):

    try:

        url = (
            f"https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendMessage"
        )

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=30
        )

        print(
            "Telegram:",
            response.status_code
        )

        return response.ok

    except Exception as e:

        print(
            "Telegram error:",
            e
        )

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "=============================="
    )

    print(
        "FOOTBALL ALERT BOT"
    )

    print(
        "=============================="
    )

    today = get_today()

    print(
        "Today:",
        today
    )

    all_matches = []

    # --------------------------------------------------------
    # GET ALL LEAGUES
    # --------------------------------------------------------

    for competition in COMPETITIONS:

        print(
            "Checking:",
            competition
        )

        matches = get_matches(
            competition,
            today
        )

        for match in matches:

            match["league_code"] = (
                competition
            )

            all_matches.append(
                match
            )

    print(
        "TOTAL MATCHES:",
        len(all_matches)
    )

    # --------------------------------------------------------
    # NO MATCHES
    # --------------------------------------------------------

    if not all_matches:

        send_message(
            "⚽ بازی‌ای برای امروز پیدا نشد.\n"
            f"📅 {today}"
        )

        return

    # --------------------------------------------------------
    # SEND IMAGE
    # --------------------------------------------------------

    if send_matches_image(
        all_matches
    ):

        print(
            "IMAGE SENT SUCCESSFULLY"
        )

    else:

        send_message(
            f"⚽ بازی‌های امروز\n"
            f"تعداد بازی‌ها: {len(all_matches)}\n"
            f"📅 {today}"
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
