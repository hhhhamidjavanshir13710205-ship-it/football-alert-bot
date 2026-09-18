# -*- coding: utf-8 -*-

import os
import time
import requests

from io import BytesIO
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ============================================================
# CONFIG
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

TEHRAN = ZoneInfo("Asia/Tehran")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"


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
    "PL": (125, 45, 190),
    "PD": (225, 0, 60),
    "SA": (0, 125, 220),
    "BL1": (40, 48, 58),
    "FL1": (15, 110, 205),
    "DED": (245, 105, 0),
    "PPL": (0, 155, 95),
    "BSA": (0, 125, 75),
    "CL": (50, 75, 210),
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
                return ImageFont.truetype(
                    path,
                    size
                )

            except Exception:
                pass

    return ImageFont.load_default()


# ============================================================
# PERSIAN TEXT
# ============================================================

def draw_fa(
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
# PERSIAN DIGITS
# ============================================================

def persian_digits(text):

    table = str.maketrans(
        "0123456789",
        "۰۱۲۳۴۵۶۷۸۹"
    )

    return str(text).translate(table)


# ============================================================
# FIT TEAM NAME
# ============================================================

def draw_team_name(
    draw,
    center,
    text,
    max_width,
    max_size=34,
    min_size=20
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

            bbox = draw.textbbox(
                (0, 0),
                str(text),
                font=font,
                direction="rtl",
                language="fa"
            )

        except Exception:

            bbox = draw.textbbox(
                (0, 0),
                str(text),
                font=font
            )

        width = bbox[2] - bbox[0]

        if width <= max_width:

            draw_fa(
                draw,
                center,
                text,
                font,
                (15, 20, 28)
            )

            return

    draw_fa(
        draw,
        center,
        text,
        get_font(
            min_size,
            bold=True
        ),
        (15, 20, 28)
    )


# ============================================================
# LOGO CACHE
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
            BytesIO(
                response.content
            )
        ).convert("RGBA")

        logo.thumbnail(
            (120, 120),
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

        tehran = dt.astimezone(
            TEHRAN
        )

        return persian_digits(
            tehran.strftime(
                "%H:%M"
            )
        )

    except Exception:

        return "--:--"


# ============================================================
# GET TODAY
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
                "Rate limit. Waiting..."
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
            "API ERROR:",
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
    cx,
    cy,
    size=110
):

    if logo is None:
        return

    logo = logo.copy()

    logo.thumbnail(
        (size, size),
        Image.Resampling.LANCZOS
    )

    x = int(
        cx - logo.width / 2
    )

    y = int(
        cy - logo.height / 2
    )

    image.paste(
        logo,
        (x, y),
        logo
    )


# ============================================================
# PLACEHOLDER LOGO
# ============================================================

def draw_placeholder(
    draw,
    cx,
    cy,
    color,
    text
):

    radius = 48

    draw.ellipse(
        (
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius
        ),
        fill=(244, 247, 250),
        outline=(220, 225, 230),
        width=2
    )

    letter = str(text)[:1]

    draw_fa(
        draw,
        (cx, cy),
        letter,
        get_font(
            32,
            bold=True
        ),
        color
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
        home_data.get("crest")
    )

    away_logo = download_logo(
        away_data.get("crest")
    )

    # --------------------------------------------------------
    # SHADOW
    # --------------------------------------------------------

    shadow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    shadow_draw = ImageDraw.Draw(
        shadow
    )

    shadow_draw.rounded_rectangle(
        (
            x + 8,
            y + 10,
            x + width + 8,
            y + height + 10
        ),
        radius=28,
        fill=(0, 0, 0, 100)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(8)
    )

    image.paste(
        shadow,
        (0, 0),
        shadow
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
        radius=28,
        fill=(250, 252, 253),
        outline=(220, 228, 235),
        width=2
    )

    # --------------------------------------------------------
    # TOP LIGHT STRIPE
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            x + 25,
            y + 12,
            x + width - 25,
            y + 17
        ),
        radius=3,
        fill=(235, 239, 243)
    )

    center_y = y + height // 2

    # --------------------------------------------------------
    # LOGO POSITIONS
    # --------------------------------------------------------

    home_x = x + width - 85
    away_x = x + 85

    # Logo circles
    for logo_x in [home_x, away_x]:

        draw.ellipse(
            (
                logo_x - 61,
                center_y - 61,
                logo_x + 61,
                center_y + 61
            ),
            fill=(247, 249, 251),
            outline=(230, 235, 240),
            width=2
        )

    # --------------------------------------------------------
    # LOGOS
    # --------------------------------------------------------

    if home_logo:

        paste_logo(
            image,
            home_logo,
            home_x,
            center_y,
            105
        )

    else:

        draw_placeholder(
            draw,
            home_x,
            center_y,
            (40, 130, 90),
            home
        )

    if away_logo:

        paste_logo(
            image,
            away_logo,
            away_x,
            center_y,
            105
        )

    else:

        draw_placeholder(
            draw,
            away_x,
            center_y,
            (40, 130, 90),
            away
        )

    # --------------------------------------------------------
    # TEAM NAMES
    # --------------------------------------------------------

    draw_team_name(
        draw,
        (
            x + width - 245,
            center_y
        ),
        home,
        220,
        max_size=34,
        min_size=19
    )

    draw_team_name(
        draw,
        (
            x + 245,
            center_y
        ),
        away,
        220,
        max_size=34,
        min_size=19
    )

    # --------------------------------------------------------
    # TIME PILL
    # --------------------------------------------------------

    cx = x + width // 2

    pill_w = 135
    pill_h = 65

    draw.rounded_rectangle(
        (
            cx - pill_w // 2,
            center_y - pill_h // 2,
            cx + pill_w // 2,
            center_y + pill_h // 2
        ),
        radius=20,
        fill=(236, 250, 243),
        outline=(35, 190, 120),
        width=3
    )

    time_font = get_font(
        34,
        bold=True
    )

    draw.text(
        (
            cx,
            center_y
        ),
        get_match_time(match),
        font=time_font,
        fill=(13, 130, 82),
        anchor="mm"
    )

    # --------------------------------------------------------
    # VS
    # --------------------------------------------------------

    draw.text(
        (
            cx,
            center_y + 48
        ),
        "VS",
        font=get_font(
            15,
            bold=True
        ),
        fill=(155, 163, 172),
        anchor="mm"
    )


# ============================================================
# DRAW LEAGUE BLOCK
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
        (50, 100, 170)
    )

    league_name = COMPETITIONS.get(
        code,
        "مسابقات"
    )

    header_h = 72
    card_h = 150
    gap = 18

    # --------------------------------------------------------
    # LEAGUE HEADER SHADOW
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            x + 5,
            y + 6,
            x + width + 5,
            y + header_h + 6
        ),
        radius=25,
        fill=(0, 0, 0)
    )

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
        radius=25,
        fill=color
    )

    # روشنایی بالای نوار
    draw.rounded_rectangle(
        (
            x + 25,
            y + 8,
            x + width - 25,
            y + 13
        ),
        radius=3,
        fill=(
            min(color[0] + 35, 255),
            min(color[1] + 35, 255),
            min(color[2] + 35, 255)
        )
    )

    league_font = get_font(
        31,
        bold=True
    )

    draw_fa(
        draw,
        (
            x + width // 2,
            y + header_h // 2
        ),
        league_name,
        league_font,
        (255, 255, 255)
    )

    current_y = (
        y
        + header_h
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
            card_h
        )

        current_y += (
            card_h
            + gap
        )

    return current_y - y


# ============================================================
# CREATE PROFESSIONAL IMAGE
# ============================================================

def create_matches_image(
    matches,
    today
):

    # طراحی با رزولوشن بالا
    WIDTH = 1800

    SIDE = 55
    GAP = 35

    COLUMN_WIDTH = (
        WIDTH
        - SIDE * 2
        - GAP
    ) // 2

    HEADER_HEIGHT = 365

    # --------------------------------------------------------
    # GROUP LEAGUES
    # --------------------------------------------------------

    grouped = {}

    for match in matches:

        code = match.get(
            "league_code",
            ""
        )

        grouped.setdefault(
            code,
            []
        ).append(match)

    for code in grouped:

        grouped[code].sort(
            key=lambda x:
            x.get(
                "utcDate",
                ""
            )
        )

    # --------------------------------------------------------
    # BALANCE TWO COLUMNS
    # --------------------------------------------------------

    left = []
    right = []

    left_h = 0
    right_h = 0

    for code in COMPETITIONS:

        if code not in grouped:
            continue

        count = len(
            grouped[code]
        )

        estimated = (
            72
            + 18
            + count * (
                150 + 18
            )
        )

        if left_h <= right_h:

            left.append(
                (
                    code,
                    grouped[code]
                )
            )

            left_h += estimated

        else:

            right.append(
                (
                    code,
                    grouped[code]
                )
            )

            right_h += estimated

    content_h = max(
        left_h,
        right_h
    )

    HEIGHT = (
        HEADER_HEIGHT
        + content_h
        + 80
    )

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    image = Image.new(
        "RGB",
        (
            WIDTH,
            HEIGHT
        ),
        (5, 24, 43)
    )

    draw = ImageDraw.Draw(
        image
    )

    # --------------------------------------------------------
    # GRADIENT BACKGROUND
    # --------------------------------------------------------

    for yy in range(HEIGHT):

        ratio = yy / max(
            HEIGHT - 1,
            1
        )

        r = int(
            5 + 7 * ratio
        )

        g = int(
            25 + 30 * ratio
        )

        b = int(
            45 + 25 * ratio
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

    for xx in range(
        -500,
        WIDTH + 500,
        130
    ):

        draw.line(
            (
                xx,
                0,
                xx + 250,
                250
            ),
            fill=(15, 52, 76),
            width=3
        )

    # --------------------------------------------------------
    # DECORATIVE GLOW CIRCLES
    # --------------------------------------------------------

    glow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(
        glow
    )

    glow_draw.ellipse(
        (
            -300,
            500,
            300,
            1100
        ),
        fill=(0, 180, 130, 30)
    )

    glow_draw.ellipse(
        (
            WIDTH - 300,
            700,
            WIDTH + 250,
            1250
        ),
        fill=(20, 80, 220, 25)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(100)
    )

    image.paste(
        glow,
        (0, 0),
        glow
    )

    # --------------------------------------------------------
    # HEADER SHADOW
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            38,
            38,
            WIDTH - 38,
            HEADER_HEIGHT - 20
        ),
        radius=45,
        fill=(0, 0, 0)
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            30,
            25,
            WIDTH - 30,
            HEADER_HEIGHT - 30
        ),
        radius=45,
        fill=(6, 24, 43),
        outline=(35, 225, 130),
        width=4
    )

    # --------------------------------------------------------
    # GREEN TOP BAR
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            220,
            25,
            WIDTH - 220,
            42
        ),
        radius=8,
        fill=(30, 225, 130)
    )

    # --------------------------------------------------------
    # FOOTBALL ICON
    # --------------------------------------------------------

    bx = 190
    by = 145

    draw.ellipse(
        (
            bx - 65,
            by - 65,
            bx + 65,
            by + 65
        ),
        fill=(250, 252, 253),
        outline=(205, 215, 220),
        width=3
    )

    # توپ هندسی
    draw.polygon(
        [
            (bx, by - 28),
            (bx + 27, by - 8),
            (bx + 17, by + 23),
            (bx - 17, by + 23),
            (bx - 27, by - 8)
        ],
        fill=(20, 40, 55)
    )

    for ex, ey in [
        (bx, by - 28),
        (bx + 27, by - 8),
        (bx + 17, by + 23),
        (bx - 17, by + 23),
        (bx - 27, by - 8)
    ]:

        draw.line(
            (
                bx,
                by,
                ex,
                ey
            ),
            fill=(20, 40, 55),
            width=4
        )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title_font = get_font(
        70,
        bold=True
    )

    draw_fa(
        draw,
        (
            WIDTH // 2 + 35,
            105
        ),
        "بازی‌های امروز",
        title_font,
        (255, 255, 255)
    )

    # --------------------------------------------------------
    # SUBTITLE
    # --------------------------------------------------------

    subtitle_font = get_font(
        40,
        bold=True
    )

    draw_fa(
        draw,
        (
            WIDTH // 2 + 25,
            185
        ),
        "۹ لیگ معتبر",
        subtitle_font,
        (30, 225, 130)
    )

    # --------------------------------------------------------
    # TEHRAN
    # --------------------------------------------------------

    draw_fa(
        draw,
        (
            WIDTH // 2 + 25,
            245
        ),
        "زمان‌ها به وقت تهران",
        get_font(
            31,
            bold=True
        ),
        (235, 242, 247)
    )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    draw.text(
        (
            WIDTH // 2 + 25,
            295
        ),
        today.isoformat(),
        font=get_font(
            25
        ),
        fill=(145, 170, 185),
        anchor="mm"
    )

    # --------------------------------------------------------
    # MATCH COUNT
    # --------------------------------------------------------

    count_text = (
        f"{persian_digits(len(matches))} بازی امروز"
    )

    draw_fa(
        draw,
        (
            WIDTH - 170,
            295
        ),
        count_text,
        get_font(
            23,
            bold=True
        ),
        (30, 225, 130)
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

        h = draw_league(
            image,
            draw,
            code,
            league_matches,
            left_x,
            left_y,
            COLUMN_WIDTH
        )

        left_y += h

    for code, league_matches in right:

        h = draw_league(
            image,
            draw,
            code,
            league_matches,
            right_x,
            right_y,
            COLUMN_WIDTH
        )

        right_y += h

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    footer_y = HEIGHT - 35

    draw.line(
        (
            170,
            footer_y,
            WIDTH - 170,
            footer_y
        ),
        fill=(30, 225, 130),
        width=4
    )

    return image


# ============================================================
# SEND IMAGE
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
            quality=96,
            optimize=True,
            subsampling=0
        )

        output.seek(0)

        url = (
            "https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendPhoto"
        )

        caption = (
            "⚽ بازی‌های امروز\n"
            "🏆 ۹ لیگ معتبر\n"
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
                    "football_today.jpg",
                    output,
                    "image/jpeg"
                )
            },
            timeout=120
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
            "IMAGE SEND ERROR:",
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

        print(
            response.text
        )

        return response.ok

    except Exception as e:

        print(
            "TEXT ERROR:",
            e
        )

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "=========================================="
    )

    print(
        "FOOTBALL ALERT BOT - PROFESSIONAL DESIGN"
    )

    print(
        "=========================================="
    )

    # --------------------------------------------------------
    # CHECK SECRETS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # TODAY
    # --------------------------------------------------------

    today = get_today()

    print(
        "Tehran date:",
        today
    )

    all_matches = []

    # --------------------------------------------------------
    # CHECK 9 LEAGUES
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
            f"📅 {today.isoformat()}"
        )

        return

    # --------------------------------------------------------
    # SEND ONE PROFESSIONAL IMAGE
    # --------------------------------------------------------

    success = send_matches_image(
        all_matches,
        today
    )

    if success:

        print(
            "=========================================="
        )

        print(
            "SUCCESS - IMAGE SENT"
        )

        print(
            "=========================================="
        )

    else:

        print(
            "Image failed."
        )

        send_message(
            "⚽ بازی‌های امروز\n"
            f"📅 {today.isoformat()}\n"
            f"تعداد بازی‌ها: {len(all_matches)}"
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
