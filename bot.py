# -*- coding: utf-8 -*-

import os
import io
import time
import math
import requests

from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import arabic_reshaper
from bidi.algorithm import get_display


# ============================================================
# CONFIG
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

TEHRAN = ZoneInfo("Asia/Tehran")

POSTER_WIDTH = 1600

# فاصله بین کارت‌ها
CARD_GAP = 28

# حاشیه پوستر
SIDE_MARGIN = 70

# تعداد ستون‌های کارت
COLUMNS = 2


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


# رنگ اختصاصی لیگ‌ها
LEAGUE_COLORS = {
    "PL": (126, 87, 255),
    "PD": (239, 92, 105),
    "SA": (54, 139, 245),
    "BL1": (235, 78, 78),
    "FL1": (76, 143, 245),
    "DED": (244, 157, 52),
    "PPL": (47, 181, 126),
    "BSA": (54, 164, 103),
    "CL": (93, 111, 235),
}


# ============================================================
# TEAM NAMES
# ============================================================

TEAM_NAMES = {

    # --------------------------------------------------------
    # ENGLAND
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # SPAIN
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # ITALY
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # GERMANY
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # FRANCE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # NETHERLANDS
    # --------------------------------------------------------

    "AFC Ajax": "آژاکس",
    "PSV": "آیندهوون",
    "Feyenoord Rotterdam": "فاینورد",
    "AZ": "آلکمار",
    "FC Twente '65": "توئنته",
    "FC Utrecht": "اوترخت",
    "PEC Zwolle": "زوله",
    "FC Groningen": "خرونینگن",

    # --------------------------------------------------------
    # PORTUGAL
    # --------------------------------------------------------

    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "SC Braga": "براگا",
    "Vitória SC": "ویتوریا گیمارش",

    # --------------------------------------------------------
    # BRAZIL
    # --------------------------------------------------------

    "CR Flamengo": "فلامینگو",
    "SE Palmeiras": "پالمیراس",
    "Botafogo FR": "بوتافوگو",
    "Fluminense FC": "فلومیننزه",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
}


# ============================================================
# FONTS
# ============================================================

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansArabic-Regular.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansArabic-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def find_font(bold=False):
    """
    پیدا کردن فونت فارسی مناسب
    """

    if bold:
        preferred = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        preferred = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    custom = os.getenv("FONT_PATH")

    if custom and os.path.exists(custom):
        return custom

    for path in preferred:
        if os.path.exists(path):
            return path

    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path

    return None


def get_font(size, bold=False):

    path = find_font(bold)

    if path:
        return ImageFont.truetype(path, size)

    return ImageFont.load_default()


# ============================================================
# PERSIAN TEXT
# ============================================================

def rtl_text(text):
    """
    شکل‌دهی صحیح حروف فارسی و راست‌به‌چپ
    """

    if not text:
        return ""

    try:
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)


def fa_digits(value):
    """
    تبدیل اعداد انگلیسی به فارسی
    """

    table = str.maketrans(
        "0123456789",
        "۰۱۲۳۴۵۶۷۸۹"
    )

    return str(value).translate(table)


def fit_text(draw, text, max_width, start_size, min_size=22, bold=True):

    size = start_size

    while size >= min_size:

        font = get_font(size, bold=bold)

        bbox = draw.textbbox(
            (0, 0),
            rtl_text(text),
            font=font
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:
            return font

        size -= 2

    return get_font(min_size, bold=bold)


def draw_center_rtl(draw, center_x, y, text, font, fill):

    rendered = rtl_text(text)

    bbox = draw.textbbox(
        (0, 0),
        rendered,
        font=font
    )

    width = bbox[2] - bbox[0]

    x = center_x - width / 2

    draw.text(
        (x, y),
        rendered,
        font=font,
        fill=fill
    )


# ============================================================
# DATE / TIME
# ============================================================

def get_today():

    return datetime.now(
        TEHRAN
    ).strftime("%Y-%m-%d")


def format_persian_date(date_string):

    try:

        dt = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        )

        return fa_digits(
            dt.strftime("%Y/%m/%d")
        )

    except Exception:

        return fa_digits(date_string)


def match_time(utc_string):

    try:

        dt = datetime.fromisoformat(
            utc_string.replace("Z", "+00:00")
        )

        tehran_time = dt.astimezone(
            TEHRAN
        )

        return tehran_time.strftime("%H:%M")

    except Exception:

        return "--:--"


# ============================================================
# API
# ============================================================

def get_matches(competition, date_string):

    headers = {
        "X-Auth-Token": FOOTBALL_API_TOKEN
    }

    params = {
        "dateFrom": date_string,
        "dateTo": date_string
    }

    for attempt in range(3):

        try:

            response = requests.get(
                API_URL.format(competition),
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 429:

                print(
                    "Rate limit reached. Waiting 45 seconds..."
                )

                time.sleep(45)

                continue

            response.raise_for_status()

            data = response.json()

            return data.get("matches", [])

        except Exception as e:

            print(
                f"Error getting {competition}: {e}"
            )

            if attempt < 2:
                time.sleep(5)

    return []


# ============================================================
# LOGO DOWNLOAD
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
            timeout=15
        )

        response.raise_for_status()

        image = Image.open(
            io.BytesIO(response.content)
        ).convert("RGBA")

        # حداکثر اندازه لوگو
        image.thumbnail(
            (260, 260),
            Image.Resampling.LANCZOS
        )

        logo_cache[url] = image

        return image

    except Exception as e:

        print(
            f"Logo error: {e}"
        )

        logo_cache[url] = None

        return None


# ============================================================
# GRAPHIC HELPERS
# ============================================================

def rounded_rectangle(draw, box, radius, fill, outline=None, width=1):

    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width
    )


def add_shadow(base, box, radius=25, blur=25):

    shadow = Image.new(
        "RGBA",
        base.size,
        (0, 0, 0, 0)
    )

    sd = ImageDraw.Draw(shadow)

    x1, y1, x2, y2 = box

    sd.rounded_rectangle(
        box,
        radius=radius,
        fill=(0, 0, 0, 150)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(blur)
    )

    base.alpha_composite(
        shadow,
        (0, 0)
    )


def make_gradient(width, height):

    image = Image.new(
        "RGB",
        (width, height)
    )

    pixels = image.load()

    for y in range(height):

        ratio = y / max(height - 1, 1)

        # پس‌زمینه سرمه‌ای/مشکی
        r = int(9 + ratio * 5)
        g = int(12 + ratio * 6)
        b = int(25 + ratio * 13)

        for x in range(width):

            # نور بسیار ملایم در مرکز
            cx = width * 0.50
            cy = height * 0.30

            distance = math.sqrt(
                ((x - cx) / width) ** 2
                + ((y - cy) / height) ** 2
            )

            glow = max(
                0,
                1 - distance * 3
            )

            pixels[x, y] = (
                min(255, int(r + glow * 8)),
                min(255, int(g + glow * 10)),
                min(255, int(b + glow * 20)),
            )

    return image.convert("RGBA")


def draw_background_decor(base):

    overlay = Image.new(
        "RGBA",
        base.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(
        overlay
    )

    w, h = base.size

    # دایره‌های نور
    for cx, cy, radius, alpha in [
        (150, 220, 330, 35),
        (w - 100, 420, 400, 25),
        (w // 2, h - 150, 500, 18),
    ]:

        draw.ellipse(
            (
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius
            ),
            fill=(95, 105, 255, alpha)
        )

    # خطوط مورب مدرن
    for i in range(-h, w, 180):

        draw.line(
            (
                i,
                h,
                i + h,
                0
            ),
            fill=(255, 255, 255, 8),
            width=2
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(8)
    )

    base.alpha_composite(
        overlay
    )


# ============================================================
# LOGO DRAW
# ============================================================

def draw_logo(
    canvas,
    logo,
    center_x,
    center_y,
    size=180
):

    # صفحه سفید پشت لوگو
    plate = Image.new(
        "RGBA",
        (size + 36, size + 36),
        (0, 0, 0, 0)
    )

    pd = ImageDraw.Draw(plate)

    # سایه
    pd.ellipse(
        (
            8,
            12,
            size + 28,
            size + 28
        ),
        fill=(0, 0, 0, 80)
    )

    # دایره سفید
    pd.ellipse(
        (
            0,
            0,
            size + 28,
            size + 28
        ),
        fill=(248, 249, 252, 255)
    )

    if logo:

        logo_copy = logo.copy()

        logo_copy.thumbnail(
            (size - 15, size - 15),
            Image.Resampling.LANCZOS
        )

        lx = (
            plate.width
            - logo_copy.width
        ) // 2

        ly = (
            plate.height
            - logo_copy.height
        ) // 2

        plate.alpha_composite(
            logo_copy,
            (lx, ly)
        )

    else:

        # اگر لوگو پیدا نشد
        pd.ellipse(
            (
                22,
                22,
                size + 6,
                size + 6
            ),
            outline=(200, 204, 215, 255),
            width=4
        )

    x = int(
        center_x - plate.width / 2
    )

    y = int(
        center_y - plate.height / 2
    )

    canvas.alpha_composite(
        plate,
        (x, y)
    )


# ============================================================
# MATCH CARD
# ============================================================

def draw_match_card(
    canvas,
    match,
    x,
    y,
    width,
    height,
    number
):

    draw = ImageDraw.Draw(
        canvas
    )

    competition = match["competition_code"]

    league_name = match["league_name"]

    home = match["home"]
    away = match["away"]

    home_logo = match["home_logo"]
    away_logo = match["away_logo"]

    time_text = match["time"]

    accent = LEAGUE_COLORS.get(
        competition,
        (100, 120, 230)
    )

    # --------------------------------------------------------
    # shadow
    # --------------------------------------------------------

    add_shadow(
        canvas,
        (
            x,
            y + 8,
            x + width,
            y + height + 8
        ),
        radius=34,
        blur=22
    )

    # --------------------------------------------------------
    # card background
    # --------------------------------------------------------

    rounded_rectangle(
        draw,
        (
            x,
            y,
            x + width,
            y + height
        ),
        34,
        fill=(20, 24, 42, 245)
    )

    # --------------------------------------------------------
    # accent top line
    # --------------------------------------------------------

    rounded_rectangle(
        draw,
        (
            x,
            y,
            x + width,
            y + 8
        ),
        4,
        fill=accent
    )

    # --------------------------------------------------------
    # match number
    # --------------------------------------------------------

    circle_size = 54

    draw.ellipse(
        (
            x + 26,
            y + 24,
            x + 26 + circle_size,
            y + 24 + circle_size
        ),
        fill=(255, 255, 255, 18)
    )

    number_font = get_font(
        25,
        bold=True
    )

    num = fa_digits(number)

    bbox = draw.textbbox(
        (0, 0),
        num,
        font=number_font
    )

    nw = bbox[2] - bbox[0]
    nh = bbox[3] - bbox[1]

    draw.text(
        (
            x + 26 + (circle_size - nw) / 2,
            y + 24 + (circle_size - nh) / 2 - 3
        ),
        num,
        font=number_font,
        fill=(235, 238, 248)
    )

    # --------------------------------------------------------
    # league name
    # --------------------------------------------------------

    league_font = fit_text(
        draw,
        league_name,
        width - 170,
        30,
        20,
        bold=True
    )

    draw.text(
        (
            x + width - 40,
            y + 27
        ),
        rtl_text(league_name),
        font=league_font,
        anchor="ra",
        fill=(235, 238, 248)
    )

    # --------------------------------------------------------
    # separator
    # --------------------------------------------------------

    draw.line(
        (
            x + 28,
            y + 92,
            x + width - 28,
            y + 92
        ),
        fill=(255, 255, 255, 16),
        width=2
    )

    # --------------------------------------------------------
    # team area
    # --------------------------------------------------------

    center_x = x + width / 2

    logo_y = y + 175

    left_logo_x = x + width * 0.27
    right_logo_x = x + width * 0.73

    draw_logo(
        canvas,
        home_logo,
        left_logo_x,
        logo_y,
        size=145
    )

    draw_logo(
        canvas,
        away_logo,
        right_logo_x,
        logo_y,
        size=145
    )

    # --------------------------------------------------------
    # team names
    # --------------------------------------------------------

    team_font_home = fit_text(
        draw,
        home,
        width * 0.38,
        34,
        21,
        bold=True
    )

    team_font_away = fit_text(
        draw,
        away,
        width * 0.38,
        34,
        21,
        bold=True
    )

    # تیم میزبان
    draw_center_rtl(
        draw,
        left_logo_x,
        y + 292,
        home,
        team_font_home,
        (247, 248, 252)
    )

    # تیم مهمان
    draw_center_rtl(
        draw,
        right_logo_x,
        y + 292,
        away,
        team_font_away,
        (247, 248, 252)
    )

    # --------------------------------------------------------
    # VS
    # --------------------------------------------------------

    vs_font = get_font(
        25,
        bold=True
    )

    draw_center_rtl(
        draw,
        center_x,
        y + 160,
        "VS",
        vs_font,
        (137, 145, 172)
    )

    # --------------------------------------------------------
    # time badge
    # --------------------------------------------------------

    badge_w = 160
    badge_h = 70

    bx = int(
        center_x - badge_w / 2
    )

    by = y + 225

    rounded_rectangle(
        draw,
        (
            bx,
            by,
            bx + badge_w,
            by + badge_h
        ),
        22,
        fill=accent
    )

    # ساعت
    time_font = get_font(
        39,
        bold=True
    )

    time_render = fa_digits(time_text)

    bbox = draw.textbbox(
        (0, 0),
        time_render,
        font=time_font
    )

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    draw.text(
        (
            center_x - tw / 2,
            by + (badge_h - th) / 2 - 7
        ),
        time_render,
        font=time_font,
        fill=(255, 255, 255)
    )

    # --------------------------------------------------------
    # Tehran time label
    # --------------------------------------------------------

    label_font = get_font(
        21,
        bold=False
    )

    draw_center_rtl(
        draw,
        center_x,
        y + height - 45,
        "به وقت تهران",
        label_font,
        (145, 151, 175)
    )


# ============================================================
# CREATE POSTER
# ============================================================

def create_poster(matches):

    # ارتفاع کارت
    card_height = 390

    card_width = int(
        (
            POSTER_WIDTH
            - SIDE_MARGIN * 2
            - CARD_GAP
        ) / 2
    )

    rows = math.ceil(
        len(matches) / COLUMNS
    )

    header_height = 410

    footer_height = 110

    total_height = (
        header_height
        + rows * card_height
        + max(0, rows - 1) * CARD_GAP
        + footer_height
        + 90
    )

    canvas = make_gradient(
        POSTER_WIDTH,
        total_height
    )

    draw_background_decor(
        canvas
    )

    draw = ImageDraw.Draw(
        canvas
    )

    # ========================================================
    # HEADER
    # ========================================================

    # خط بالای پوستر
    draw.rectangle(
        (
            0,
            0,
            POSTER_WIDTH,
            8
        ),
        fill=(115, 98, 255, 255)
    )

    # برچسب کوچک
    small_font = get_font(
        26,
        bold=True
    )

    draw.text(
        (
            SIDE_MARGIN,
            60
        ),
        "FOOTBALL DAILY",
        font=small_font,
        fill=(145, 151, 255)
    )

    # عنوان اصلی
    title_font = get_font(
        82,
        bold=True
    )

    title = rtl_text(
        "بازی‌های امروز"
    )

    bbox = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_w = bbox[2] - bbox[0]

    draw.text(
        (
            POSTER_WIDTH - SIDE_MARGIN,
            105
        ),
        title,
        font=title_font,
        anchor="ra",
        fill=(250, 250, 253)
    )

    # زیرعنوان
    subtitle_font = get_font(
        32,
        bold=False
    )

    subtitle = rtl_text(
        "برنامه مسابقات فوتبال امروز"
    )

    draw.text(
        (
            POSTER_WIDTH - SIDE_MARGIN,
            205
        ),
        subtitle,
        font=subtitle_font,
        anchor="ra",
        fill=(164, 171, 196)
    )

    # تاریخ
    today = get_today()

    date_text = (
        "تاریخ  "
        + format_persian_date(today)
    )

    date_font = get_font(
        29,
        bold=True
    )

    rounded_rectangle(
        draw,
        (
            SIDE_MARGIN,
            150,
            SIDE_MARGIN + 280,
            215
        ),
        18,
        fill=(255, 255, 255, 13),
        outline=(255, 255, 255, 20),
        width=1
    )

    draw.text(
        (
            SIDE_MARGIN + 140,
            169
        ),
        rtl_text(date_text),
        font=date_font,
        anchor="mm",
        fill=(235, 238, 248)
    )

    # خط تزئینی
    draw.line(
        (
            SIDE_MARGIN,
            300,
            POSTER_WIDTH - SIDE_MARGIN,
            300
        ),
        fill=(255, 255, 255, 20),
        width=2
    )

    # تعداد مسابقات
    count_font = get_font(
        25,
        bold=True
    )

    count_text = (
        fa_digits(len(matches))
        + " مسابقه"
    )

    draw.text(
        (
            POSTER_WIDTH - SIDE_MARGIN,
            330
        ),
        rtl_text(count_text),
        font=count_font,
        anchor="ra",
        fill=(139, 148, 177)
    )

    # ========================================================
    # MATCHES
    # ========================================================

    start_y = header_height

    for index, match in enumerate(matches):

        row = index // COLUMNS
        col = index % COLUMNS

        x = (
            SIDE_MARGIN
            + col * (card_width + CARD_GAP)
        )

        y = (
            start_y
            + row * (card_height + CARD_GAP)
        )

        draw_match_card(
            canvas,
            match,
            x,
            y,
            card_width,
            card_height,
            index + 1
        )

    # ========================================================
    # FOOTER
    # ========================================================

    footer_y = (
        start_y
        + rows * card_height
        + max(0, rows - 1) * CARD_GAP
        + 40
    )

    draw.line(
        (
            SIDE_MARGIN,
            footer_y,
            POSTER_WIDTH - SIDE_MARGIN,
            footer_y
        ),
        fill=(255, 255, 255, 18),
        width=2
    )

    footer_font = get_font(
        24,
        bold=False
    )

    draw.text(
        (
            POSTER_WIDTH - SIDE_MARGIN,
            footer_y + 34
        ),
        rtl_text(
            "تمامی ساعت‌ها به وقت تهران"
        ),
        font=footer_font,
        anchor="ra",
        fill=(130, 138, 164)
    )

    # لوگوی کوچک تزئینی / نقطه
    draw.ellipse(
        (
            SIDE_MARGIN,
            footer_y + 29,
            SIDE_MARGIN + 18,
            footer_y + 47
        ),
        fill=(115, 98, 255)
    )

    # ========================================================
    # SAVE
    # ========================================================

    output = io.BytesIO()

    canvas.convert("RGB").save(
        output,
        format="JPEG",
        quality=96,
        optimize=True
    )

    output.seek(0)

    return output


# ============================================================
# SEND TELEGRAM
# ============================================================

def send_photo(photo_bytes, caption):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendPhoto"
    )

    files = {
        "photo": (
            "football_today.jpg",
            photo_bytes,
            "image/jpeg"
        )
    }

    data = {
        "chat_id": CHAT_ID,
        "caption": caption
    }

    response = requests.post(
        url,
        files=files,
        data=data,
        timeout=60
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("FOOTBALL DAILY BOT")
    print("=" * 60)

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN is missing"
        )

    if not CHAT_ID:
        raise ValueError(
            "CHAT_ID is missing"
        )

    if not FOOTBALL_API_TOKEN:
        raise ValueError(
            "FOOTBALL_API_TOKEN is missing"
        )

    today = get_today()

    print(
        f"Tehran date: {today}"
    )

    all_matches = []

    # --------------------------------------------------------
    # دریافت مسابقات
    # --------------------------------------------------------

    for code, league_name in COMPETITIONS.items():

        print(
            f"Checking {code} - {league_name}"
        )

        matches = get_matches(
            code,
            today
        )

        print(
            f"Found {len(matches)} matches"
        )

        for match in matches:

            status = match.get(
                "status",
                ""
            )

            # فقط مسابقات معتبر
            if status in [
                "CANCELLED",
                "POSTPONED"
            ]:
                continue

            utc_time = match.get(
                "utcDate"
            )

            if not utc_time:
                continue

            home_team = (
                match.get("homeTeam", {})
                .get("name", "تیم میزبان")
            )

            away_team = (
                match.get("awayTeam", {})
                .get("name", "تیم مهمان")
            )

            home_logo_url = (
                match.get("homeTeam", {})
                .get("crest")
            )

            away_logo_url = (
                match.get("awayTeam", {})
                .get("crest")
            )

            all_matches.append({

                "competition_code": code,

                "league_name": league_name,

                "home": TEAM_NAMES.get(
                    home_team,
                    home_team
                ),

                "away": TEAM_NAMES.get(
                    away_team,
                    away_team
                ),

                "home_logo": download_logo(
                    home_logo_url
                ),

                "away_logo": download_logo(
                    away_logo_url
                ),

                "time": match_time(
                    utc_time
                ),

                "utc": utc_time,
            })

    # --------------------------------------------------------
    # مرتب‌سازی بر اساس ساعت
    # --------------------------------------------------------

    all_matches.sort(
        key=lambda x: x["utc"]
    )

    print(
        f"Total matches: {len(all_matches)}"
    )

    # --------------------------------------------------------
    # اگر بازی نبود
    # --------------------------------------------------------

    if not all_matches:

        message = (
            "⚽ بازی‌های امروز\n\n"
            f"📅 تاریخ: {format_persian_date(today)}\n\n"
            "امروز در ۹ لیگ منتخب "
            "مسابقه‌ای پیدا نشد."
        )

        url = (
            f"https://api.telegram.org/bot"
            f"{BOT_TOKEN}/sendMessage"
        )

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=30
        )

        print(
            "No matches found."
        )

        return

    # --------------------------------------------------------
    # ساخت پوستر
    # --------------------------------------------------------

    print(
        "Creating professional poster..."
    )

    poster = create_poster(
        all_matches
    )

    # --------------------------------------------------------
    # کپشن تلگرام
    # --------------------------------------------------------

    caption = (
        "⚽ بازی‌های امروز\n"
        f"📅 {format_persian_date(today)}\n"
        f"🏟️ {fa_digits(len(all_matches))} مسابقه\n"
        "🕐 تمام ساعت‌ها به وقت تهران"
    )

    # --------------------------------------------------------
    # ارسال
    # --------------------------------------------------------

    print(
        "Sending poster to Telegram..."
    )

    send_photo(
        poster,
        caption
    )

    print(
        "Message sent successfully."
    )

    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
