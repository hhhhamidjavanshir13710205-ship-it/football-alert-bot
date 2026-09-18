# -*- coding: utf-8 -*-

import os
import time
import requests

from io import BytesIO
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ============================================================
# SETTINGS
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

TEHRAN = ZoneInfo("Asia/Tehran")

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


LEAGUE_COLORS = {
    "PL": (126, 48, 190),
    "PD": (225, 10, 62),
    "SA": (10, 112, 215),
    "BL1": (48, 55, 66),
    "FL1": (25, 115, 205),
    "DED": (244, 103, 5),
    "PPL": (0, 150, 105),
    "BSA": (0, 120, 80),
    "CL": (65, 80, 210),
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
# PERSIAN DRAW
# ============================================================

def draw_fa(
    draw,
    position,
    text,
    font,
    fill,
    anchor="mm"
):

    try:

        draw.text(
            position,
            str(text),
            font=font,
            fill=fill,
            anchor=anchor,
            direction="rtl",
            language="fa"
        )

    except Exception:

        draw.text(
            position,
            str(text),
            font=font,
            fill=fill,
            anchor=anchor
        )


# ============================================================
# PERSIAN NUMBERS
# ============================================================

def persian_digits(value):

    table = str.maketrans(
        "0123456789",
        "۰۱۲۳۴۵۶۷۸۹"
    )

    return str(value).translate(table)


# ============================================================
# LOGO CACHE
# ============================================================

logo_cache = {}


def get_logo(url):

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
            BytesIO(
                response.content
            )
        ).convert("RGBA")

        logo.thumbnail(
            (150, 150),
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
# API
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

    params = {
        "dateFrom":
        (
            today - timedelta(days=1)
        ).isoformat(),

        "dateTo":
        today.isoformat()
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
            "HTTP:",
            response.status_code
        )

        if response.status_code == 429:

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

        today_matches = []

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

                local_date = (
                    dt.astimezone(
                        TEHRAN
                    ).date()
                )

                if local_date == today:

                    match[
                        "league_code"
                    ] = competition

                    today_matches.append(
                        match
                    )

            except Exception:
                continue

        return today_matches

    except Exception as e:

        print(
            "API ERROR:",
            competition,
            e
        )

        return []


# ============================================================
# LOGO PLACEHOLDER
# ============================================================

def placeholder(
    draw,
    cx,
    cy,
    name
):

    draw.ellipse(
        (
            cx - 57,
            cy - 57,
            cx + 57,
            cy + 57
        ),
        fill=(245, 248, 250),
        outline=(220, 226, 232),
        width=3
    )

    draw_fa(
        draw,
        (
            cx,
            cy
        ),
        str(name)[:1],
        get_font(
            38,
            bold=True
        ),
        (30, 120, 90)
    )


# ============================================================
# PASTE LOGO
# ============================================================

def paste_logo(
    image,
    logo,
    cx,
    cy
):

    if logo is None:
        return

    logo = logo.copy()

    logo.thumbnail(
        (120, 120),
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
        (
            x,
            y
        ),
        logo
    )


# ============================================================
# TEAM TEXT
# ============================================================

def team_text(
    draw,
    center,
    text,
    max_width=280
):

    for size in range(
        39,
        20,
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

        width = box[2] - box[0]

        if width <= max_width:

            draw_fa(
                draw,
                center,
                text,
                font,
                (15, 21, 29)
            )

            return


# ============================================================
# MATCH CARD
# ============================================================

def match_card(
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

    home_logo = get_logo(
        home_data.get(
            "crest"
        )
    )

    away_logo = get_logo(
        away_data.get(
            "crest"
        )
    )

    # --------------------------------------------------------
    # SHADOW
    # --------------------------------------------------------

    shadow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    sd = ImageDraw.Draw(
        shadow
    )

    sd.rounded_rectangle(
        (
            x + 10,
            y + 12,
            x + width + 10,
            y + height + 12
        ),
        radius=32,
        fill=(0, 0, 0, 110)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(12)
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
        radius=32,
        fill=(250, 252, 254),
        outline=(220, 227, 234),
        width=3
    )

    # top shine
    draw.rounded_rectangle(
        (
            x + 35,
            y + 12,
            x + width - 35,
            y + 18
        ),
        radius=4,
        fill=(235, 240, 244)
    )

    center_y = (
        y + height // 2
    )

    # --------------------------------------------------------
    # LOGO POSITIONS
    # --------------------------------------------------------

    home_x = x + width - 100
    away_x = x + 100

    # logo background
    for logo_x in (
        home_x,
        away_x
    ):

        draw.ellipse(
            (
                logo_x - 68,
                center_y - 68,
                logo_x + 68,
                center_y + 68
            ),
            fill=(247, 249, 251),
            outline=(229, 234, 239),
            width=3
        )

    # --------------------------------------------------------
    # LOGOS
    # --------------------------------------------------------

    if home_logo:

        paste_logo(
            image,
            home_logo,
            home_x,
            center_y
        )

    else:

        placeholder(
            draw,
            home_x,
            center_y,
            home
        )

    if away_logo:

        paste_logo(
            image,
            away_logo,
            away_x,
            center_y
        )

    else:

        placeholder(
            draw,
            away_x,
            center_y,
            away
        )

    # --------------------------------------------------------
    # TEAM NAMES
    # --------------------------------------------------------

    team_text(
        draw,
        (
            x + width - 300,
            center_y
        ),
        home,
        260
    )

    team_text(
        draw,
        (
            x + 300,
            center_y
        ),
        away,
        260
    )

    # --------------------------------------------------------
    # TIME BADGE SHADOW
    # --------------------------------------------------------

    cx = x + width // 2

    draw.rounded_rectangle(
        (
            cx - 83,
            center_y - 37,
            cx + 83,
            center_y + 37
        ),
        radius=23,
        fill=(207, 217, 224)
    )

    # --------------------------------------------------------
    # TIME BADGE
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            cx - 80,
            center_y - 40,
            cx + 80,
            center_y + 40
        ),
        radius=23,
        fill=(236, 250, 243),
        outline=(40, 195, 125),
        width=4
    )

    draw.text(
        (
            cx,
            center_y
        ),
        get_match_time(match),
        font=get_font(
            39,
            bold=True
        ),
        fill=(12, 132, 82),
        anchor="mm"
    )

    # --------------------------------------------------------
    # VS
    # --------------------------------------------------------

    draw.text(
        (
            cx,
            center_y + 58
        ),
        "VS",
        font=get_font(
            17,
            bold=True
        ),
        fill=(145, 153, 162),
        anchor="mm"
    )


# ============================================================
# LEAGUE BLOCK
# ============================================================

def league_block(
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
        (40, 100, 170)
    )

    league = COMPETITIONS.get(
        code,
        "مسابقات"
    )

    HEADER = 82
    CARD = 175
    GAP = 22

    # --------------------------------------------------------
    # LEAGUE HEADER SHADOW
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            x + 7,
            y + 9,
            x + width + 7,
            y + HEADER + 9
        ),
        radius=29,
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
            y + HEADER
        ),
        radius=29,
        fill=color
    )

    # upper highlight
    draw.rounded_rectangle(
        (
            x + 35,
            y + 9,
            x + width - 35,
            y + 16
        ),
        radius=4,
        fill=(
            min(color[0] + 40, 255),
            min(color[1] + 40, 255),
            min(color[2] + 40, 255)
        )
    )

    # league title
    draw_fa(
        draw,
        (
            x + width // 2,
            y + HEADER // 2 + 2
        ),
        league,
        get_font(
            36,
            bold=True
        ),
        (255, 255, 255)
    )

    current = (
        y
        + HEADER
        + GAP
    )

    for match in matches:

        match_card(
            image,
            draw,
            match,
            x,
            current,
            width,
            CARD
        )

        current += (
            CARD
            + GAP
        )

    return current - y


# ============================================================
# CREATE IMAGE
# ============================================================

def create_image(
    matches,
    today
):

    WIDTH = 2000

    SIDE = 70
    COLUMN_GAP = 45

    COLUMN_WIDTH = (
        WIDTH
        - (SIDE * 2)
        - COLUMN_GAP
    ) // 2

    HEADER_HEIGHT = 410

    # --------------------------------------------------------
    # GROUP
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

    # --------------------------------------------------------
    # BALANCE COLUMNS
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

        estimated = (
            82
            + 22
            + count * (
                175 + 22
            )
        )

        if left_height <= right_height:

            left.append(
                (
                    code,
                    grouped[code]
                )
            )

            left_height += estimated

        else:

            right.append(
                (
                    code,
                    grouped[code]
                )
            )

            right_height += estimated

    content_height = max(
        left_height,
        right_height
    )

    HEIGHT = (
        HEADER_HEIGHT
        + content_height
        + 110
    )

    # --------------------------------------------------------
    # BASE
    # --------------------------------------------------------

    image = Image.new(
        "RGB",
        (
            WIDTH,
            HEIGHT
        )
    )

    draw = ImageDraw.Draw(
        image
    )

    # --------------------------------------------------------
    # PREMIUM GRADIENT
    # --------------------------------------------------------

    for y in range(
        HEIGHT
    ):

        ratio = y / max(
            HEIGHT - 1,
            1
        )

        r = int(
            4 + ratio * 7
        )

        g = int(
            21 + ratio * 26
        )

        b = int(
            38 + ratio * 35
        )

        draw.line(
            (
                0,
                y,
                WIDTH,
                y
            ),
            fill=(r, g, b)
        )

    # --------------------------------------------------------
    # DIAGONAL SPORT LINES
    # --------------------------------------------------------

    for start in range(
        -700,
        WIDTH + 700,
        145
    ):

        draw.line(
            (
                start,
                0,
                start + 320,
                320
            ),
            fill=(14, 50, 73),
            width=3
        )

    # --------------------------------------------------------
    # DECORATIVE GREEN GLOW
    # --------------------------------------------------------

    glow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    gd = ImageDraw.Draw(
        glow
    )

    gd.ellipse(
        (
            -400,
            250,
            400,
            1150
        ),
        fill=(0, 220, 140, 38)
    )

    gd.ellipse(
        (
            WIDTH - 400,
            500,
            WIDTH + 350,
            1250
        ),
        fill=(30, 100, 240, 30)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(130)
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
            48,
            48,
            WIDTH - 48,
            HEADER_HEIGHT - 20
        ),
        radius=52,
        fill=(0, 0, 0)
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            35,
            30,
            WIDTH - 35,
            HEADER_HEIGHT - 32
        ),
        radius=52,
        fill=(5, 23, 41),
        outline=(38, 225, 135),
        width=5
    )

    # --------------------------------------------------------
    # GREEN TOP BAR
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            260,
            30,
            WIDTH - 260,
            51
        ),
        radius=10,
        fill=(35, 228, 135)
    )

    # --------------------------------------------------------
    # FOOTBALL ICON
    # --------------------------------------------------------

    bx = 185
    by = 165

    draw.ellipse(
        (
            bx - 72,
            by - 72,
            bx + 72,
            by + 72
        ),
        fill=(248, 250, 252),
        outline=(208, 216, 222),
        width=4
    )

    # football center
    draw.polygon(
        [
            (bx, by - 32),
            (bx + 31, by - 10),
            (bx + 19, by + 27),
            (bx - 19, by + 27),
            (bx - 31, by - 10)
        ],
        fill=(16, 35, 50)
    )

    for px, py in [
        (bx, by - 32),
        (bx + 31, by - 10),
        (bx + 19, by + 27),
        (bx - 19, by + 27),
        (bx - 31, by - 10)
    ]:

        draw.line(
            (
                bx,
                by,
                px,
                py
            ),
            fill=(16, 35, 50),
            width=5
        )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    draw_fa(
        draw,
        (
            WIDTH // 2 + 45,
            120
        ),
        "بازی‌های امروز",
        get_font(
            82,
            bold=True
        ),
        (255, 255, 255)
    )

    # --------------------------------------------------------
    # SUBTITLE
    # --------------------------------------------------------

    draw_fa(
        draw,
        (
            WIDTH // 2 + 40,
            215
        ),
        "۹ لیگ معتبر",
        get_font(
            45,
            bold=True
        ),
        (35, 228, 135)
    )

    # --------------------------------------------------------
    # TEHRAN
    # --------------------------------------------------------

    draw_fa(
        draw,
        (
            WIDTH // 2 + 40,
            285
        ),
        "زمان‌ها به وقت تهران",
        get_font(
            36,
            bold=True
        ),
        (235, 243, 248)
    )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    draw.text(
        (
            WIDTH // 2 + 40,
            340
        ),
        today.isoformat(),
        font=get_font(
            27
        ),
        fill=(150, 174, 188),
        anchor="mm"
    )

    # --------------------------------------------------------
    # MATCH COUNT
    # --------------------------------------------------------

    draw_fa(
        draw,
        (
            WIDTH - 190,
            340
        ),
        f"{persian_digits(len(matches))} بازی",
        get_font(
            27,
            bold=True
        ),
        (35, 228, 135)
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

    for code, league_matches in left:

        h = league_block(
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

        h = league_block(
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

    footer_y = HEIGHT - 45

    draw.line(
        (
            170,
            footer_y,
            WIDTH - 170,
            footer_y
        ),
        fill=(35, 228, 135),
        width=5
    )

    draw_fa(
        draw,
        (
            WIDTH // 2,
            footer_y + 28
        ),
        "Football Alert",
        get_font(
            20,
            bold=True
        ),
        (125, 150, 165)
    )

    return image


# ============================================================
# TELEGRAM IMAGE
# ============================================================

def send_image(
    matches,
    today
):

    try:

        image = create_image(
            matches,
            today
        )

        buffer = BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=97,
            optimize=True,
            subsampling=0
        )

        buffer.seek(0)

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
                    buffer,
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
            "SEND IMAGE ERROR:",
            e
        )

        return False


# ============================================================
# TEXT FALLBACK
# ============================================================

def send_text(text):

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
            "TEXT ERROR:",
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
        "FOOTBALL ALERT - PREMIUM GRAPHICS"
    )

    print(
        "========================================"
    )

    missing = []

    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")

    if not CHAT_ID:
        missing.append("CHAT_ID")

    if not FOOTBALL_API_TOKEN:
        missing.append(
            "FOOTBALL_API_TOKEN"
        )

    if missing:

        print(
            "Missing:",
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
    # FETCH 9 LEAGUES
    # --------------------------------------------------------

    for code in COMPETITIONS:

        matches = get_matches(
            code,
            today
        )

        all_matches.extend(
            matches
        )

    # --------------------------------------------------------
    # SORT BY TIME
    # --------------------------------------------------------

    all_matches.sort(
        key=lambda x:
        x.get(
            "utcDate",
            ""
        )
    )

    print(
        "TOTAL:",
        len(all_matches)
    )

    # --------------------------------------------------------
    # NO MATCHES
    # --------------------------------------------------------

    if not all_matches:

        send_text(
            "⚽ بازی‌ای برای امروز پیدا نشد.\n"
            f"📅 {today.isoformat()}"
        )

        return

    # --------------------------------------------------------
    # SEND ONE IMAGE
    # --------------------------------------------------------

    if send_image(
        all_matches,
        today
    ):

        print(
            "IMAGE SENT SUCCESSFULLY"
        )

    else:

        print(
            "IMAGE SEND FAILED"
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
