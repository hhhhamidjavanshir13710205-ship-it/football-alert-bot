# -*- coding: utf-8 -*-

import os
import requests

from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter,
)


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


# رنگ Accent هر لیگ
LEAGUE_ACCENT = {
    "PL": (125, 72, 210),
    "PD": (225, 55, 75),
    "SA": (30, 125, 220),
    "BL1": (230, 70, 70),
    "FL1": (50, 120, 225),
    "DED": (245, 125, 30),
    "PPL": (30, 165, 110),
    "BSA": (35, 155, 95),
    "CL": (80, 105, 230),
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

def font(size, bold=False):

    if bold:
        candidates = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for path in candidates:

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
# RTL TEXT
# ============================================================

def draw_rtl(
    draw,
    xy,
    text,
    fnt,
    fill,
    anchor="mm"
):

    try:

        draw.text(
            xy,
            str(text),
            font=fnt,
            fill=fill,
            anchor=anchor,
            direction="rtl",
            language="fa",
        )

    except:

        draw.text(
            xy,
            str(text),
            font=fnt,
            fill=fill,
            anchor=anchor,
        )


# ============================================================
# PERSIAN DIGITS
# ============================================================

def fa_digits(value):

    return str(value).translate(
        str.maketrans(
            "0123456789",
            "۰۱۲۳۴۵۶۷۸۹"
        )
    )


# ============================================================
# LOGO
# ============================================================

def download_logo(url):

    if not url:
        return None

    try:

        r = requests.get(
            url,
            timeout=20
        )

        if r.status_code != 200:
            return None

        img = Image.open(
            BytesIO(r.content)
        ).convert("RGBA")

        img.thumbnail(
            (170, 170),
            Image.Resampling.LANCZOS
        )

        return img

    except Exception as e:

        print(
            "Logo download error:",
            e
        )

        return None


# ============================================================
# MATCH TIME
# ============================================================

def match_time(match):

    raw = match.get(
        "utcDate"
    )

    if not raw:
        return "--:--"

    try:

        dt = datetime.fromisoformat(
            raw.replace(
                "Z",
                "+00:00"
            )
        )

        dt = dt.astimezone(
            TEHRAN
        )

        return fa_digits(
            dt.strftime("%H:%M")
        )

    except:

        return "--:--"


# ============================================================
# API
# ============================================================

def get_matches(
    code,
    today
):

    url = API_URL.format(code)

    headers = {
        "X-Auth-Token":
        FOOTBALL_API_TOKEN
    }

    params = {
        "dateFrom":
        today.isoformat(),

        "dateTo":
        today.isoformat(),
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        print(
            f"{code}: HTTP {response.status_code}"
        )

        if response.status_code != 200:

            print(
                response.text[:500]
            )

            return []

        data = response.json()

        result = []

        for match in data.get(
            "matches",
            []
        ):

            raw = match.get(
                "utcDate"
            )

            if not raw:
                continue

            try:

                dt = datetime.fromisoformat(
                    raw.replace(
                        "Z",
                        "+00:00"
                    )
                )

                local = dt.astimezone(
                    TEHRAN
                )

                if local.date() == today:

                    match[
                        "league_code"
                    ] = code

                    result.append(
                        match
                    )

            except:
                continue

        return result

    except Exception as e:

        print(
            f"{code} ERROR:",
            e
        )

        return []


# ============================================================
# FIT TEAM NAME
# ============================================================

def draw_team_name(
    draw,
    x,
    y,
    text,
    max_width
):

    for size in range(
        46,
        21,
        -1
    ):

        fnt = font(
            size,
            bold=True
        )

        try:

            box = draw.textbbox(
                (0, 0),
                str(text),
                font=fnt,
                direction="rtl",
                language="fa"
            )

        except:

            box = draw.textbbox(
                (0, 0),
                str(text),
                font=fnt
            )

        width = box[2] - box[0]

        if width <= max_width:

            draw_rtl(
                draw,
                (x, y),
                text,
                fnt,
                (20, 27, 37)
            )

            return


# ============================================================
# LOGO CIRCLE
# ============================================================

def draw_logo_area(
    image,
    draw,
    logo,
    x,
    y,
    accent,
    team
):

    # outer shadow
    shadow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    sd = ImageDraw.Draw(
        shadow
    )

    sd.ellipse(
        (
            x - 78 + 6,
            y - 78 + 8,
            x + 78 + 6,
            y + 78 + 8
        ),
        fill=(0, 0, 0, 70)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(9)
    )

    image.paste(
        shadow,
        (0, 0),
        shadow
    )

    # white logo plate
    draw.ellipse(
        (
            x - 78,
            y - 78,
            x + 78,
            y + 78
        ),
        fill=(255, 255, 255),
        outline=accent,
        width=4
    )

    if logo:

        logo = logo.copy()

        logo.thumbnail(
            (118, 118),
            Image.Resampling.LANCZOS
        )

        px = int(
            x - logo.width / 2
        )

        py = int(
            y - logo.height / 2
        )

        image.paste(
            logo,
            (
                px,
                py
            ),
            logo
        )

    else:

        draw.text(
            (
                x,
                y
            ),
            str(team)[:1],
            font=font(
                55,
                bold=True
            ),
            fill=accent,
            anchor="mm"
        )


# ============================================================
# MATCH CARD
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

    code = match.get(
        "league_code",
        ""
    )

    accent = LEAGUE_ACCENT.get(
        code,
        (30, 150, 100)
    )

    home_raw = match.get(
        "homeTeam",
        {}
    )

    away_raw = match.get(
        "awayTeam",
        {}
    )

    home_original = home_raw.get(
        "name",
        "میزبان"
    )

    away_original = away_raw.get(
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
            y + 15,
            x + width + 10,
            y + height + 15
        ),
        radius=38,
        fill=(0, 0, 0, 120)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(15)
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
        radius=38,
        fill=(247, 249, 251)
    )

    # accent line
    draw.rounded_rectangle(
        (
            x,
            y,
            x + 12,
            y + height
        ),
        radius=6,
        fill=accent
    )

    # --------------------------------------------------------
    # LEAGUE SMALL LABEL
    # --------------------------------------------------------

    league = COMPETITIONS.get(
        code,
        ""
    )

    draw.rounded_rectangle(
        (
            x + 35,
            y + 28,
            x + 365,
            y + 78
        ),
        radius=20,
        fill=(236, 240, 244)
    )

    draw_rtl(
        draw,
        (
            x + 200,
            y + 53
        ),
        league,
        font(
            23,
            bold=True
        ),
        (80, 91, 103)
    )

    # --------------------------------------------------------
    # CENTER
    # --------------------------------------------------------

    center_x = (
        x + width // 2
    )

    center_y = (
        y + 175
    )

    # --------------------------------------------------------
    # LOGOS
    # --------------------------------------------------------

    home_logo = download_logo(
        home_raw.get(
            "crest"
        )
    )

    away_logo = download_logo(
        away_raw.get(
            "crest"
        )
    )

    home_x = x + width - 230
    away_x = x + 230

    draw_logo_area(
        image,
        draw,
        home_logo,
        home_x,
        center_y,
        accent,
        home
    )

    draw_logo_area(
        image,
        draw,
        away_logo,
        away_x,
        center_y,
        accent,
        away
    )

    # --------------------------------------------------------
    # TEAM NAMES
    # --------------------------------------------------------

    draw_team_name(
        draw,
        home_x,
        y + 292,
        home,
        300
    )

    draw_team_name(
        draw,
        away_x,
        y + 292,
        away,
        300
    )

    # --------------------------------------------------------
    # TIME SHADOW
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            center_x - 112,
            center_y - 51,
            center_x + 112,
            center_y + 51
        ),
        radius=30,
        fill=(208, 216, 223)
    )

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            center_x - 108,
            center_y - 55,
            center_x + 108,
            center_y + 55
        ),
        radius=30,
        fill=(10, 34, 52),
        outline=accent,
        width=5
    )

    draw.text(
        (
            center_x,
            center_y
        ),
        match_time(match),
        font=font(
            50,
            bold=True
        ),
        fill=(255, 255, 255),
        anchor="mm"
    )

    # --------------------------------------------------------
    # VS
    # --------------------------------------------------------

    draw.text(
        (
            center_x,
            center_y + 76
        ),
        "VS",
        font=font(
            22,
            bold=True
        ),
        fill=(145, 154, 163),
        anchor="mm"
    )


# ============================================================
# PREMIUM POSTER
# ============================================================

def create_poster(
    matches,
    today
):

    WIDTH = 1600

    SIDE = 90

    CARD_WIDTH = (
        WIDTH - SIDE * 2
    )

    CARD_HEIGHT = 360

    CARD_GAP = 38

    HEADER = 470

    FOOTER = 130

    HEIGHT = (
        HEADER
        + len(matches) *
        (CARD_HEIGHT + CARD_GAP)
        + FOOTER
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
    # GRADIENT
    # --------------------------------------------------------

    for y in range(
        HEIGHT
    ):

        p = y / HEIGHT

        r = int(
            5 + p * 5
        )

        g = int(
            18 + p * 13
        )

        b = int(
            32 + p * 18
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
    # BACKGROUND GLOW
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
            -450,
            -300,
            550,
            750
        ),
        fill=(0, 220, 140, 55)
    )

    gd.ellipse(
        (
            WIDTH - 600,
            300,
            WIDTH + 500,
            1300
        ),
        fill=(45, 100, 255, 45)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(150)
    )

    image.paste(
        glow,
        (0, 0),
        glow
    )

    # --------------------------------------------------------
    # DECORATIVE LINES
    # --------------------------------------------------------

    for i in range(
        -500,
        WIDTH + 500,
        170
    ):

        draw.line(
            (
                i,
                0,
                i + 300,
                300
            ),
            fill=(15, 48, 67),
            width=2
        )

    # --------------------------------------------------------
    # HEADER PANEL
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            55,
            45,
            WIDTH - 55,
            HEADER - 35
        ),
        radius=55,
        fill=(7, 28, 45),
        outline=(37, 211, 130),
        width=4
    )

    # --------------------------------------------------------
    # TOP ACCENT
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            300,
            45,
            WIDTH - 300,
            62
        ),
        radius=8,
        fill=(37, 211, 130)
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    draw_rtl(
        draw,
        (
            WIDTH // 2,
            145
        ),
        "بازی‌های امروز",
        font(
            88,
            bold=True
        ),
        (255, 255, 255)
    )

    # --------------------------------------------------------
    # SUBTITLE
    # --------------------------------------------------------

    draw_rtl(
        draw,
        (
            WIDTH // 2,
            245
        ),
        "۹ لیگ معتبر فوتبال",
        font(
            43,
            bold=True
        ),
        (37, 211, 130)
    )

    # --------------------------------------------------------
    # TIMEZONE
    # --------------------------------------------------------

    draw_rtl(
        draw,
        (
            WIDTH // 2,
            315
        ),
        "تمامی زمان‌ها به وقت تهران",
        font(
            32,
            bold=True
        ),
        (215, 225, 232)
    )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    draw.text(
        (
            WIDTH // 2,
            385
        ),
        today.isoformat(),
        font=font(
            28
        ),
        fill=(137, 162, 175),
        anchor="mm"
    )

    # --------------------------------------------------------
    # MATCHES
    # --------------------------------------------------------

    y = HEADER

    for match in matches:

        draw_match_card(
            image,
            draw,
            match,
            SIDE,
            y,
            CARD_WIDTH,
            CARD_HEIGHT
        )

        y += (
            CARD_HEIGHT
            + CARD_GAP
        )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    footer_y = HEIGHT - 75

    draw.line(
        (
            250,
            footer_y,
            WIDTH - 250,
            footer_y
        ),
        fill=(37, 211, 130),
        width=3
    )

    draw.text(
        (
            WIDTH // 2,
            footer_y + 30
        ),
        "FOOTBALL ALERT",
        font=font(
            20,
            bold=True
        ),
        fill=(100, 127, 142),
        anchor="mm"
    )

    return image


# ============================================================
# TELEGRAM
# ============================================================

def send_photo(
    image,
    today,
    match_count
):

    try:

        buffer = BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=96,
            optimize=True,
            subsampling=0
        )

        buffer.seek(0)

        url = (
            f"https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendPhoto"
        )

        caption = (
            "⚽ بازی‌های امروز\n"
            f"📅 {today.isoformat()}\n"
            f"🏟 {fa_digits(match_count)} بازی\n"
            "🕐 زمان تهران"
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
            "Telegram ERROR:",
            e
        )

        return False


# ============================================================
# TEXT
# ============================================================

def send_text(message):

    try:

        url = (
            f"https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendMessage"
        )

        r = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=30
        )

        print(
            "Text:",
            r.status_code
        )

        return r.ok

    except Exception as e:

        print(
            "Text ERROR:",
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
        "FOOTBALL ALERT PREMIUM"
    )

    print(
        "======================================"
    )

    if not BOT_TOKEN:
        print("BOT_TOKEN missing")
        return

    if not CHAT_ID:
        print("CHAT_ID missing")
        return

    if not FOOTBALL_API_TOKEN:
        print(
            "FOOTBALL_API_TOKEN missing"
        )
        return

    today = datetime.now(
        TEHRAN
    ).date()

    print(
        "Tehran date:",
        today
    )

    all_matches = []

    # --------------------------------------------------------
    # FETCH ALL LEAGUES
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
    # SORT
    # --------------------------------------------------------

    all_matches.sort(
        key=lambda match:
        match.get(
            "utcDate",
            ""
        )
    )

    print(
        "TOTAL MATCHES:",
        len(all_matches)
    )

    # --------------------------------------------------------
    # NOTHING
    # --------------------------------------------------------

    if not all_matches:

        send_text(
            "⚽ بازی‌ای برای امروز پیدا نشد.\n"
            f"📅 {today.isoformat()}"
        )

        return

    # --------------------------------------------------------
    # CREATE ONE PREMIUM IMAGE
    # --------------------------------------------------------

    poster = create_poster(
        all_matches,
        today
    )

    # --------------------------------------------------------
    # SEND
    # --------------------------------------------------------

    success = send_photo(
        poster,
        today,
        len(all_matches)
    )

    if success:

        print(
            "======================================"
        )

        print(
            "PREMIUM POSTER SENT"
        )

        print(
            "======================================"
        )

    else:

        print(
            "POSTER SEND FAILED"
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
