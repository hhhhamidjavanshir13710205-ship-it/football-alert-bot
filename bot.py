# -*- coding: utf-8 -*-
"""
Football Alert Bot
نسخه طراحی جدید — پوستر مدرن و مینیمال با پشتیبانی واقعی RTL/RAQM
"""

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
MARGIN = 64
GAP = 26
CARD_HEIGHT = 340
HEADER_HEIGHT = 330
FOOTER_HEIGHT = 92

COMPETITIONS = {'PL': 'لیگ برتر انگلیس', 'PD': 'لالیگا', 'SA': 'سری آ ایتالیا', 'BL1': 'بوندسلیگا', 'FL1': 'لیگ ۱ فرانسه', 'DED': 'اردیویسه', 'PPL': 'لیگ پرتغال', 'BSA': 'سری آ برزیل', 'CL': 'لیگ قهرمانان اروپا'}
LEAGUE_COLORS = {'PL': (128, 86, 245), 'PD': (235, 75, 92), 'SA': (48, 135, 235), 'BL1': (235, 72, 72), 'FL1': (50, 125, 235), 'DED': (240, 145, 40), 'PPL': (35, 170, 115), 'BSA': (40, 160, 100), 'CL': (92, 100, 235)}
TEAM_NAMES = {'Brentford FC': 'برنتفورد', 'Chelsea FC': 'چلسی', 'Arsenal FC': 'آرسنال', 'Liverpool FC': 'لیورپول', 'Manchester City FC': 'منچسترسیتی', 'Manchester United FC': 'منچستریونایتد', 'Tottenham Hotspur FC': 'تاتنهام', 'Newcastle United FC': 'نیوکاسل', 'Aston Villa FC': 'استون ویلا', 'Everton FC': 'اورتون', 'West Ham United FC': 'وستهم', 'Fulham FC': 'فولام', 'Crystal Palace FC': 'کریستال پالاس', 'Brighton & Hove Albion FC': 'برایتون', 'Wolverhampton Wanderers FC': 'ولورهمپتون', 'Nottingham Forest FC': 'ناتینگهام فارست', 'AFC Bournemouth': 'بورنموث', 'Burnley FC': 'برنلی', 'Leeds United FC': 'لیدز', 'Sunderland AFC': 'ساندرلند', 'Real Madrid CF': 'رئال مادرید', 'FC Barcelona': 'بارسلونا', 'RCD Espanyol de Barcelona': 'اسپانیول', 'Elche CF': 'الچه', 'Club Atlético de Madrid': 'اتلتیکو مادرید', 'Club Atlأ©tico de Madrid': 'اتلتیکو مادرید', 'Sevilla FC': 'سویا', 'Valencia CF': 'والنسیا', 'Villarreal CF': 'ویارئال', 'Athletic Club': 'اتلتیک بیلبائو', 'Real Betis Balompié': 'رئال بتیس', 'Real Betis Balompiأ©': 'رئال بتیس', 'Getafe CF': 'ختافه', 'Girona FC': 'ژیرونا', 'RC Celta de Vigo': 'سلتاویگو', 'CA Osasuna': 'اوساسونا', 'Rayo Vallecano de Madrid': 'رایو وایکانو', 'RCD Mallorca': 'مایورکا', 'Deportivo Alavés': 'آلاوس', 'Deportivo Alavأ©s': 'آلاوس', 'Real Sociedad de Fútbol': 'رئال سوسیداد', 'Real Sociedad de Fأ؛tbol': 'رئال سوسیداد', 'FC Internazionale Milano': 'اینتر', 'Inter Milan': 'اینتر', 'AC Milan': 'آث میلان', 'Juventus FC': 'یوونتوس', 'SSC Napoli': 'ناپولی', 'AS Roma': 'رم', 'SS Lazio': 'لاتزیو', 'Atalanta BC': 'آتالانتا', 'ACF Fiorentina': 'فیورنتینا', 'Torino FC': 'تورینو', 'Bologna FC 1909': 'بولونیا', 'Genoa CFC': 'جنوا', 'Udinese Calcio': 'اودینزه', 'Parma Calcio 1913': 'پارما', 'US Lecce': 'لچه', 'Cagliari Calcio': 'کالیاری', 'Como 1907': 'کومو', 'US Sassuolo Calcio': 'ساسولو', 'Sassuolo Calcio': 'ساسولو', 'AC Monza': 'مونزا', 'FC Bayern München': 'بایرن مونیخ', 'FC Bayern Mأ¼nchen': 'بایرن مونیخ', 'Borussia Dortmund': 'دورتموند', 'RB Leipzig': 'لایپزیگ', 'Bayer 04 Leverkusen': 'بایرلورکوزن', 'Eintracht Frankfurt': 'آینتراخت فرانکفورت', 'VfB Stuttgart': 'اشتوتگارت', 'VfL Wolfsburg': 'ولفسبورگ', 'Borussia Mönchengladbach': 'مونشن گلادباخ', 'Borussia Mأ¶nchengladbach': 'مونشن گلادباخ', 'SV Werder Bremen': 'وردربرمن', '1. FSV Mainz 05': 'ماینتس', 'TSG 1899 Hoffenheim': 'هوفنهایم', 'Sport-Club Freiburg': 'فرایبورگ', 'FC Augsburg': 'آگسبورگ', '1. FC Union Berlin': 'یونیون برلین', '1. FC Köln': 'کلن', '1. FC Kأ¶ln': 'کلن', 'Hamburger SV': 'هامبورگ', 'Paris Saint-Germain FC': 'پاری سن ژرمن', 'Olympique de Marseille': 'مارسی', 'AS Monaco FC': 'موناکو', 'Olympique Lyonnais': 'لیون', 'Lille OSC': 'لیل', 'OGC Nice': 'نیس', 'Stade Rennais FC 1901': 'رن', 'FC Nantes': 'نانت', 'Toulouse FC': 'تولوز', 'RC Lens': 'لانس', 'Racing Club de Lens': 'لانس', 'RC Strasbourg Alsace': 'استراسبورگ', 'AFC Ajax': 'آژاکس', 'PSV': 'آیندهوون', 'Feyenoord Rotterdam': 'فاینورد', 'AZ': 'آلکمار', "FC Twente '65": 'توئنته', 'FC Utrecht': 'اوترخت', 'PEC Zwolle': 'زوله', 'FC Groningen': 'خرونینگن', 'SL Benfica': 'بنفیکا', 'FC Porto': 'پورتو', 'Sporting Clube de Portugal': 'اسپورتینگ', 'SC Braga': 'براگا', 'Vitória SC': 'ویتوریا گیمارش', 'Vitأ³ria SC': 'ویتوریا گیمارش', 'CR Flamengo': 'فلامینگو', 'SE Palmeiras': 'پالمیراس', 'Botafogo FR': 'بوتافوگو', 'Fluminense FC': 'فلومیننزه', 'Corinthians': 'کورینتیانس', 'São Paulo FC': 'سائوپائولو', 'Sأ£o Paulo FC': 'سائوپائولو'}


# ============================================================
# فونت و RTL
# ============================================================

def find_font(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def get_font(size, bold=False, latin=False):
    custom = os.getenv("FONT_PATH")

    if custom and os.path.exists(custom) and not latin:
        path = custom
    elif latin:
        path = find_font([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ])
    elif bold:
        path = find_font([
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/vazirmatn/Vazirmatn-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ])
    else:
        path = find_font([
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/vazirmatn/Vazirmatn-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ])

    if path:
        try:
            return ImageFont.truetype(
                path,
                size,
                layout_engine=ImageFont.Layout.RAQM
            )
        except Exception:
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def repair_text(text):
    if text is None:
        return ""

    text = str(text)

    try:
        repaired = text.encode("cp1256").decode("utf-8")
        if repaired != text:
            return repaired
    except Exception:
        pass

    return text


def persian_digits(text):
    return str(text).translate(
        str.maketrans(
            "0123456789",
            "۰۱۲۳۴۵۶۷۸۹"
        )
    )


def rtl_kwargs(font, fill, anchor="mm", align="center"):
    return {
        "font": font,
        "fill": fill,
        "anchor": anchor,
        "align": align,
        "direction": "rtl",
        "language": "fa",
    }


def draw_rtl(draw, xy, text, font, fill, anchor="ra", align="right"):
    try:
        draw.text(
            xy,
            repair_text(text),
            **rtl_kwargs(font, fill, anchor, align)
        )
    except Exception:
        draw.text(
            xy,
            repair_text(text),
            font=font,
            fill=fill,
            anchor=anchor,
            align=align,
        )


def draw_center(draw, cx, cy, text, font, fill):
    draw_rtl(
        draw,
        (cx, cy),
        text,
        font,
        fill,
        anchor="mm",
        align="center",
    )


def text_width(draw, text, font):
    text = repair_text(text)

    try:
        box = draw.textbbox(
            (0, 0),
            text,
            font=font,
            direction="rtl",
            language="fa",
        )
    except Exception:
        box = draw.textbbox(
            (0, 0),
            text,
            font=font,
        )

    return box[2] - box[0]


def fit_font(draw, text, max_width, max_size, min_size=18):
    for size in range(max_size, min_size - 1, -2):
        font = get_font(size, bold=True)

        if text_width(draw, text, font) <= max_width:
            return font

    return get_font(min_size, bold=True)


# ============================================================
# تاریخ و ساعت
# ============================================================

def get_today():
    return datetime.now(TEHRAN).strftime("%Y-%m-%d")


def format_date(date_string):
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d")
        return f"{dt.year}/{dt.month:02d}/{dt.day:02d}"
    except Exception:
        return date_string


def match_time(utc_string):
    try:
        dt = datetime.fromisoformat(
            utc_string.replace("Z", "+00:00")
        )
        return dt.astimezone(TEHRAN).strftime("%H:%M")
    except Exception:
        return "--:--"


# ============================================================
# نام تیم
# ============================================================

def team_display_name(original):
    original = repair_text(original).strip()

    if original in TEAM_NAMES:
        return TEAM_NAMES[original]

    normalized = original.replace("  ", " ")

    if normalized in TEAM_NAMES:
        return TEAM_NAMES[normalized]

    # نام ناشناخته را دست‌نخورده نگه می‌داریم.
    # اگر انگلیسی باشد با فونت مناسب در کارت نمایش داده می‌شود.
    return normalized


# ============================================================
# دریافت مسابقات
# ============================================================

def get_matches(code, date_string):
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

            return response.json().get(
                "matches",
                []
            )

        except Exception as exc:
            print(
                f"Error {code}: {exc}"
            )

            if attempt < 2:
                time.sleep(5)

    return []


# ============================================================
# لوگو
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
            io.BytesIO(response.content)
        ).convert("RGBA")

        image.thumbnail(
            (190, 190),
            Image.Resampling.LANCZOS
        )

        LOGO_CACHE[url] = image

        return image

    except Exception as exc:
        print(
            f"Logo download failed: {exc}"
        )

        LOGO_CACHE[url] = None
        return None


# ============================================================
# پس‌زمینه جدید
# ============================================================

def create_background(width, height):
    image = Image.new(
        "RGB",
        (width, height),
        (8, 12, 29)
    )

    pixels = image.load()

    for y in range(height):
        ratio = y / max(height - 1, 1)

        r = int(8 + 5 * ratio)
        g = int(12 + 8 * ratio)
        b = int(29 + 17 * ratio)

        for x in range(width):
            dx = (x - width * 0.78) / width
            dy = (y - height * 0.10) / height

            distance = math.sqrt(
                dx * dx + dy * dy
            )

            glow = max(
                0.0,
                1.0 - distance * 3.0
            )

            pixels[x, y] = (
                min(255, int(r + glow * 7)),
                min(255, int(g + glow * 7)),
                min(255, int(b + glow * 18)),
            )

    return image.convert("RGBA")


def add_background_effects(image):
    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)
    width, height = image.size

    draw.ellipse(
        (-320, -280, 480, 520),
        fill=(118, 80, 255, 24)
    )

    draw.ellipse(
        (
            width - 520,
            -180,
            width + 280,
            620
        ),
        fill=(35, 130, 255, 20)
    )

    draw.ellipse(
        (
            width * 0.25,
            height * 0.62,
            width * 0.72,
            height * 1.12
        ),
        fill=(60, 70, 190, 10)
    )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(70)
    )

    image.alpha_composite(overlay)


# ============================================================
# ابزارهای گرافیکی
# ============================================================

def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width
    )


def add_shadow(
    image,
    box,
    radius=22,
    blur=18,
    offset_y=8
):
    shadow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(shadow)

    x1, y1, x2, y2 = box

    draw.rounded_rectangle(
        (
            x1,
            y1 + offset_y,
            x2,
            y2 + offset_y
        ),
        radius=radius,
        fill=(0, 0, 0, 105)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(blur)
    )

    image.alpha_composite(shadow)


def draw_logo(
    image,
    logo,
    cx,
    cy,
    size=116
):
    plate = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(plate)

    draw.ellipse(
        (2, 4, size - 2, size - 2),
        fill=(0, 0, 0, 70)
    )

    draw.ellipse(
        (0, 0, size - 5, size - 7),
        fill=(248, 249, 252, 255)
    )

    if logo:
        logo = logo.copy()

        logo.thumbnail(
            (size - 30, size - 30),
            Image.Resampling.LANCZOS
        )

        lx = (size - logo.width) // 2
        ly = (size - logo.height) // 2 - 2

        plate.alpha_composite(
            logo,
            (lx, ly)
        )

    else:
        draw.ellipse(
            (28, 28, size - 36, size - 36),
            outline=(190, 196, 210, 255),
            width=3
        )

    image.alpha_composite(
        plate,
        (
            int(cx - size / 2),
            int(cy - size / 2)
        )
    )


# ============================================================
# کارت مسابقه — طراحی کاملاً جدید
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
    draw = ImageDraw.Draw(image)

    accent = LEAGUE_COLORS.get(
        match["competition_code"],
        (105, 90, 235)
    )

    # سایه
    add_shadow(
        image,
        (
            x,
            y,
            x + width,
            y + height
        ),
        26,
        20,
        8
    )

    # بدنه
    rounded(
        draw,
        (
            x,
            y,
            x + width,
            y + height
        ),
        26,
        (17, 22, 41, 255),
        (42, 49, 73, 255),
        1
    )

    # نوار رنگی بالا
    rounded(
        draw,
        (
            x,
            y,
            x + width,
            y + 8
        ),
        4,
        accent
    )

    # شماره
    badge = 46
    bx = x + 22
    by = y + 21

    rounded(
        draw,
        (
            bx,
            by,
            bx + badge,
            by + badge
        ),
        15,
        (255, 255, 255, 16),
        (255, 255, 255, 25),
        1
    )

    num_font = get_font(
        21,
        bold=True
    )

    draw_center(
        draw,
        bx + badge / 2,
        by + badge / 2 + 1,
        persian_digits(number),
        num_font,
        (232, 235, 244)
    )

    # نام لیگ به صورت کپسولی
    league = repair_text(
        match["league_name"]
    )

    league_font = fit_font(
        draw,
        league,
        width - 170,
        24,
        17
    )

    league_width = text_width(
        draw,
        league,
        league_font
    )

    pill_width = min(
        width - 105,
        league_width + 32
    )

    pill_x2 = x + width - 22
    pill_x1 = pill_x2 - pill_width

    rounded(
        draw,
        (
            pill_x1,
            y + 20,
            pill_x2,
            y + 64
        ),
        15,
        tuple(accent) + (28,),
        tuple(accent) + (90,),
        1
    )

    draw_rtl(
        draw,
        (
            pill_x2 - 14,
            y + 42
        ),
        league,
        league_font,
        (232, 235, 244),
        anchor="rm"
    )

    # خط ظریف
    draw.line(
        (
            x + 22,
            y + 82,
            x + width - 22,
            y + 82
        ),
        fill=(255, 255, 255, 25),
        width=1
    )

    # جای لوگوها
    home_x = x + width * 0.25
    away_x = x + width * 0.75
    center_x = x + width / 2
    logo_y = y + 153

    draw_logo(
        image,
        match["home_logo"],
        home_x,
        logo_y,
        116
    )

    draw_logo(
        image,
        match["away_logo"],
        away_x,
        logo_y,
        116
    )

    # VS با فونت لاتین تا هیچ مربع/گلیف خراب ایجاد نشود
    vs_font = get_font(
        18,
        bold=True,
        latin=True
    )

    draw.text(
        (center_x, y + 129),
        "VS",
        font=vs_font,
        fill=(111, 121, 148),
        anchor="mm"
    )

    # کپسول ساعت
    time_width = 146
    time_height = 54

    time_x = center_x - time_width / 2
    time_y = y + 184

    rounded(
        draw,
        (
            time_x,
            time_y,
            time_x + time_width,
            time_y + time_height
        ),
        17,
        tuple(accent) + (255,)
    )

    time_font = get_font(
        29,
        bold=True
    )

    draw_center(
        draw,
        center_x,
        time_y + time_height / 2 + 1,
        persian_digits(match["time"]),
        time_font,
        (255, 255, 255)
    )

    # نام تیم‌ها
    home = repair_text(
        match["home"]
    )

    away = repair_text(
        match["away"]
    )

    home_font = fit_font(
        draw,
        home,
        width * 0.37,
        28,
        18
    )

    away_font = fit_font(
        draw,
        away,
        width * 0.37,
        28,
        18
    )

    draw_center(
        draw,
        home_x,
        y + 274,
        home,
        home_font,
        (247, 248, 252)
    )

    draw_center(
        draw,
        away_x,
        y + 274,
        away,
        away_font,
        (247, 248, 252)
    )

    # میزبان / مهمان
    small_font = get_font(
        16,
        bold=False
    )

    draw_center(
        draw,
        home_x,
        y + 312,
        "میزبان",
        small_font,
        (111, 120, 145)
    )

    draw_center(
        draw,
        away_x,
        y + 312,
        "مهمان",
        small_font,
        (111, 120, 145)
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

    rows = math.ceil(
        len(matches) / columns
    )

    height = (
        HEADER_HEIGHT
        + rows * CARD_HEIGHT
        + max(0, rows - 1) * GAP
        + FOOTER_HEIGHT
        + 34
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
            7
        ),
        fill=(128, 86, 245, 255)
    )

    # عنوان کوچک انگلیسی
    mini_font = get_font(
        18,
        bold=True,
        latin=True
    )

    draw.text(
        (
            MARGIN,
            44
        ),
        "MATCHDAY",
        font=mini_font,
        fill=(151, 137, 255)
    )

    # تاریخ
    date_font = get_font(
        21,
        bold=True
    )

    date_label = (
        "تاریخ  "
        + persian_digits(
            format_date(
                get_today()
            )
        )
    )

    date_width = text_width(
        draw,
        date_label,
        date_font
    )

    date_box_width = max(
        230,
        date_width + 34
    )

    rounded(
        draw,
        (
            MARGIN,
            83,
            MARGIN + date_box_width,
            135
        ),
        16,
        (255, 255, 255, 13),
        (255, 255, 255, 28),
        1
    )

    draw_rtl(
        draw,
        (
            MARGIN + date_box_width - 16,
            109
        ),
        date_label,
        date_font,
        (220, 224, 236),
        anchor="rm"
    )

    # عنوان اصلی
    title_font = get_font(
        70,
        bold=True
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            83
        ),
        "بازی‌های امروز",
        title_font,
        (250, 250, 253),
        anchor="ra"
    )

    # زیرعنوان
    subtitle_font = get_font(
        24,
        bold=False
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            168
        ),
        "برنامه مسابقات فوتبال امروز",
        subtitle_font,
        (135, 144, 169),
        anchor="ra"
    )

    # تعداد بازی‌ها
    count_font = get_font(
        22,
        bold=True
    )

    count_text = (
        persian_digits(
            len(matches)
        )
        + " مسابقه"
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            216
        ),
        count_text,
        count_font,
        (177, 184, 205),
        anchor="ra"
    )

    # خط جداکننده
    draw.line(
        (
            MARGIN,
            267,
            WIDTH - MARGIN,
            267
        ),
        fill=(255, 255, 255, 30),
        width=1
    )

    draw.ellipse(
        (
            MARGIN,
            260,
            MARGIN + 14,
            274
        ),
        fill=(128, 86, 245, 255)
    )

    # کارت‌ها
    start_y = HEADER_HEIGHT

    for index, match in enumerate(matches):
        row = index // columns
        col = index % columns

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
                CARD_HEIGHT
                + GAP
            )
        )

        draw_match_card(
            image,
            match,
            x,
            y,
            card_width,
            CARD_HEIGHT,
            index + 1
        )

    # فوتر
    footer_y = (
        start_y
        + rows * CARD_HEIGHT
        + max(0, rows - 1) * GAP
        + 24
    )

    draw.line(
        (
            MARGIN,
            footer_y,
            WIDTH - MARGIN,
            footer_y
        ),
        fill=(255, 255, 255, 25),
        width=1
    )

    footer_font = get_font(
        18,
        bold=False
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            footer_y + 34
        ),
        "تمامی ساعت‌ها به وقت تهران",
        footer_font,
        (103, 112, 139),
        anchor="ra"
    )

    # خروجی
    output = io.BytesIO()

    image.convert("RGB").save(
        output,
        format="JPEG",
        quality=96,
        optimize=True
    )

    output.seek(0)

    return output


# ============================================================
# تلگرام
# ============================================================

def send_photo(photo, caption):
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


def send_message(message):
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


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("FOOTBALL DAILY BOT — NEW DESIGN")
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
        f"Today in Tehran: {today}"
    )

    all_matches = []

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

            if status in (
                "CANCELLED",
                "POSTPONED"
            ):
                continue

            utc = match.get(
                "utcDate"
            )

            if not utc:
                continue

            home_data = match.get(
                "homeTeam",
                {}
            ) or {}

            away_data = match.get(
                "awayTeam",
                {}
            ) or {}

            home_original = repair_text(
                home_data.get(
                    "name",
                    "تیم میزبان"
                )
            )

            away_original = repair_text(
                away_data.get(
                    "name",
                    "تیم مهمان"
                )
            )

            home_name = team_display_name(
                home_original
            )

            away_name = team_display_name(
                away_original
            )

            all_matches.append(
                {
                    "competition_code": code,
                    "league_name": league_name,
                    "home": home_name,
                    "away": away_name,
                    "home_logo": download_logo(
                        home_data.get("crest")
                    ),
                    "away_logo": download_logo(
                        away_data.get("crest")
                    ),
                    "time": match_time(utc),
                    "utc": utc
                }
            )

    all_matches.sort(
        key=lambda item: item["utc"]
    )

    print(
        f"TOTAL MATCHES: {len(all_matches)}"
    )

    if not all_matches:
        message = (
            "⚽ بازی‌های امروز\n\n"
            f"📅 تاریخ: {format_date(today)}\n\n"
            "در ۹ لیگ منتخب امروز "
            "مسابقه‌ای پیدا نشد."
        )

        send_message(message)

        print(
            "No matches found."
        )

        return

    print(
        "Creating new poster..."
    )

    poster = create_poster(
        all_matches
    )

    caption = (
        "⚽ بازی‌های امروز\n"
        f"📅 {format_date(today)}\n"
        f"🎯 {persian_digits(len(all_matches))} مسابقه\n"
        "🕐 تمامی ساعت‌ها به وقت تهران"
    )

    send_photo(
        poster,
        caption
    )

    print(
        "DONE"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
