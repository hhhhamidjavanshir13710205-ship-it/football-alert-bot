import os
import io
import time
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display


# =========================================================
# تنظیمات
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

TEHRAN = ZoneInfo("Asia/Tehran")

WIDTH = 1600
MARGIN = 70
GAP = 28
EXPORT_SCALE = 2
LOGO_MAX_SIZE = 420

OUTPUT_WIDTH = WIDTH * EXPORT_SCALE


# =========================================================
# لیگ‌ها
# =========================================================

COMPETITIONS = {
    "PL": "لیگ برتر انگلیس",
    "PD": "لالیگا",
    "SA": "سری آ ایتالیا",
    "BL1": "بوندس‌لیگا",
    "FL1": "لیگ ۱ فرانسه",
    "DED": "اردیویسه هلند",
    "PPL": "لیگ برتر پرتغال",
    "BSA": "سری آ برزیل",
    "CL": "لیگ قهرمانان اروپا",
}


LEAGUE_COLORS = {
    "PL": (60, 105, 210),
    "PD": (225, 75, 75),
    "SA": (55, 125, 220),
    "BL1": (220, 60, 60),
    "FL1": (65, 90, 180),
    "DED": (235, 125, 45),
    "PPL": (40, 150, 105),
    "BSA": (50, 150, 95),
    "CL": (80, 90, 190),
}


LEAGUE_ICONS = {
    "PL": "🏴",
    "PD": "🇪🇸",
    "SA": "🇮🇹",
    "BL1": "🇩🇪",
    "FL1": "🇫🇷",
    "DED": "🇳🇱",
    "PPL": "🇵🇹",
    "BSA": "🇧🇷",
    "CL": "⭐",
}


# =========================================================
# نام تیم‌ها
# =========================================================

TEAM_NAMES = {

    # England
    "Arsenal FC": "آرسنال",
    "Aston Villa FC": "استون ویلا",
    "AFC Bournemouth": "بورنموث",
    "Brentford FC": "برنتفورد",
    "Brighton & Hove Albion": "برایتون",
    "Chelsea FC": "چلسی",
    "Crystal Palace FC": "کریستال پالاس",
    "Everton FC": "اورتون",
    "Fulham FC": "فولام",
    "Leeds United FC": "لیدز یونایتد",
    "Liverpool FC": "لیورپول",
    "Manchester City FC": "منچسترسیتی",
    "Manchester United FC": "منچستریونایتد",
    "Newcastle United FC": "نیوکاسل",
    "Nottingham Forest FC": "ناتینگهام فارست",
    "Sunderland AFC": "ساندرلند",
    "Tottenham Hotspur FC": "تاتنهام",
    "West Ham United FC": "وستهم",
    "Wolverhampton Wanderers FC": "ولورهمپتون",

    # Spain
    "Real Madrid CF": "رئال مادرید",
    "FC Barcelona": "بارسلونا",
    "Club Atlético de Madrid": "اتلتیکومادرید",
    "Club Atletico de Madrid": "اتلتیکومادرید",
    "Athletic Club": "اتلتیک بیلبائو",
    "Real Sociedad de Fútbol": "رئال سوسیداد",
    "Real Betis": "رئال بتیس",
    "Sevilla FC": "سویا",
    "Villarreal CF": "ویارئال",
    "Valencia CF": "والنسیا",
    "Girona FC": "ژیرونا",

    # Italy
    "Inter": "اینتر",
    "AC Milan": "آث میلان",
    "Juventus FC": "یوونتوس",
    "SSC Napoli": "ناپولی",
    "AS Roma": "رم",
    "SS Lazio": "لاتزیو",
    "Atalanta BC": "آتالانتا",
    "ACF Fiorentina": "فیورنتینا",

    # Germany
    "FC Bayern München": "بایرن مونیخ",
    "Borussia Dortmund": "بوروسیا دورتموند",
    "Bayer 04 Leverkusen": "بایرلورکوزن",
    "RB Leipzig": "لایپزیگ",
    "Eintracht Frankfurt": "آینتراخت فرانکفورت",
    "VfB Stuttgart": "اشتوتگارت",

    # France
    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
    "Olympique de Marseille": "مارسی",
    "Olympique Lyonnais": "لیون",
    "AS Monaco FC": "موناکو",
    "LOSC Lille": "لیل",
    "OGC Nice": "نیس",

    # Netherlands
    "Ajax": "آژاکس",
    "PSV": "پی‌اس‌وی آیندهوون",
    "Feyenoord": "فاینورد",
    "FC Utrecht": "اوترخت",

    # Portugal
    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting CP": "اسپورتینگ",
    "SC Braga": "براگا",

    # Brazil
    "Flamengo": "فلامینگو",
    "Palmeiras": "پالمیراس",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
    "Santos FC": "سانتوس",

}


# =========================================================
# فونت
# =========================================================

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf",
    "/usr/share/fonts/opentype/noto/NotoKufiArabic-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

FONT_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf",
    "/usr/share/fonts/opentype/noto/NotoKufiArabic-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def find_font(candidates):
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


FONT_REGULAR = find_font(FONT_CANDIDATES)
FONT_BOLD = find_font(FONT_BOLD_CANDIDATES)


if not FONT_REGULAR:
    raise RuntimeError("فونت مناسب پیدا نشد.")

if not FONT_BOLD:
    FONT_BOLD = FONT_REGULAR


def font(size, bold=False):
    return ImageFont.truetype(
        FONT_BOLD if bold else FONT_REGULAR,
        size
    )


# =========================================================
# فارسی / RTL
# =========================================================

def rtl(text):
    """
    آماده‌سازی متن فارسی برای Pillow
    """
    if text is None:
        return ""

    text = str(text)

    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def repair_text(text):
    """
    تلاش برای اصلاح متن‌های خراب UTF-8 / CP1256.
    برای متن‌های سالم هیچ تغییری ایجاد نمی‌کند.
    """

    if not text:
        return ""

    text = str(text)

    bad_markers = [
        "ط§",
        "ط¨",
        "ط©",
        "ط·",
        "آ",
        "Ã",
        "â€",
        "ð",
    ]

    if not any(marker in text for marker in bad_markers):
        return text

    attempts = []

    for source_encoding in ("cp1256", "latin1"):
        try:
            repaired = text.encode(source_encoding).decode("utf-8")
            attempts.append(repaired)
        except Exception:
            pass

    if attempts:
        # متنی که کمترین نشانه خرابی را داشته باشد انتخاب می‌کنیم.
        def score(value):
            bad = sum(value.count(x) for x in bad_markers)
            return bad

        return min(attempts, key=score)

    return text


# =========================================================
# API
# =========================================================

session = requests.Session()

session.headers.update({
    "X-Auth-Token": FOOTBALL_API_TOKEN or ""
})


def get_today():
    return datetime.now(TEHRAN).date()


def format_date(date_obj):
    return date_obj.strftime("%Y/%m/%d")


def fetch_matches(competition_code, date_obj):
    date_str = date_obj.strftime("%Y-%m-%d")

    url = API_URL.format(competition_code)

    params = {
        "dateFrom": date_str,
        "dateTo": date_str,
    }

    for attempt in range(3):

        try:
            response = session.get(
                url,
                params=params,
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("matches", [])

            if response.status_code == 429:
                print("محدودیت API. ۴۵ ثانیه صبر می‌کنیم...")
                time.sleep(45)
                continue

            print(
                f"خطای API برای {competition_code}: "
                f"{response.status_code}"
            )

        except requests.RequestException as exc:
            print(
                f"خطای اتصال برای {competition_code}: {exc}"
            )

        if attempt < 2:
            time.sleep(5)

    return []


# =========================================================
# نام تیم
# =========================================================

def get_team_display_name(team_name):
    if not team_name:
        return "نامشخص"

    original = str(team_name)
    repaired = repair_text(original)

    # ابتدا نام اصلی
    if original in TEAM_NAMES:
        return TEAM_NAMES[original]

    # سپس نسخه اصلاح‌شده
    if repaired in TEAM_NAMES:
        return TEAM_NAMES[repaired]

    # جستجوی بدون حساسیت به شکل نوشتاری
    for key, value in TEAM_NAMES.items():

        if repair_text(key) == repaired:
            return value

        if key.lower() == repaired.lower():
            return value

    return repaired


# =========================================================
# زمان بازی
# =========================================================

def match_time(utc_date):
    try:
        dt = datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )

        local_dt = dt.astimezone(TEHRAN)

        return local_dt.strftime("%H:%M")

    except Exception:
        return "--:--"


def match_datetime(utc_date):
    try:
        return datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )
    except Exception:
        return datetime.max


# =========================================================
# دانلود لوگو
# =========================================================

LOGO_CACHE = {}


def download_logo(url):
    if not url:
        return None

    if url in LOGO_CACHE:
        return LOGO_CACHE[url]

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        image = Image.open(
            io.BytesIO(response.content)
        ).convert("RGBA")

        image.thumbnail(
            (LOGO_MAX_SIZE, LOGO_MAX_SIZE),
            Image.Resampling.LANCZOS
        )

        LOGO_CACHE[url] = image

        return image

    except Exception as exc:
        print(f"خطا در دریافت لوگو: {exc}")

        LOGO_CACHE[url] = None

        return None


# =========================================================
# ابزارهای گرافیکی
# =========================================================

def rounded_rectangle(
    draw,
    xy,
    radius,
    fill,
    outline=None,
    width=1
):
    draw.rounded_rectangle(
        xy,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width
    )


def text_bbox(draw, text, fnt):
    return draw.textbbox(
        (0, 0),
        text,
        font=fnt
    )


def text_width(draw, text, fnt):
    box = text_bbox(draw, text, fnt)
    return box[2] - box[0]


def centered_text(
    draw,
    center_x,
    y,
    text,
    fnt,
    fill,
):
    shaped = rtl(text)

    box = draw.textbbox(
        (0, 0),
        shaped,
        font=fnt
    )

    width = box[2] - box[0]

    draw.text(
        (
            center_x - width / 2,
            y
        ),
        shaped,
        font=fnt,
        fill=fill,
    )


def draw_rtl(
    draw,
    xy,
    text,
    fnt,
    fill,
    anchor="ra",
):
    shaped = rtl(text)

    draw.text(
        xy,
        shaped,
        font=fnt,
        fill=fill,
        anchor=anchor,
    )


def fit_font(
    draw,
    text,
    max_width,
    start_size,
    min_size=18,
    bold=False,
):
    size = start_size

    while size >= min_size:

        fnt = font(size, bold)

        shaped = rtl(text)

        box = draw.textbbox(
            (0, 0),
            shaped,
            font=fnt
        )

        width = box[2] - box[0]

        if width <= max_width:
            return fnt

        size -= 2

    return font(min_size, bold)


# =========================================================
# پس‌زمینه
# =========================================================

def create_background(width, height):
    image = Image.new(
        "RGB",
        (width, height),
        (8, 12, 24)
    )

    draw = ImageDraw.Draw(image)

    top = (12, 19, 38)
    bottom = (5, 8, 17)

    for y in range(height):
        ratio = y / max(1, height - 1)

        color = tuple(
            int(
                top[i] * (1 - ratio)
                + bottom[i] * ratio
            )
            for i in range(3)
        )

        draw.line(
            [(0, y), (width, y)],
            fill=color
        )

    # نورهای محو
    glow = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    glow_draw.ellipse(
        (
            -300,
            -250,
            650,
            700
        ),
        fill=(45, 80, 180, 75)
    )

    glow_draw.ellipse(
        (
            width - 650,
            -250,
            width + 300,
            650
        ),
        fill=(100, 50, 180, 55)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(120)
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        glow
    ).convert("RGB")

    return image


# =========================================================
# سایه
# =========================================================

def draw_shadow(
    base,
    box,
    radius=30,
    blur=25,
    offset=(0, 15),
    opacity=110,
):
    shadow = Image.new(
        "RGBA",
        base.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(shadow)

    x1, y1, x2, y2 = box

    ox, oy = offset

    draw.rounded_rectangle(
        (
            x1 + ox,
            y1 + oy,
            x2 + ox,
            y2 + oy,
        ),
        radius=radius,
        fill=(0, 0, 0, opacity)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(blur)
    )

    base.alpha_composite(shadow)


# =========================================================
# لوگو
# =========================================================

def draw_logo(
    base,
    logo,
    center_x,
    center_y,
    max_size=190,
):
    if logo is None:
        return

    image = logo.copy()

    image.thumbnail(
        (max_size, max_size),
        Image.Resampling.LANCZOS
    )

    x = int(
        center_x - image.width / 2
    )

    y = int(
        center_y - image.height / 2
    )

    base.alpha_composite(
        image,
        (x, y)
    )


# =========================================================
# بج لیگ
# =========================================================

def league_badge(
    draw,
    x,
    y,
    code,
    league_name,
):
    color = LEAGUE_COLORS.get(
        code,
        (80, 100, 150)
    )

    icon = LEAGUE_ICONS.get(
        code,
        "⚽"
    )

    # Badge
    draw.rounded_rectangle(
        (
            x,
            y,
            x + 255,
            y + 54
        ),
        radius=27,
        fill=color
    )

    centered_text(
        draw,
        x + 30,
        y + 11,
        icon,
        font(25),
        (255, 255, 255)
    )

    draw_rtl(
        draw,
        (
            x + 225,
            y + 27
        ),
        league_name,
        font(22, True),
        (255, 255, 255),
        anchor="ra"
    )


# =========================================================
# کارت بازی
# =========================================================

def draw_match_card(
    image,
    draw,
    match,
    index,
    x,
    y,
    width,
    height,
):
    code = match["competition"]

    league_name = COMPETITIONS.get(
        code,
        code
    )

    league_name = repair_text(
        league_name
    )

    color = LEAGUE_COLORS.get(
        code,
        (80, 100, 150)
    )

    home = match["home"]
    away = match["away"]

    home_name = get_team_display_name(
        home["name"]
    )

    away_name = get_team_display_name(
        away["name"]
    )

    home_logo = download_logo(
        home.get("crest")
    )

    away_logo = download_logo(
        away.get("crest")
    )

    # سایه
    draw_shadow(
        image,
        (
            x,
            y,
            x + width,
            y + height
        ),
        radius=30,
        blur=24,
        offset=(0, 12),
        opacity=120
    )

    # کارت
    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + height
        ),
        radius=30,
        fill=(18, 24, 40),
        outline=(42, 53, 76),
        width=2
    )

    # نوار بالایی
    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + 85
        ),
        radius=30,
        fill=(23, 30, 50)
    )

    # اصلاح گوشه‌های پایین نوار
    draw.rectangle(
        (
            x,
            y + 55,
            x + width,
            y + 85
        ),
        fill=(23, 30, 50)
    )

    # خط رنگی لیگ
    draw.rectangle(
        (
            x,
            y,
            x + 8,
            y + height
        ),
        fill=color
    )

    # شماره بازی
    pill_x = x + 28
    pill_y = y + 18

    draw.rounded_rectangle(
        (
            pill_x,
            pill_y,
            pill_x + 70,
            pill_y + 46
        ),
        radius=23,
        fill=(32, 42, 64)
    )

    centered_text(
        draw,
        pill_x + 35,
        pill_y + 10,
        str(index),
        font(21, True),
        (235, 240, 250)
    )

    # نام لیگ
    draw_rtl(
        draw,
        (
            x + width - 30,
            y + 42
        ),
        league_name,
        font(22, True),
        (225, 230, 240),
        anchor="ra"
    )

    # Divider
    divider_y = y + 90

    draw.line(
        (
            x + 30,
            divider_y,
            x + width - 30,
            divider_y
        ),
        fill=(43, 52, 72),
        width=2
    )

    # مختصات
    center_x = x + width / 2

    home_x = x + width * 0.27
    away_x = x + width * 0.73

    logo_y = y + 205

    # لوگوها
    draw_logo(
        image,
        home_logo,
        home_x,
        logo_y,
        max_size=145
    )

    draw_logo(
        image,
        away_logo,
        away_x,
        logo_y,
        max_size=145
    )

    # نام تیم‌ها
    home_font = fit_font(
        draw,
        home_name,
        280,
        31,
        19,
        True
    )

    away_font = fit_font(
        draw,
        away_name,
        280,
        31,
        19,
        True
    )

    centered_text(
        draw,
        home_x,
        y + 285,
        home_name,
        home_font,
        (248, 249, 252)
    )

    centered_text(
        draw,
        away_x,
        y + 285,
        away_name,
        away_font,
        (248, 249, 252)
    )

    # میزبان / مهمان
    centered_text(
        draw,
        home_x,
        y + 330,
        "میزبان",
        font(19),
        (125, 140, 165)
    )

    centered_text(
        draw,
        away_x,
        y + 330,
        "مهمان",
        font(19),
        (125, 140, 165)
    )

    # VS
    draw.ellipse(
        (
            center_x - 45,
            y + 175,
            center_x + 45,
            y + 265
        ),
        fill=(28, 37, 58),
        outline=(65, 78, 105),
        width=2
    )

    centered_text(
        draw,
        center_x,
        y + 198,
        "VS",
        font(24, True),
        (225, 230, 240)
    )

    # زمان
    time_value = match_time(
        match["utcDate"]
    )

    time_y = y + height - 62

    draw.rounded_rectangle(
        (
            center_x - 90,
            time_y - 4,
            center_x + 90,
            time_y + 46
        ),
        radius=25,
        fill=color
    )

    centered_text(
        draw,
        center_x,
        time_y + 8,
        time_value,
        font(23, True),
        (255, 255, 255)
    )


# =========================================================
# ساخت پوستر
# =========================================================

def create_poster(matches):
    columns = 2

    card_width = (
        WIDTH
        - 2 * MARGIN
        - GAP
    ) // columns

    card_height = 395

    rows = (
        len(matches)
        + columns
        - 1
    ) // columns

    header_height = 385
    footer_height = 105

    height = (
        header_height
        + rows * card_height
        + max(0, rows - 1) * GAP
        + footer_height
        + 2 * MARGIN
    )

    image = create_background(
        WIDTH,
        height
    ).convert("RGBA")

    draw = ImageDraw.Draw(image)

    # =====================================================
    # Header
    # =====================================================

    centered_text(
        draw,
        WIDTH / 2,
        60,
        "FOOTBALL DAILY",
        font(54, True),
        (245, 247, 252)
    )

    centered_text(
        draw,
        WIDTH / 2,
        130,
        "MATCH CENTER",
        font(24, True),
        (120, 150, 205)
    )

    centered_text(
        draw,
        WIDTH / 2,
        195,
        "مرکز مسابقات فوتبال",
        font(42, True),
        (240, 243, 248)
    )

    today = get_today()

    centered_text(
        draw,
        WIDTH / 2,
        255,
        f"بازی‌های امروز | {format_date(today)}",
        font(25),
        (155, 168, 190)
    )

    centered_text(
        draw,
        WIDTH / 2,
        305,
        f"{len(matches)} مسابقه",
        font(22),
        (105, 125, 155)
    )

    # =====================================================
    # کارت‌ها
    # =====================================================

    start_y = header_height + MARGIN

    for i, match in enumerate(matches):

        row = i // columns
        col = i % columns

        x = (
            MARGIN
            + col * (
                card_width + GAP
            )
        )

        y = (
            start_y
            + row * (
                card_height + GAP
            )
        )

        draw_match_card(
            image=image,
            draw=draw,
            match=match,
            index=i + 1,
            x=x,
            y=y,
            width=card_width,
            height=card_height,
        )

    # =====================================================
    # Footer
    # =====================================================

    footer_y = height - footer_height

    draw.line(
        (
            MARGIN,
            footer_y,
            WIDTH - MARGIN,
            footer_y
        ),
        fill=(42, 52, 72),
        width=2
    )

    centered_text(
        draw,
        WIDTH / 2,
        footer_y + 28,
        "ساعت‌ها به وقت تهران",
        font(21),
        (125, 140, 165)
    )

    centered_text(
        draw,
        WIDTH / 2,
        footer_y + 62,
        "Football Daily",
        font(18, True),
        (80, 105, 145)
    )

    # =====================================================
    # خروجی با کیفیت بالا
    # =====================================================

    output = io.BytesIO()

    high_res = image.resize(
        (
            WIDTH * EXPORT_SCALE,
            height * EXPORT_SCALE
        ),
        Image.Resampling.LANCZOS
    )

    high_res.convert("RGB").save(
        output,
        format="PNG",
        optimize=True,
        compress_level=6
    )

    output.seek(0)

    return output


# =========================================================
# تلگرام
# =========================================================

def send_photo(photo_bytes, caption):
    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendPhoto"
    )

    files = {
        "photo": (
            "football_daily.png",
            photo_bytes,
            "image/png"
        )
    }

    data = {
        "chat_id": CHAT_ID,
        "caption": caption,
    }

    response = requests.post(
        url,
        files=files,
        data=data,
        timeout=60,
    )

    if not response.ok:
        raise RuntimeError(
            f"Telegram error: "
            f"{response.status_code} "
            f"{response.text}"
        )

    return response.json()


def send_message(text):
    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
        },
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"Telegram error: "
            f"{response.status_code} "
            f"{response.text}"
        )

    return response.json()


# =========================================================
# آماده‌سازی مسابقات
# =========================================================

def collect_matches(today):
    all_matches = []

    for code in COMPETITIONS:

        print(
            f"در حال دریافت مسابقات {code}..."
        )

        matches = fetch_matches(
            code,
            today
        )

        for match in matches:

            status = match.get(
                "status",
                ""
            )

            if status in {
                "CANCELLED",
                "POSTPONED"
            }:
                continue

            home_team = match.get(
                "homeTeam",
                {}
            )

            away_team = match.get(
                "awayTeam",
                {}
            )

            if not home_team.get("name"):
                continue

            if not away_team.get("name"):
                continue

            all_matches.append({
                "competition": code,
                "utcDate": match.get(
                    "utcDate"
                ),
                "home": {
                    "name": home_team.get(
                        "name"
                    ),
                    "crest": home_team.get(
                        "crest"
                    ),
                },
                "away": {
                    "name": away_team.get(
                        "name"
                    ),
                    "crest": away_team.get(
                        "crest"
                    ),
                },
            })

    all_matches.sort(
        key=lambda x: match_datetime(
            x["utcDate"]
        )
    )

    return all_matches


# =========================================================
# کپشن
# =========================================================

def create_caption(matches, today):

    lines = [
        "⚽ فوتبال دیلی",
        "",
        f"📅 بازی‌های امروز | {format_date(today)}",
        f"🏟 تعداد مسابقات: {len(matches)}",
        "",
    ]

    for index, match in enumerate(
        matches,
        start=1
    ):
        home = get_team_display_name(
            match["home"]["name"]
        )

        away = get_team_display_name(
            match["away"]["name"]
        )

        league = COMPETITIONS.get(
            match["competition"],
            match["competition"]
        )

        game_time = match_time(
            match["utcDate"]
        )

        lines.append(
            f"{index}. {home} - {away} | "
            f"{game_time} | {league}"
        )

    lines.extend([
        "",
        "🕐 تمام ساعت‌ها به وقت تهران"
    ])

    return "\n".join(lines)


# =========================================================
# Main
# =========================================================

def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN تنظیم نشده است."
        )

    if not CHAT_ID:
        raise RuntimeError(
            "CHAT_ID تنظیم نشده است."
        )

    if not FOOTBALL_API_TOKEN:
        raise RuntimeError(
            "FOOTBALL_API_TOKEN تنظیم نشده است."
        )

    today = get_today()

    print(
        f"تاریخ امروز: {format_date(today)}"
    )

    matches = collect_matches(
        today
    )

    print(
        f"تعداد مسابقات: {len(matches)}"
    )

    if not matches:

        send_message(
            "⚽ بازی فوتبالی برای امروز "
            "در لیگ‌های انتخاب‌شده پیدا نشد."
        )

        print(
            "هیچ مسابقه‌ای پیدا نشد."
        )

        return

    poster = create_poster(
        matches
    )

    caption = create_caption(
        matches,
        today
    )

    send_photo(
        poster,
        caption
    )

    print(
        "پوستر با موفقیت به تلگرام ارسال شد."
    )


if __name__ == "__main__":
    main()
