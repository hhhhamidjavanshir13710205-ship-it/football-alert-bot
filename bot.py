# -*- coding: utf-8 -*-

import os
import io
import time
import math
import requests

from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ============================================================
# تنظیمات
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

TEHRAN = ZoneInfo("Asia/Tehran")

WIDTH = 1600
MARGIN = 70
GAP = 28


# ============================================================
# لیگ‌ها
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
    "PL": (128, 86, 245),
    "PD": (235, 75, 92),
    "SA": (48, 135, 235),
    "BL1": (235, 72, 72),
    "FL1": (50, 125, 235),
    "DED": (240, 145, 40),
    "PPL": (35, 170, 115),
    "BSA": (40, 160, 100),
    "CL": (92, 100, 235),
}


# ============================================================
# نام تیم‌ها
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
    "Club Atlأ©tico de Madrid": "اتلتیکو مادرید",
    "Sevilla FC": "سویا",
    "Valencia CF": "والنسیا",
    "Villarreal CF": "ویارئال",
    "Athletic Club": "اتلتیک بیلبائو",
    "Real Betis Balompié": "رئال بتیس",
    "Real Betis Balompiأ©": "رئال بتیس",
    "Getafe CF": "ختافه",
    "Girona FC": "ژیرونا",
    "RC Celta de Vigo": "سلتاویگو",
    "CA Osasuna": "اوساسونا",
    "Rayo Vallecano de Madrid": "رایو وایکانو",
    "RCD Mallorca": "مایورکا",
    "Deportivo Alavés": "آلاوس",
    "Deportivo Alavأ©s": "آلاوس",
    "Real Sociedad de Fútbol": "رئال سوسیداد",
    "Real Sociedad de Fأ؛tbol": "رئال سوسیداد",

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
    "US Sassuolo Calcio": "ساسولو",
    "Sassuolo Calcio": "ساسولو",

    # Germany
    "FC Bayern München": "بایرن مونیخ",
    "FC Bayern Mأ¼nchen": "بایرن مونیخ",
    "Borussia Dortmund": "دورتموند",
    "RB Leipzig": "لایپزیگ",
    "Bayer 04 Leverkusen": "بایرلورکوزن",
    "Eintracht Frankfurt": "آینتراخت فرانکفورت",
    "VfB Stuttgart": "اشتوتگارت",
    "VfL Wolfsburg": "ولفسبورگ",
    "Borussia Mönchengladbach": "مونشن گلادباخ",
    "Borussia Mأ¶nchengladbach": "مونشن گلادباخ",
    "SV Werder Bremen": "وردربرمن",
    "1. FSV Mainz 05": "ماینتس",
    "TSG 1899 Hoffenheim": "هوفنهایم",
    "Sport-Club Freiburg": "فرایبورگ",
    "FC Augsburg": "آگسبورگ",
    "1. FC Union Berlin": "یونیون برلین",
    "1. FC Köln": "کلن",
    "1. FC Kأ¶ln": "کلن",
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
    "Racing Club de Lens": "لانس",
    "RC Strasbourg Alsace": "استراسبورگ",

    # Netherlands
    "AFC Ajax": "آژاکس",
    "PSV": "آیندهوون",
    "Feyenoord Rotterdam": "فاینورد",
    "AZ": "آلکمار",
    "FC Twente '65": "توئنته",
    "FC Utrecht": "اوترخت",
    "PEC Zwolle": "زوله",
    "FC Groningen": "خرونینگن",

    # Portugal
    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "SC Braga": "براگا",
    "Vitória SC": "ویتوریا گیمارش",
    "Vitأ³ria SC": "ویتوریا گیمارش",

    # Brazil
    "CR Flamengo": "فلامینگو",
    "SE Palmeiras": "پالمیراس",
    "Botafogo FR": "بوتافوگو",
    "Fluminense FC": "فلومیننزه",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
    "Sأ£o Paulo FC": "سائوپائولو",
}


# ============================================================
# فونت
# ============================================================

def get_font(size, bold=False):

    custom = os.getenv("FONT_PATH")

    if custom and os.path.exists(custom):
        return ImageFont.truetype(custom, size)

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
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


# ============================================================
# بررسی RAQM
# ============================================================

def check_raqm():

    try:
        layout_engine = ImageFont.Layout.RAQM

        test_font = get_font(
            30,
            bold=False
        )

        print("Pillow RAQM available.")

        return layout_engine

    except Exception as e:

        print(
            f"WARNING: Pillow RAQM unavailable: {e}"
        )

        return None


RAQM_ENGINE = check_raqm()


# ============================================================
# اصلاح متن‌های Encoding خراب
# ============================================================

def repair_text(text):

    if text is None:
        return ""

    text = str(text)

    # اگر متن قبلاً درست باشد، همان را نگه می‌داریم.
    # متن‌های فارسی خراب‌شده در فایل فعلی با cp1256 قابل بازیابی هستند.
    try:

        repaired = text.encode(
            "cp1256"
        ).decode(
            "utf-8"
        )

        # فقط وقتی نتیجه واقعاً بهتر شده باشد.
        if repaired != text:
            return repaired

    except Exception:
        pass

    return text


# ============================================================
# متن فارسی با RAQM
# ============================================================

def draw_rtl(
    draw,
    xy,
    text,
    font,
    fill,
    anchor="ra",
    align="right"
):

    text = repair_text(text)

    kwargs = {
        "font": font,
        "fill": fill,
        "anchor": anchor,
        "align": align,
    }

    if RAQM_ENGINE is not None:
        kwargs["direction"] = "rtl"
        kwargs["language"] = "fa"

    draw.text(
        xy,
        text,
        **kwargs
    )


def text_bbox(
    draw,
    text,
    font,
    direction="rtl"
):

    text = repair_text(text)

    kwargs = {
        "font": font
    }

    if RAQM_ENGINE is not None:
        kwargs["direction"] = direction
        kwargs["language"] = "fa"

    return draw.textbbox(
        (0, 0),
        text,
        **kwargs
    )


# ============================================================
# اعداد فارسی
# ============================================================

def persian_digits(text):

    table = str.maketrans(
        "0123456789",
        "۰۱۲۳۴۵۶۷۸۹"
    )

    return str(text).translate(table)


# ============================================================
# متن وسط
# ============================================================

def draw_center(
    draw,
    cx,
    y,
    text,
    font,
    fill
):

    text = repair_text(text)

    box = text_bbox(
        draw,
        text,
        font,
        "rtl"
    )

    w = box[2] - box[0]

    kwargs = {
        "font": font,
        "fill": fill,
        "anchor": "ra",
        "align": "center",
    }

    if RAQM_ENGINE is not None:
        kwargs["direction"] = "rtl"
        kwargs["language"] = "fa"

    draw.text(
        (
            cx + w / 2,
            y
        ),
        text,
        **kwargs
    )


# ============================================================
# فونت مناسب با عرض
# ============================================================

def fit_font(
    draw,
    text,
    max_width,
    max_size,
    min_size=20
):

    text = repair_text(text)

    for size in range(
        max_size,
        min_size - 1,
        -2
    ):

        font = get_font(
            size,
            bold=True
        )

        box = text_bbox(
            draw,
            text,
            font,
            "rtl"
        )

        width = box[2] - box[0]

        if width <= max_width:
            return font

    return get_font(
        min_size,
        bold=True
    )


# ============================================================
# تاریخ
# ============================================================

def get_today():

    return datetime.now(
        TEHRAN
    ).strftime(
        "%Y-%m-%d"
    )


def format_date(date_string):

    try:

        dt = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        )

        return (
            str(dt.year)
            + "/"
            + str(dt.month).zfill(2)
            + "/"
            + str(dt.day).zfill(2)
        )

    except Exception:

        return date_string


# ============================================================
# ساعت تهران
# ============================================================

def match_time(utc_string):

    try:

        dt = datetime.fromisoformat(
            utc_string.replace(
                "Z",
                "+00:00"
            )
        )

        local = dt.astimezone(
            TEHRAN
        )

        return local.strftime(
            "%H:%M"
        )

    except Exception:

        return "--:--"


# ============================================================
# دریافت مسابقات
# ============================================================

def get_matches(
    code,
    date_string
):

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
                API_URL.format(code),
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

            return data.get(
                "matches",
                []
            )

        except Exception as e:

            print(
                f"Error {code}: {e}"
            )

            if attempt < 2:
                time.sleep(5)

    return []


# ============================================================
# دانلود لوگو
# ============================================================

LOGO_CACHE = {}


def download_logo(url):

    if not url:
        return None

    if url in LOGO_CACHE:
        return LOGO_CACHE[url]

    try:

        response = requests.get(
            url,
            timeout=15
        )

        response.raise_for_status()

        image = Image.open(
            io.BytesIO(
                response.content
            )
        ).convert(
            "RGBA"
        )

        image.thumbnail(
            (240, 240),
            Image.Resampling.LANCZOS
        )

        LOGO_CACHE[url] = image

        return image

    except Exception as e:

        print(
            f"Logo download failed: {e}"
        )

        LOGO_CACHE[url] = None

        return None


# ============================================================
# پس‌زمینه
# ============================================================

def create_background(
    width,
    height
):

    image = Image.new(
        "RGBA",
        (width, height)
    )

    pixels = image.load()

    for y in range(height):

        ratio = y / max(
            height - 1,
            1
        )

        r = int(
            7 + ratio * 5
        )

        g = int(
            10 + ratio * 5
        )

        b = int(
            24 + ratio * 12
        )

        for x in range(width):

            dx = (
                x - width * 0.5
            ) / width

            dy = (
                y - height * 0.18
            ) / height

            distance = math.sqrt(
                dx * dx + dy * dy
            )

            glow = max(
                0,
                1 - distance * 3
            )

            pixels[x, y] = (
                min(
                    255,
                    int(r + glow * 8)
                ),
                min(
                    255,
                    int(g + glow * 8)
                ),
                min(
                    255,
                    int(b + glow * 18)
                ),
                255
            )

    return image


def add_background_effects(image):

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(
        overlay
    )

    w, h = image.size

    draw.ellipse(
        (
            -300,
            -200,
            500,
            600
        ),
        fill=(87, 75, 230, 22)
    )

    draw.ellipse(
        (
            w - 500,
            100,
            w + 300,
            900
        ),
        fill=(45, 100, 230, 18)
    )

    for x in range(
        -h,
        w + h,
        220
    ):

        draw.line(
            (
                x,
                h,
                x + h,
                0
            ),
            fill=(255, 255, 255, 5),
            width=2
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(12)
    )

    image.alpha_composite(
        overlay
    )


# ============================================================
# سایه کارت
# ============================================================

def add_card_shadow(
    image,
    box,
    radius=28
):

    shadow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(
        shadow
    )

    x1, y1, x2, y2 = box

    draw.rounded_rectangle(
        (
            x1,
            y1 + 10,
            x2,
            y2 + 10
        ),
        radius=radius,
        fill=(0, 0, 0, 110)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(22)
    )

    image.alpha_composite(
        shadow
    )


# ============================================================
# لوگو
# ============================================================

def draw_logo(
    image,
    logo,
    cx,
    cy,
    size=155
):

    plate_size = size + 30

    plate = Image.new(
        "RGBA",
        (
            plate_size,
            plate_size
        ),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(
        plate
    )

    # سایه
    draw.ellipse(
        (
            5,
            9,
            plate_size - 1,
            plate_size + 5
        ),
        fill=(0, 0, 0, 70)
    )

    # صفحه سفید
    draw.ellipse(
        (
            0,
            0,
            plate_size - 7,
            plate_size - 7
        ),
        fill=(248, 249, 252, 255)
    )

    if logo:

        logo = logo.copy()

        logo.thumbnail(
            (
                size - 10,
                size - 10
            ),
            Image.Resampling.LANCZOS
        )

        lx = (
            plate.width
            - logo.width
        ) // 2

        ly = (
            plate.height
            - logo.height
        ) // 2

        plate.alpha_composite(
            logo,
            (
                lx,
                ly
            )
        )

    else:

        draw.ellipse(
            (
                25,
                25,
                plate_size - 32,
                plate_size - 32
            ),
            outline=(
                205,
                209,
                220,
                255
            ),
            width=4
        )

    image.alpha_composite(
        plate,
        (
            int(
                cx - plate.width / 2
            ),
            int(
                cy - plate.height / 2
            )
        )
    )


# ============================================================
# کارت مسابقه
# ============================================================

def draw_match_card(
    image,
    match,
    x,
    y,
    width,
    height,
    number
):

    draw = ImageDraw.Draw(
        image
    )

    accent = LEAGUE_COLORS.get(
        match["competition_code"],
        (100, 110, 235)
    )

    # سایه
    add_card_shadow(
        image,
        (
            x,
            y,
            x + width,
            y + height
        )
    )

    # خود کارت
    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + height
        ),
        radius=30,
        fill=(19, 23, 42, 255)
    )

    # نوار رنگی
    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + 7
        ),
        radius=4,
        fill=accent
    )

    # شماره
    circle = 52

    draw.ellipse(
        (
            x + 24,
            y + 22,
            x + 24 + circle,
            y + 22 + circle
        ),
        fill=(255, 255, 255, 16)
    )

    number_font = get_font(
        23,
        bold=True
    )

    number_text = persian_digits(
        number
    )

    box = draw.textbbox(
        (0, 0),
        number_text,
        font=number_font
    )

    nw = box[2] - box[0]
    nh = box[3] - box[1]

    draw.text(
        (
            x + 24 + (circle - nw) / 2,
            y + 22 + (circle - nh) / 2 - 3
        ),
        number_text,
        font=number_font,
        fill=(240, 242, 249)
    )

    # نام لیگ
    league_font = fit_font(
        draw,
        match["league_name"],
        width - 150,
        28,
        18
    )

    league_text = repair_text(
        match["league_name"]
    )

    league_box = text_bbox(
        draw,
        league_text,
        league_font,
        "rtl"
    )

    league_width = (
        league_box[2]
        - league_box[0]
    )

    draw_rtl(
        draw,
        (
            x + width - 30,
            y + 31
        ),
        league_text,
        league_font,
        (239, 241, 247),
        anchor="ra"
    )

    # خط جداکننده
    draw.line(
        (
            x + 30,
            y + 92,
            x + width - 30,
            y + 92
        ),
        fill=(255, 255, 255, 22),
        width=2
    )

    center = x + width / 2

    home_x = x + width * 0.27
    away_x = x + width * 0.73

    logo_y = y + 180

    # لوگوها
    draw_logo(
        image,
        match["home_logo"],
        home_x,
        logo_y,
        140
    )

    draw_logo(
        image,
        match["away_logo"],
        away_x,
        logo_y,
        140
    )

    # VS
    vs_font = get_font(
        24,
        bold=True
    )

    draw_center(
        draw,
        center,
        y + 166,
        "VS",
        vs_font,
        (132, 140, 164)
    )

    # ساعت
    time_width = 155
    time_height = 66

    time_x = int(
        center - time_width / 2
    )

    time_y = y + 222

    draw.rounded_rectangle(
        (
            time_x,
            time_y,
            time_x + time_width,
            time_y + time_height
        ),
        radius=19,
        fill=accent
    )

    time_font = get_font(
        35,
        bold=True
    )

    time_text = persian_digits(
        match["time"]
    )

    box = draw.textbbox(
        (0, 0),
        time_text,
        font=time_font
    )

    tw = box[2] - box[0]
    th = box[3] - box[1]

    draw.text(
        (
            center - tw / 2,
            time_y
            + (time_height - th) / 2
            - 6
        ),
        time_text,
        font=time_font,
        fill=(255, 255, 255)
    )

    # نام تیم‌ها
    home_font = fit_font(
        draw,
        match["home"],
        width * 0.36,
        32,
        19
    )

    away_font = fit_font(
        draw,
        match["away"],
        width * 0.36,
        32,
        19
    )

    draw_center(
        draw,
        home_x,
        y + 300,
        match["home"],
        home_font,
        (248, 249, 253)
    )

    draw_center(
        draw,
        away_x,
        y + 300,
        match["away"],
        away_font,
        (248, 249, 253)
    )

    # میزبان / مهمان
    small_font = get_font(
        17,
        bold=False
    )

    draw_center(
        draw,
        home_x,
        y + 347,
        "میزبان",
        small_font,
        (120, 128, 153)
    )

    draw_center(
        draw,
        away_x,
        y + 347,
        "مهمان",
        small_font,
        (120, 128, 153)
    )


# ============================================================
# ساخت پوستر
# ============================================================

def create_poster(matches):

    columns = 2

    card_width = int(
        (
            WIDTH
            - MARGIN * 2
            - GAP
        ) / 2
    )

    card_height = 395

    rows = math.ceil(
        len(matches) / columns
    )

    header_height = 385

    footer_height = 100

    height = (
        header_height
        + rows * card_height
        + max(
            0,
            rows - 1
        ) * GAP
        + footer_height
        + 60
    )

    image = create_background(
        WIDTH,
        height
    )

    add_background_effects(
        image
    )

    draw = ImageDraw.Draw(
        image
    )

    # نوار بالایی
    draw.rectangle(
        (
            0,
            0,
            WIDTH,
            8
        ),
        fill=(126, 90, 245)
    )

    # عنوان انگلیسی
    english_font = get_font(
        27,
        bold=True
    )

    draw.text(
        (
            MARGIN,
            52
        ),
        "FOOTBALL DAILY",
        font=english_font,
        fill=(145, 132, 255)
    )

    # عنوان فارسی
    title_font = get_font(
        76,
        bold=True
    )

    title = "بازی‌های امروز"

    title_box = text_bbox(
        draw,
        title,
        title_font,
        "rtl"
    )

    title_w = (
        title_box[2]
        - title_box[0]
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            95
        ),
        title,
        title_font,
        (250, 250, 253),
        anchor="ra"
    )

    # زیرعنوان
    subtitle_font = get_font(
        28,
        bold=False
    )

    subtitle = (
        "برنامه مسابقات فوتبال امروز"
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            190
        ),
        subtitle,
        subtitle_font,
        (148, 155, 180),
        anchor="ra"
    )

    # تاریخ
    date_font = get_font(
        27,
        bold=True
    )

    date_text = (
        "تاریخ "
        + format_date(
            get_today()
        )
    )

    date_box = text_bbox(
        draw,
        date_text,
        date_font,
        "rtl"
    )

    date_w = (
        date_box[2]
        - date_box[0]
    )

    date_box_w = max(
        290,
        date_w + 55
    )

    draw.rounded_rectangle(
        (
            MARGIN,
            145,
            MARGIN + date_box_w,
            210
        ),
        radius=17,
        fill=(255, 255, 255, 15),
        outline=(255, 255, 255, 22),
        width=1
    )

    draw_rtl(
        draw,
        (
            MARGIN + date_box_w - 25,
            161
        ),
        date_text,
        date_font,
        (235, 238, 246),
        anchor="ra"
    )

    # خط
    draw.line(
        (
            MARGIN,
            285,
            WIDTH - MARGIN,
            285
        ),
        fill=(255, 255, 255, 20),
        width=2
    )

    # تعداد بازی‌ها
    count_font = get_font(
        24,
        bold=True
    )

    count_text = (
        persian_digits(
            len(matches)
        )
        + " مسابقه امروز"
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            325
        ),
        count_text,
        count_font,
        (135, 143, 170),
        anchor="ra"
    )

    # کارت‌ها
    start_y = header_height

    for i, match in enumerate(
        matches
    ):

        row = i // columns
        col = i % columns

        x = (
            MARGIN
            + col * (
                card_width
                + GAP
            )
        )

        y = (
            start_y
            + row * (
                card_height
                + GAP
            )
        )

        draw_match_card(
            image,
            match,
            x,
            y,
            card_width,
            card_height,
            i + 1
        )

    # فوتر
    footer_y = (
        start_y
        + rows * card_height
        + max(
            0,
            rows - 1
        ) * GAP
        + 30
    )

    draw.line(
        (
            MARGIN,
            footer_y,
            WIDTH - MARGIN,
            footer_y
        ),
        fill=(255, 255, 255, 18),
        width=2
    )

    footer_font = get_font(
        22,
        bold=False
    )

    footer = (
        "تمامی ساعت‌ها به وقت تهران"
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            footer_y + 30
        ),
        footer,
        footer_font,
        (116, 124, 150),
        anchor="ra"
    )

    # نقطه تزئینی
    draw.ellipse(
        (
            MARGIN,
            footer_y + 31,
            MARGIN + 16,
            footer_y + 47
        ),
        fill=(126, 90, 245)
    )

    # خروجی JPEG
    output = io.BytesIO()

    image.convert(
        "RGB"
    ).save(
        output,
        format="JPEG",
        quality=97,
        optimize=True
    )

    output.seek(0)

    return output


# ============================================================
# ارسال تلگرام
# ============================================================

def send_photo(
    photo,
    caption
):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendPhoto"
    )

    files = {
        "photo": (
            "football_today.jpg",
            photo,
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

    print(
        "Telegram message sent."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("FOOTBALL DAILY BOT")
    print("=" * 60)

    # بررسی Secretها
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
        f"Today in Tehran: {today}"
    )

    all_matches = []

    # دریافت ۹ لیگ
    for code, league_name in COMPETITIONS.items():

        print(
            f"Checking {code}..."
        )

        matches = get_matches(
            code,
            today
        )

        print(
            f"{code}: {len(matches)} matches"
        )

        for match in matches:

            status = match.get(
                "status",
                ""
            )

            if status in [
                "CANCELLED",
                "POSTPONED"
            ]:
                continue

            utc = match.get(
                "utcDate"
            )

            if not utc:
                continue

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
                "تیم میزبان"
            )

            away_original = away_data.get(
                "name",
                "تیم مهمان"
            )

            home_original = repair_text(
                home_original
            )

            away_original = repair_text(
                away_original
            )

            home_name = TEAM_NAMES.get(
                home_original
            )

            if not home_name:
                home_name = home_original

            away_name = TEAM_NAMES.get(
                away_original
            )

            if not away_name:
                away_name = away_original

            home_logo_url = home_data.get(
                "crest"
            )

            away_logo_url = away_data.get(
                "crest"
            )

            all_matches.append(
                {
                    "competition_code": code,
                    "league_name": league_name,
                    "home": home_name,
                    "away": away_name,
                    "home_logo": download_logo(
                        home_logo_url
                    ),
                    "away_logo": download_logo(
                        away_logo_url
                    ),
                    "time": match_time(
                        utc
                    ),
                    "utc": utc
                }
            )

    # مرتب‌سازی بر اساس زمان
    all_matches.sort(
        key=lambda item: item["utc"]
    )

    print(
        f"TOTAL MATCHES: {len(all_matches)}"
    )

    # اگر بازی پیدا نشد
    if not all_matches:

        message = (
            "⚽ بازی‌های امروز\n\n"
            f"📅 تاریخ: {format_date(today)}\n\n"
            "در ۹ لیگ منتخب امروز "
            "مسابقه‌ای پیدا نشد."
        )

        url = (
            f"https://api.telegram.org/bot"
            f"{BOT_TOKEN}/sendMessage"
        )

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=30
        )

        response.raise_for_status()

        print(
            "No matches found."
        )

        return

    # ساخت پوستر
    print(
        "Creating poster..."
    )

    poster = create_poster(
        all_matches
    )

    # کپشن
    caption = (
        "⚽ بازی‌های امروز\n"
        f"📅 {format_date(today)}\n"
        f"🎯 {persian_digits(len(all_matches))} مسابقه\n"
        "🕐 تمامی ساعت‌ها به وقت تهران"
    )

    # ارسال
    send_photo(
        poster,
        caption
    )

    print(
        "DONE"
    )

    print("=" * 60)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
