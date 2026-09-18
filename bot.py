# -*- coding: utf-8 -*-

import os
import time
import requests

from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import arabic_reshaper
from bidi.algorithm import get_display


# ============================================================
# SETTINGS
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

TEHRAN = ZoneInfo("Asia/Tehran")


# ============================================================
# 9 LEAGUES
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
# LEAGUE COLORS
# ============================================================

LEAGUE_COLORS = {
    "PL": (90, 25, 130),
    "PD": (205, 0, 45),
    "SA": (0, 100, 190),
    "BL1": (35, 40, 45),
    "FL1": (0, 75, 155),
    "DED": (245, 105, 10),
    "PPL": (0, 145, 75),
    "BSA": (0, 125, 70),
    "CL": (15, 55, 150),
}


# ============================================================
# TEAM NAMES
# ============================================================

TEAM_NAMES = {

    # ---------------- ENGLAND ----------------

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

    # ---------------- SPAIN ----------------

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

    # ---------------- ITALY ----------------

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

    # ---------------- GERMANY ----------------

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

    # ---------------- FRANCE ----------------

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

    # ---------------- NETHERLANDS ----------------

    "AFC Ajax": "آژاکس",
    "PSV": "آیندهوون",
    "Feyenoord Rotterdam": "فاینورد",
    "AZ": "آلکمار",
    "FC Twente '65": "توئنته",
    "FC Utrecht": "اوترخت",

    # ---------------- PORTUGAL ----------------

    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "SC Braga": "براگا",
    "Vitória SC": "ویتوریا گیمارش",

    # ---------------- BRAZIL ----------------

    "CR Flamengo": "فلامینگو",
    "SE Palmeiras": "پالمیراس",
    "Botafogo FR": "بوتافوگو",
    "Fluminense FC": "فلومیننزه",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
}


# ============================================================
# CACHE
# ============================================================

logo_cache = {}


# ============================================================
# FONTS
# ============================================================

def get_font(size, bold=False):

    if bold:
        paths = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for path in paths:

        if os.path.exists(path):

            try:
                return ImageFont.truetype(path, size)
            except:
                pass

    return ImageFont.load_default()


# ============================================================
# PERSIAN TEXT
# ============================================================

def fa_text(text):

    text = str(text)

    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    except:
        return text


# ============================================================
# DRAW PERSIAN TEXT
# ============================================================

def draw_fa(
    draw,
    xy,
    text,
    font,
    fill,
    anchor="mm"
):

    draw.text(
        xy,
        fa_text(text),
        font=font,
        fill=fill,
        anchor=anchor
    )


# ============================================================
# FIT TEXT
# ============================================================

def draw_fitted_text(
    draw,
    xy,
    text,
    max_width,
    max_size,
    min_size,
    fill
):

    for size in range(
        max_size,
        min_size - 1,
        -1
    ):

        font = get_font(
            size,
            bold=True
        )

        display_text = fa_text(text)

        box = draw.textbbox(
            (0, 0),
            display_text,
            font=font
        )

        text_width = box[2] - box[0]

        if text_width <= max_width:

            draw.text(
                xy,
                display_text,
                font=font,
                fill=fill,
                anchor="mm"
            )

            return

    font = get_font(
        min_size,
        bold=True
    )

    draw.text(
        xy,
        fa_text(text),
        font=font,
        fill=fill,
        anchor="mm"
    )


# ============================================================
# DOWNLOAD LOGO
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
            print(
                "Logo failed:",
                response.status_code
            )
            return None

        logo = Image.open(
            BytesIO(response.content)
        ).convert("RGBA")

        logo.thumbnail(
            (70, 70),
            Image.Resampling.LANCZOS
        )

        logo_cache[url] = logo

        return logo

    except Exception as e:

        print(
            "Logo error:",
            e
        )

        return None


# ============================================================
# MATCH TIME
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

        dt = dt.astimezone(
            TEHRAN
        )

        return dt.strftime(
            "%H:%M"
        )

    except:

        return "--:--"


# ============================================================
# TODAY
# ============================================================

def get_today():

    return datetime.now(
        TEHRAN
    ).strftime(
        "%Y-%m-%d"
    )


# ============================================================
# GET MATCHES
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
            "=>",
            response.status_code
        )

        if response.status_code == 429:

            print(
                "Rate limit. Waiting 45 seconds..."
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
# DRAW LOGO
# ============================================================

def paste_logo(
    image,
    logo,
    center_x,
    center_y
):

    if logo:

        x = int(
            center_x -
            logo.width / 2
        )

        y = int(
            center_y -
            logo.height / 2
        )

        image.paste(
            logo,
            (x, y),
            logo
        )


# ============================================================
# DRAW MATCH ROW
# ============================================================

def draw_match_row(
    image,
    draw,
    match,
    x,
    y,
    width,
    height
):

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

    # --------------------------------------------------------
    # CARD
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + height
        ),
        radius=18,
        fill=(255, 255, 255),
        outline=(225, 229, 235),
        width=2
    )

    center_y = y + height // 2

    # --------------------------------------------------------
    # HOME LOGO
    # --------------------------------------------------------

    home_logo_x = x + width - 55

    if home_logo:

        paste_logo(
            image,
            home_logo,
            home_logo_x,
            center_y
        )

    # --------------------------------------------------------
    # AWAY LOGO
    # --------------------------------------------------------

    away_logo_x = x + 55

    if away_logo:

        paste_logo(
            image,
            away_logo,
            away_logo_x,
            center_y
        )

    # --------------------------------------------------------
    # HOME NAME
    # --------------------------------------------------------

    draw_fitted_text(
        draw,
        (
            x + width - 155,
            center_y
        ),
        home,
        150,
        26,
        17,
        (20, 25, 35)
    )

    # --------------------------------------------------------
    # AWAY NAME
    # --------------------------------------------------------

    draw_fitted_text(
        draw,
        (
            x + 155,
            center_y
        ),
        away,
        150,
        26,
        17,
        (20, 25, 35)
    )

    # --------------------------------------------------------
    # TIME BOX
    # --------------------------------------------------------

    time_text = get_match_time(
        match
    )

    box_w = 92
    box_h = 48

    cx = x + width // 2

    draw.rounded_rectangle(
        (
            cx - box_w // 2,
            center_y - box_h // 2,
            cx + box_w // 2,
            center_y + box_h // 2
        ),
        radius=14,
        fill=(239, 246, 244)
    )

    time_font = get_font(
        25,
        bold=True
    )

    draw.text(
        (
            cx,
            center_y
        ),
        time_text,
        font=time_font,
        fill=(20, 115, 75),
        anchor="mm"
    )


# ============================================================
# DRAW LEAGUE BLOCK
# ============================================================

def draw_league_block(
    image,
    draw,
    code,
    matches,
    x,
    y,
    width
):

    color = LEAGUE_COLORS.get(
        code,
        (30, 90, 150)
    )

    league_name = COMPETITIONS.get(
        code,
        "مسابقات"
    )

    header_h = 58
    row_h = 108

    # --------------------------------------------------------
    # LEAGUE HEADER
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + header_h
        ),
        radius=18,
        fill=color
    )

    league_font = get_font(
        25,
        bold=True
    )

    draw.text(
        (
            x + width // 2,
            y + header_h // 2
        ),
        fa_text(league_name),
        font=league_font,
        fill=(255, 255, 255),
        anchor="mm"
    )

    # --------------------------------------------------------
    # MATCHES
    # --------------------------------------------------------

    current_y = y + header_h + 8

    for match in matches:

        draw_match_row(
            image,
            draw,
            match,
            x,
            current_y,
            width,
            row_h
        )

        current_y += row_h + 8

    return (
        header_h
        + 8
        + len(matches)
        * (row_h + 8)
        + 10
    )


# ============================================================
# CREATE PROFESSIONAL IMAGE
# ============================================================

def create_matches_image(
    matches
):

    WIDTH = 1200

    SIDE = 35

    GAP = 25

    COLUMN_WIDTH = (
        WIDTH
        - SIDE * 2
        - GAP
    ) // 2

    HEADER_HEIGHT = 245

    # --------------------------------------------------------
    # GROUP BY LEAGUE
    # --------------------------------------------------------

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

    # مرتب‌سازی بازی‌ها
    for code in grouped:

        grouped[code].sort(
            key=lambda m:
            m.get("utcDate", "")
        )

    # --------------------------------------------------------
    # BALANCE TWO COLUMNS
    # --------------------------------------------------------

    left = []
    right = []

    left_height = 0
    right_height = 0

    for code in COMPETITIONS:

        if code not in grouped:
            continue

        matches_for_league = grouped[
            code
        ]

        block_height = (
            58
            + 8
            + len(matches_for_league)
            * (108 + 8)
            + 10
        )

        if left_height <= right_height:

            left.append(
                (
                    code,
                    matches_for_league
                )
            )

            left_height += block_height

        else:

            right.append(
                (
                    code,
                    matches_for_league
                )
            )

            right_height += block_height

    content_height = max(
        left_height,
        right_height
    )

    height = (
        HEADER_HEIGHT
        + content_height
        + 40
    )

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    image = Image.new(
        "RGB",
        (
            WIDTH,
            height
        ),
        (10, 35, 60)
    )

    draw = ImageDraw.Draw(
        image
    )

    # --------------------------------------------------------
    # GRADIENT BACKGROUND
    # --------------------------------------------------------

    for yy in range(height):

        ratio = yy / max(
            height,
            1
        )

        r = int(
            8 + 8 * ratio
        )

        g = int(
            35 + 35 * ratio
        )

        b = int(
            60 + 25 * ratio
        )

        draw.line(
            (
                0,
                yy,
                WIDTH,
                yy
            ),
            fill=(r, g, b)
        )

    # --------------------------------------------------------
    # DECORATIVE LINES
    # --------------------------------------------------------

    for i in range(
        0,
        WIDTH,
        80
    ):

        draw.line(
            (
                i,
                0,
                i + 180,
                180
            ),
            fill=(30, 75, 100),
            width=2
        )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            30,
            25,
            WIDTH - 30,
            HEADER_HEIGHT - 20
        ),
        radius=35,
        fill=(7, 24, 45),
        outline=(30, 205, 125),
        width=3
    )

    # سبز بالا
    draw.rounded_rectangle(
        (
            160,
            25,
            WIDTH - 160,
            36
        ),
        radius=5,
        fill=(30, 220, 125)
    )

    # --------------------------------------------------------
    # FOOTBALL ICON
    # --------------------------------------------------------

    ball_x = 165
    ball_y = 95

    draw.ellipse(
        (
            ball_x - 45,
            ball_y - 45,
            ball_x + 45,
            ball_y + 45
        ),
        fill=(255, 255, 255),
        outline=(210, 215, 220),
        width=3
    )

    # خطوط ساده توپ
    draw.line(
        (
            ball_x - 20,
            ball_y - 25,
            ball_x + 5,
            ball_y - 10
        ),
        fill=(35, 45, 55),
        width=4
    )

    draw.line(
        (
            ball_x + 5,
            ball_y - 10,
            ball_x + 25,
            ball_y + 15
        ),
        fill=(35, 45, 55),
        width=4
    )

    draw.line(
        (
            ball_x - 20,
            ball_y - 25,
            ball_x - 25,
            ball_y + 15
        ),
        fill=(35, 45, 55),
        width=4
    )

    # --------------------------------------------------------
    # MAIN TITLE
    # --------------------------------------------------------

    title_font = get_font(
        56,
        bold=True
    )

    draw.text(
        (
            WIDTH // 2 + 35,
            90
        ),
        fa_text(
            "بازی‌های امروز"
        ),
        font=title_font,
        fill=(255, 255, 255),
        anchor="mm"
    )

    # --------------------------------------------------------
    # GREEN SUBTITLE
    # --------------------------------------------------------

    subtitle_font = get_font(
        31,
        bold=True
    )

    draw.text(
        (
            WIDTH // 2 + 20,
            150
        ),
        fa_text(
            "۹ لیگ معتبر"
        ),
        font=subtitle_font,
        fill=(30, 225, 125),
        anchor="mm"
    )

    # --------------------------------------------------------
    # TEHRAN TIME
    # --------------------------------------------------------

    date_font = get_font(
        25,
        bold=True
    )

    draw.text(
        (
            WIDTH // 2 + 20,
            200
        ),
        fa_text(
            "زمان‌ها به وقت تهران"
        ),
        font=date_font,
        fill=(215, 225, 232),
        anchor="mm"
    )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    small_font = get_font(
        20
    )

    draw.text(
        (
            WIDTH // 2 + 20,
            225
        ),
        get_today(),
        font=small_font,
        fill=(150, 170, 185),
        anchor="mm"
    )

    # --------------------------------------------------------
    # COLUMNS
    # --------------------------------------------------------

    left_x = SIDE

    right_x = (
        SIDE
        + COLUMN_WIDTH
        + GAP
    )

    left_y = HEADER_HEIGHT
    right_y = HEADER_HEIGHT

    for code, league_matches in left:

        block_height = draw_league_block(
            image,
            draw,
            code,
            league_matches,
            left_x,
            left_y,
            COLUMN_WIDTH
        )

        left_y += block_height

    for code, league_matches in right:

        block_height = draw_league_block(
            image,
            draw,
            code,
            league_matches,
            right_x,
            right_y,
            COLUMN_WIDTH
        )

        right_y += block_height

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    footer_y = height - 30

    draw.line(
        (
            100,
            footer_y,
            WIDTH - 100,
            footer_y
        ),
        fill=(30, 210, 125),
        width=3
    )

    return image


# ============================================================
# SEND PHOTO
# ============================================================

def send_matches_image(
    matches
):

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
            "https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendPhoto"
        )

        caption = (
            "⚽ بازی‌های امروز\n"
            "۹ لیگ معتبر\n"
            "🕐 زمان‌ها به وقت تهران"
        )

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },
            files={
                "photo": (
                    "today_matches.jpg",
                    output,
                    "image/jpeg"
                )
            },
            timeout=90
        )

        print(
            "Telegram:",
            response.status_code
        )

        print(
            response.text
        )

        return response.ok

    except Exception as e:

        print(
            "SEND IMAGE ERROR:",
            e
        )

        return False


# ============================================================
# SEND TEXT FALLBACK
# ============================================================

def send_message(text):

    try:

        url = (
            "https://api.telegram.org/"
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
            "Telegram text:",
            response.status_code
        )

        return response.ok

    except Exception as e:

        print(
            "Telegram text error:",
            e
        )

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "========================================"
    )

    print(
        "FOOTBALL ALERT BOT"
    )

    print(
        "========================================"
    )

    # بررسی Secrets
    missing = []

    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")

    if not CHAT_ID:
        missing.append("CHAT_ID")

    if not FOOTBALL_API_TOKEN:
        missing.append("FOOTBALL_API_TOKEN")

    if missing:

        print(
            "Missing secrets:",
            missing
        )

        return

    today = get_today()

    print(
        "Tehran date:",
        today
    )

    all_matches = []

    # --------------------------------------------------------
    # GET 9 LEAGUES
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

            match[
                "league_code"
            ] = competition

            all_matches.append(
                match
            )

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    all_matches.sort(
        key=lambda m:
        m.get(
            "utcDate",
            ""
        )
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
    # ONE IMAGE
    # --------------------------------------------------------

    success = send_matches_image(
        all_matches
    )

    if success:

        print(
            "========================================"
        )

        print(
            "SUCCESS - ONE DAILY IMAGE SENT"
        )

        print(
            "========================================"
        )

    else:

        print(
            "Image failed."
        )

        send_message(
            f"⚽ بازی‌های امروز\n"
            f"📅 {today}\n"
            f"تعداد بازی‌ها: {len(all_matches)}"
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
