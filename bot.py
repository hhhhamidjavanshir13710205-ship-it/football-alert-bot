# -*- coding: utf-8 -*-

import os
import time
import requests

from io import BytesIO
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


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
# COLORS
# ============================================================

LEAGUE_COLORS = {
    "PL": (105, 30, 145),
    "PD": (215, 0, 55),
    "SA": (10, 105, 195),
    "BL1": (40, 45, 50),
    "FL1": (5, 100, 190),
    "DED": (245, 105, 5),
    "PPL": (0, 145, 80),
    "BSA": (0, 125, 70),
    "CL": (30, 75, 175),
}


# ============================================================
# TEAM NAMES
# ============================================================

TEAM_NAMES = {

    # ENGLAND
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

    # SPAIN
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

    # ITALY
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
    "US Sassuolo Calcio": "ساسولو",
    "Sassuolo Calcio": "ساسولو",
    "AC Monza": "مونتزا",
    "AC Monza S.p.A.": "مونتزا",

    # GERMANY
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

    # FRANCE
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
    "Racing Club de Lens": "لانس",
    "RC Strasbourg Alsace": "استراسبورگ",

    # NETHERLANDS
    "AFC Ajax": "آژاکس",
    "PSV": "آیندهوون",
    "Feyenoord Rotterdam": "فاینورد",
    "AZ": "آلکمار",
    "FC Twente '65": "توئنته",
    "FC Utrecht": "اوترخت",
    "PEC Zwolle": "زوله",
    "FC Groningen": "خرونینگن",

    # PORTUGAL
    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "SC Braga": "براگا",
    "Vitória SC": "ویتوریا گیمارش",

    # BRAZIL
    "CR Flamengo": "فلامینگو",
    "SE Palmeiras": "پالمیراس",
    "Botafogo FR": "بوتافوگو",
    "Fluminense FC": "فلومیننزه",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
}


# ============================================================
# FONT
# ============================================================

def get_font(size, bold=False):

    if bold:
        paths = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass

    return ImageFont.load_default()


# ============================================================
# PERSIAN TEXT
#
# مهم:
# متن را مستقیماً با direction=rtl به Pillow می‌دهیم.
# دیگر از arabic_reshaper + bidi استفاده نمی‌کنیم تا
# مشکل وارونه شدن نوشته نسخه قبلی تکرار نشود.
# ============================================================

def draw_persian(
    draw,
    xy,
    text,
    font,
    fill,
    anchor="mm"
):

    try:

        draw.text(
            xy,
            str(text),
            font=font,
            fill=fill,
            anchor=anchor,
            direction="rtl",
            language="fa"
        )

    except Exception:

        draw.text(
            xy,
            str(text),
            font=font,
            fill=fill,
            anchor=anchor
        )


# ============================================================
# FIT PERSIAN TEXT
# ============================================================

def draw_team_name(
    draw,
    xy,
    text,
    max_width,
    max_size=28,
    min_size=17,
    fill=(20, 25, 35)
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

        try:

            box = draw.textbbox(
                (0, 0),
                str(text),
                font=font,
                direction="rtl",
                language="fa"
            )

        except Exception:

            box = draw.textbbox(
                (0, 0),
                str(text),
                font=font
            )

        w = box[2] - box[0]

        if w <= max_width:

            draw_persian(
                draw,
                xy,
                text,
                font,
                fill
            )

            return

    draw_persian(
        draw,
        xy,
        text,
        get_font(
            min_size,
            bold=True
        ),
        fill
    )


# ============================================================
# DOWNLOAD LOGO
# ============================================================

logo_cache = {}


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
                "Logo HTTP:",
                response.status_code
            )
            return None

        logo = Image.open(
            BytesIO(response.content)
        ).convert("RGBA")

        logo.thumbnail(
            (82, 82),
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
# MATCH TIME - TEHRAN
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

    except Exception:

        return "--:--"


# ============================================================
# TODAY IN TEHRAN
# ============================================================

def get_today():

    return datetime.now(
        TEHRAN
    ).date()


# ============================================================
# GET MATCHES
# ============================================================

def get_matches(
    competition,
    today
):

    url = API_URL.format(
        competition
    )

    headers = {
        "X-Auth-Token":
        FOOTBALL_API_TOKEN
    }

    # یک روز قبل تا امروز را می‌گیریم
    # تا بازی‌های نزدیک نیمه‌شب UTC از دست نروند.

    date_from = (
        today - timedelta(days=1)
    ).isoformat()

    date_to = today.isoformat()

    params = {
        "dateFrom": date_from,
        "dateTo": date_to
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
                "Rate limit - waiting 45 seconds..."
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

        matches = data.get(
            "matches",
            []
        )

        # فقط بازی‌هایی که واقعاً در تاریخ امروز تهران هستند
        result = []

        for match in matches:

            utc_date = match.get(
                "utcDate"
            )

            if not utc_date:
                continue

            try:

                dt = datetime.fromisoformat(
                    utc_date.replace(
                        "Z",
                        "+00:00"
                    )
                )

                tehran_date = (
                    dt.astimezone(
                        TEHRAN
                    ).date()
                )

                if tehran_date == today:

                    result.append(
                        match
                    )

            except Exception:

                continue

        return result

    except Exception as e:

        print(
            "API error:",
            competition,
            e
        )

        return []


# ============================================================
# PLACE LOGO
# ============================================================

def paste_logo(
    image,
    logo,
    center_x,
    center_y
):

    if not logo:
        return

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
# DRAW MATCH CARD
# ============================================================

def draw_match_card(
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
        home_data.get(
            "crest"
        )
    )

    away_logo = download_logo(
        away_data.get(
            "crest"
        )
    )

    # --------------------------------------------------------
    # CARD SHADOW
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            x + 4,
            y + 5,
            x + width + 4,
            y + height + 5
        ),
        radius=22,
        fill=(5, 20, 35)
    )

    # --------------------------------------------------------
    # WHITE CARD
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + height
        ),
        radius=22,
        fill=(255, 255, 255),
        outline=(220, 226, 232),
        width=2
    )

    center_y = y + height // 2

    # --------------------------------------------------------
    # LOGO BACKGROUND CIRCLES
    # --------------------------------------------------------

    home_logo_x = x + width - 60
    away_logo_x = x + 60

    draw.ellipse(
        (
            home_logo_x - 47,
            center_y - 47,
            home_logo_x + 47,
            center_y + 47
        ),
        fill=(248, 249, 250)
    )

    draw.ellipse(
        (
            away_logo_x - 47,
            center_y - 47,
            away_logo_x + 47,
            center_y + 47
        ),
        fill=(248, 249, 250)
    )

    # --------------------------------------------------------
    # LOGOS
    # --------------------------------------------------------

    paste_logo(
        image,
        home_logo,
        home_logo_x,
        center_y
    )

    paste_logo(
        image,
        away_logo,
        away_logo_x,
        center_y
    )

    # --------------------------------------------------------
    # TEAM NAMES
    # --------------------------------------------------------

    draw_team_name(
        draw,
        (
            x + width - 175,
            center_y
        ),
        home,
        150,
        max_size=27,
        min_size=16
    )

    draw_team_name(
        draw,
        (
            x + 175,
            center_y
        ),
        away,
        150,
        max_size=27,
        min_size=16
    )

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    time_text = get_match_time(
        match
    )

    box_width = 100
    box_height = 52

    cx = x + width // 2

    draw.rounded_rectangle(
        (
            cx - box_width // 2,
            center_y - box_height // 2,
            cx + box_width // 2,
            center_y + box_height // 2
        ),
        radius=16,
        fill=(235, 248, 241),
        outline=(30, 180, 110),
        width=2
    )

    time_font = get_font(
        27,
        bold=True
    )

    draw.text(
        (
            cx,
            center_y
        ),
        time_text,
        font=time_font,
        fill=(15, 125, 78),
        anchor="mm"
    )

    # خط VS بسیار ظریف
    vs_font = get_font(
        13,
        bold=True
    )

    draw.text(
        (
            cx,
            center_y + 36
        ),
        "VS",
        font=vs_font,
        fill=(150, 155, 162),
        anchor="mm"
    )


# ============================================================
# DRAW LEAGUE
# ============================================================

def draw_league(
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
        (40, 90, 150)
    )

    league_name = COMPETITIONS.get(
        code,
        "مسابقات"
    )

    header_height = 58
    card_height = 112
    gap = 10

    # --------------------------------------------------------
    # LEAGUE HEADER
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + header_height
        ),
        radius=20,
        fill=color
    )

    league_font = get_font(
        25,
        bold=True
    )

    draw_persian(
        draw,
        (
            x + width // 2,
            y + header_height // 2
        ),
        league_name,
        league_font,
        (255, 255, 255)
    )

    # --------------------------------------------------------
    # MATCHES
    # --------------------------------------------------------

    current_y = (
        y
        + header_height
        + gap
    )

    for match in matches:

        draw_match_card(
            image,
            draw,
            match,
            x,
            current_y,
            width,
            card_height
        )

        current_y += (
            card_height
            + gap
        )

    return current_y - y + 8


# ============================================================
# CREATE FINAL IMAGE
# ============================================================

def create_matches_image(
    matches,
    today
):

    WIDTH = 1200

    SIDE = 35

    COLUMN_GAP = 25

    COLUMN_WIDTH = (
        WIDTH
        - SIDE * 2
        - COLUMN_GAP
    ) // 2

    HEADER_HEIGHT = 255

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

    # --------------------------------------------------------
    # SORT MATCHES
    # --------------------------------------------------------

    for code in grouped:

        grouped[code].sort(
            key=lambda m:
            m.get(
                "utcDate",
                ""
            )
        )

    # --------------------------------------------------------
    # SPLIT LEAGUES INTO TWO COLUMNS
    # --------------------------------------------------------

    left = []
    right = []

    left_height = 0
    right_height = 0

    for code in COMPETITIONS:

        if code not in grouped:
            continue

        count = len(
            grouped[code]
        )

        estimated_height = (
            58
            + 10
            + count
            * (112 + 10)
            + 8
        )

        if left_height <= right_height:

            left.append(
                (
                    code,
                    grouped[code]
                )
            )

            left_height += (
                estimated_height
            )

        else:

            right.append(
                (
                    code,
                    grouped[code]
                )
            )

            right_height += (
                estimated_height
            )

    content_height = max(
        left_height,
        right_height
    )

    height = (
        HEADER_HEIGHT
        + content_height
        + 50
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
        (7, 30, 52)
    )

    draw = ImageDraw.Draw(
        image
    )

    # --------------------------------------------------------
    # DARK BLUE GRADIENT
    # --------------------------------------------------------

    for yy in range(height):

        ratio = yy / max(
            height - 1,
            1
        )

        r = int(
            6 + 10 * ratio
        )

        g = int(
            28 + 28 * ratio
        )

        b = int(
            50 + 25 * ratio
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
    # DECORATIVE DIAGONAL LINES
    # --------------------------------------------------------

    for xx in range(
        -300,
        WIDTH + 300,
        90
    ):

        draw.line(
            (
                xx,
                0,
                xx + 180,
                180
            ),
            fill=(20, 65, 88),
            width=2
        )

    # --------------------------------------------------------
    # MAIN HEADER
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            30,
            25,
            WIDTH - 30,
            HEADER_HEIGHT - 20
        ),
        radius=35,
        fill=(7, 24, 44),
        outline=(30, 215, 125),
        width=3
    )

    # --------------------------------------------------------
    # GREEN TOP LINE
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            160,
            25,
            WIDTH - 160,
            37
        ),
        radius=6,
        fill=(30, 220, 125)
    )

    # --------------------------------------------------------
    # FOOTBALL ICON
    # --------------------------------------------------------

    bx = 165
    by = 100

    draw.ellipse(
        (
            bx - 48,
            by - 48,
            bx + 48,
            by + 48
        ),
        fill=(250, 250, 250),
        outline=(205, 212, 218),
        width=3
    )

    # توپ ساده
    draw.polygon(
        [
            (bx, by - 18),
            (bx + 17, by - 6),
            (bx + 11, by + 14),
            (bx - 11, by + 14),
            (bx - 17, by - 6)
        ],
        fill=(30, 45, 55)
    )

    draw.line(
        (
            bx,
            by - 18,
            bx,
            by - 36
        ),
        fill=(30, 45, 55),
        width=3
    )

    draw.line(
        (
            bx + 17,
            by - 6,
            bx + 35,
            by - 20
        ),
        fill=(30, 45, 55),
        width=3
    )

    draw.line(
        (
            bx + 11,
            by + 14,
            bx + 25,
            by + 30
        ),
        fill=(30, 45, 55),
        width=3
    )

    draw.line(
        (
            bx - 11,
            by + 14,
            bx - 25,
            by + 30
        ),
        fill=(30, 45, 55),
        width=3
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title_font = get_font(
        55,
        bold=True
    )

    draw_persian(
        draw,
        (
            WIDTH // 2 + 30,
            82
        ),
        "بازی‌های امروز",
        title_font,
        (255, 255, 255)
    )

    # --------------------------------------------------------
    # SUBTITLE
    # --------------------------------------------------------

    subtitle_font = get_font(
        31,
        bold=True
    )

    draw_persian(
        draw,
        (
            WIDTH // 2 + 20,
            145
        ),
        "۹ لیگ معتبر",
        subtitle_font,
        (30, 225, 125)
    )

    # --------------------------------------------------------
    # TEHRAN TIME
    # --------------------------------------------------------

    time_font = get_font(
        25,
        bold=True
    )

    draw_persian(
        draw,
        (
            WIDTH // 2 + 20,
            193
        ),
        "زمان‌ها به وقت تهران",
        time_font,
        (225, 232, 238)
    )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    date_font = get_font(
        20,
        bold=False
    )

    draw.text(
        (
            WIDTH // 2 + 20,
            225
        ),
        today.isoformat(),
        font=date_font,
        fill=(145, 165, 180),
        anchor="mm"
    )

    # --------------------------------------------------------
    # COLUMNS
    # --------------------------------------------------------

    left_x = SIDE

    right_x = (
        SIDE
        + COLUMN_WIDTH
        + COLUMN_GAP
    )

    left_y = HEADER_HEIGHT

    right_y = HEADER_HEIGHT

    # ستون چپ
    for code, league_matches in left:

        block_height = draw_league(
            image,
            draw,
            code,
            league_matches,
            left_x,
            left_y,
            COLUMN_WIDTH
        )

        left_y += block_height

    # ستون راست
    for code, league_matches in right:

        block_height = draw_league(
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
    # FOOTER LINE
    # --------------------------------------------------------

    footer_y = height - 25

    draw.line(
        (
            120,
            footer_y,
            WIDTH - 120,
            footer_y
        ),
        fill=(30, 215, 125),
        width=3
    )

    return image


# ============================================================
# SEND PHOTO TO TELEGRAM
# ============================================================

def send_matches_image(
    matches,
    today
):

    try:

        image = create_matches_image(
            matches,
            today
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
            "Telegram photo:",
            response.status_code
        )

        print(
            response.text
        )

        return response.ok

    except Exception as e:

        print(
            "IMAGE ERROR:",
            e
        )

        return False


# ============================================================
# SEND TEXT
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
            "Telegram error:",
            e
        )

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "======================================"
    )

    print(
        "FOOTBALL ALERT BOT"
    )

    print(
        "======================================"
    )

    # بررسی Secrets
    missing = []

    if not BOT_TOKEN:
        missing.append(
            "BOT_TOKEN"
        )

    if not CHAT_ID:
        missing.append(
            "CHAT_ID"
        )

    if not FOOTBALL_API_TOKEN:
        missing.append(
            "FOOTBALL_API_TOKEN"
        )

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
    # SORT ALL MATCHES
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
            f"📅 {today.isoformat()}"
        )

        return

    # --------------------------------------------------------
    # SEND ONE IMAGE
    # --------------------------------------------------------

    if send_matches_image(
        all_matches,
        today
    ):

        print(
            "======================================"
        )

        print(
            "SUCCESS - DAILY IMAGE SENT"
        )

        print(
            "======================================"
        )

    else:

        print(
            "Could not send image."
        )

        send_message(
            "⚽ بازی‌های امروز\n"
            f"📅 {today.isoformat()}\n"
            f"تعداد بازی‌ها: {len(all_matches)}"
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
