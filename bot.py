import os
import time
import requests

from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")


# ============================================================
# API
# ============================================================

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"


# ============================================================
# COMPETITIONS
# ============================================================

COMPETITIONS = {
    "PL": "🏴 لیگ برتر انگلیس",
    "PD": "🇪🇸 لالیگا",
    "SA": "🇮🇹 سری آ",
    "BL1": "🇩🇪 بوندسلیگا",
    "FL1": "🇫🇷 لیگ ۱ فرانسه",
    "DED": "🇳🇱 اردیویسه",
    "PPL": "🇵🇹 لیگ پرتغال",
    "BSA": "🇧🇷 سری آ برزیل",
    "CL": "🏆 لیگ قهرمانان اروپا",
}


# ============================================================
# TEAM NAMES - PERSIAN
# ============================================================

TEAM_NAMES = {

    # --------------------------------------------------------
    # England
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
    # Spain
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
    # Italy
    # --------------------------------------------------------

    "FC Internazionale Milano": "اینتر",
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

    # --------------------------------------------------------
    # Germany
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
    # France
    # --------------------------------------------------------

    "Paris Saint-Germain FC": "پاری‌سن‌ژرمن",
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

    # --------------------------------------------------------
    # Netherlands
    # --------------------------------------------------------

    "AFC Ajax": "آژاکس",
    "PSV": "آیندهوون",
    "Feyenoord Rotterdam": "فاینورد",
    "AZ": "آلکمار",
    "FC Twente '65": "توئنته",
    "FC Utrecht": "اوترخت",

    # --------------------------------------------------------
    # Portugal
    # --------------------------------------------------------

    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "SC Braga": "براگا",
    "Vitória SC": "ویتوریا گیمارش",

    # --------------------------------------------------------
    # Brazil
    # --------------------------------------------------------

    "CR Flamengo": "فلامینگو",
    "SE Palmeiras": "پالمیراس",
    "Botafogo FR": "بوتافوگو",
    "Fluminense FC": "فلومیننزه",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
}


# ============================================================
# COUNTRY FLAGS
# ============================================================

COUNTRY_FLAGS = {
    "PL": "🇬🇧",
    "PD": "🇪🇸",
    "SA": "🇮🇹",
    "BL1": "🇩🇪",
    "FL1": "🇫🇷",
    "DED": "🇳🇱",
    "PPL": "🇵🇹",
    "BSA": "🇧🇷",
    "CL": "🇪🇺",
}


# ============================================================
# LOGO CACHE
# ============================================================

logo_cache = {}


# ============================================================
# FONT
# ============================================================

def get_font(size):
    """
    پیدا کردن فونت مناسب.
    اول فونت تعریف‌شده توسط FONT_PATH را امتحان می‌کند.
    سپس چند مسیر معمول لینوکس را بررسی می‌کند.
    """

    custom_font = os.getenv("FONT_PATH")

    font_paths = []

    if custom_font:
        font_paths.append(custom_font)

    font_paths.extend([
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    ])

    for path in font_paths:

        if os.path.exists(path):

            try:
                return ImageFont.truetype(
                    path,
                    size
                )

            except Exception:
                pass

    # آخرین fallback
    return ImageFont.load_default()


# ============================================================
# TELEGRAM SEND MESSAGE
# ============================================================

def send_message(text):

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
        "Telegram message:",
        response.status_code
    )

    print(response.text)

    return response.ok


# ============================================================
# DOWNLOAD TEAM LOGO
# ============================================================

def download_logo(url):

    if not url:
        return None

    # اگر قبلاً دانلود شده
    if url in logo_cache:
        return logo_cache[url]

    try:

        response = requests.get(
            url,
            timeout=20
        )

        if response.status_code != 200:

            print(
                "Logo download failed:",
                response.status_code,
                url
            )

            return None

        image = Image.open(
            BytesIO(response.content)
        ).convert("RGBA")

        # اندازه مناسب برای کارت
        image.thumbnail(
            (70, 70),
            Image.Resampling.LANCZOS
        )

        logo_cache[url] = image

        return image

    except Exception as e:

        print(
            "Logo error:",
            e
        )

        return None


# ============================================================
# PERSIAN TEXT DRAWING
# ============================================================

def draw_rtl_text(
    draw,
    xy,
    text,
    font,
    fill
):
    """
    تلاش برای نمایش درست متن فارسی.
    Pillow در محیط‌هایی که libraqm داشته باشند
    RTL و shaping را انجام می‌دهد.
    """

    x, y = xy

    try:

        draw.text(
            (x, y),
            text,
            font=font,
            fill=fill,
            anchor="mm",
            direction="rtl",
            language="fa"
        )

    except Exception:

        draw.text(
            (x, y),
            text,
            font=font,
            fill=fill,
            anchor="mm"
        )


# ============================================================
# CREATE MATCH CARD
# ============================================================

def create_match_card(
    home,
    away,
    home_logo,
    away_logo,
    time_text,
    league
):
    """
    ساخت یک کارت کوچک برای یک بازی.

    خروجی:
        PNG داخل BytesIO
    """

    # --------------------------------------------------------
    # CARD SIZE
    # --------------------------------------------------------

    width = 900
    height = 180

    background = (255, 255, 255)
    text_color = (30, 30, 30)
    secondary_color = (110, 110, 110)
    border_color = (225, 225, 225)

    image = Image.new(
        "RGB",
        (width, height),
        background
    )

    draw = ImageDraw.Draw(image)

    # --------------------------------------------------------
    # BORDER
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            2,
            2,
            width - 3,
            height - 3
        ),
        radius=25,
        outline=border_color,
        width=3
    )

    # --------------------------------------------------------
    # FONTS
    # --------------------------------------------------------

    team_font = get_font(34)
    time_font = get_font(38)
    league_font = get_font(22)

    # --------------------------------------------------------
    # POSITIONS
    # --------------------------------------------------------

    # سمت راست = میزبان
    home_logo_x = 760
    home_text_x = 650

    # سمت چپ = مهمان
    away_logo_x = 140
    away_text_x = 250

    center_x = width // 2

    # --------------------------------------------------------
    # LEAGUE
    # --------------------------------------------------------

    draw_rtl_text(
        draw,
        (center_x, 28),
        league,
        league_font,
        secondary_color
    )

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    draw.text(
        (center_x, 105),
        time_text,
        font=time_font,
        fill=text_color,
        anchor="mm"
    )

    # --------------------------------------------------------
    # HOME LOGO
    # --------------------------------------------------------

    if home_logo:

        logo = home_logo.copy()

        logo.thumbnail(
            (70, 70),
            Image.Resampling.LANCZOS
        )

        logo_x = (
            home_logo_x
            - logo.width // 2
        )

        logo_y = (
            100
            - logo.height // 2
        )

        image.paste(
            logo,
            (logo_x, logo_y),
            logo
        )

    # --------------------------------------------------------
    # AWAY LOGO
    # --------------------------------------------------------

    if away_logo:

        logo = away_logo.copy()

        logo.thumbnail(
            (70, 70),
            Image.Resampling.LANCZOS
        )

        logo_x = (
            away_logo_x
            - logo.width // 2
        )

        logo_y = (
            100
            - logo.height // 2
        )

        image.paste(
            logo,
            (logo_x, logo_y),
            logo
        )

    # --------------------------------------------------------
    # HOME TEAM NAME
    # --------------------------------------------------------

    draw_rtl_text(
        draw,
        (home_text_x, 105),
        home,
        team_font,
        text_color
    )

    # --------------------------------------------------------
    # AWAY TEAM NAME
    # --------------------------------------------------------

    draw_rtl_text(
        draw,
        (away_text_x, 105),
        away,
        team_font,
        text_color
    )

    # --------------------------------------------------------
    # RETURN PNG
    # --------------------------------------------------------

    output = BytesIO()

    image.save(
        output,
        format="PNG"
    )

    output.seek(0)

    return output


# ============================================================
# SEND MATCH CARD TO TELEGRAM
# ============================================================

def send_match_card(
    match,
    league,
    flag
):

    home_team = match.get(
        "homeTeam",
        {}
    )

    away_team = match.get(
        "awayTeam",
        {}
    )

    # --------------------------------------------------------
    # ORIGINAL TEAM NAMES
    # --------------------------------------------------------

    home_original = home_team.get(
        "name",
        "تیم میزبان"
    )

    away_original = away_team.get(
        "name",
        "تیم مهمان"
    )

    # --------------------------------------------------------
    # PERSIAN TEAM NAMES
    # --------------------------------------------------------

    home = TEAM_NAMES.get(
        home_original,
        home_original
    )

    away = TEAM_NAMES.get(
        away_original,
        away_original
    )

    # --------------------------------------------------------
    # CRESTS
    # --------------------------------------------------------

    home_crest = home_team.get(
        "crest"
    )

    away_crest = away_team.get(
        "crest"
    )

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------
    
    utc_date = match.get(
        "utcDate"
    )

    if not utc_date:
        time_text = "--:--"
    else:
        try:
            dt = datetime.fromisoformat(
                utc_date.replace(
                    "Z",
                    "+00:00"
                )
            )

            iran_timezone = ZoneInfo(
                "Asia/Tehran"
            )

            iran_time = dt.astimezone(
                iran_timezone
            )

            time_text = iran_time.strftime(
                "%H:%M"
            )

        except Exception as e:
            print(
                "Time conversion error:",
                e
            )

            time_text = "--:--"

    # --------------------------------------------------------
    # DOWNLOAD LOGOS
    # --------------------------------------------------------

    home_logo = download_logo(
        home_crest
    )

    away_logo = download_logo(
        away_crest
    )

    # --------------------------------------------------------
    # IF BOTH LOGOS EXIST
    # --------------------------------------------------------

    if home_logo and away_logo:

        try:

            card = create_match_card(
                home=home,
                away=away,
                home_logo=home_logo,
                away_logo=away_logo,
                time_text=time_text,
                league=league
            )

            url = (
                f"https://api.telegram.org/"
                f"bot{BOT_TOKEN}/sendPhoto"
            )

            response = requests.post(
                url,
                data={
                    "chat_id": CHAT_ID
                },
                files={
                    "photo": (
                        "match.png",
                        card,
                        "image/png"
                    )
                },
                timeout=30
            )

            print(
                "Telegram card:",
                home,
                "vs",
                away,
                response.status_code
            )

            print(response.text)

            if response.ok:
                return True

        except Exception as e:

            print(
                "Card creation/send error:",
                e
            )

    # --------------------------------------------------------
    # FALLBACK TEXT
    # --------------------------------------------------------

    fallback = (
        f"{league}\n"
        f"⚽ {flag} {home} - {flag} {away}\n"
        f"🕐 {time_text}"
    )

    return send_message(
        fallback
    )


# ============================================================
# GET TODAY
# ============================================================

def get_today():

    return datetime.now(
        ZoneInfo("Asia/Tehran")
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

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    print(
        competition,
        "API:",
        response.status_code
    )

    # --------------------------------------------------------
    # RATE LIMIT
    # --------------------------------------------------------

    if response.status_code == 429:

        print(
            "Rate limit reached."
        )

        print(
            "Waiting 45 seconds..."
        )

        time.sleep(45)

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        print(
            competition,
            "API after waiting:",
            response.status_code
        )

    # --------------------------------------------------------
    # ERROR
    # --------------------------------------------------------

    if response.status_code != 200:

        print(
            response.text[:500]
        )

        return []

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    data = response.json()

    return data.get(
        "matches",
        []
    )


# ============================================================
# MAIN
# ============================================================

def main():

    date = get_today()

    print(
        "================================"
    )

    print(
        "FOOTBALL ALERT BOT"
    )

    print(
        "IRAN DATE:",
        date
    )

    print(
        "================================"
    )

    all_matches = []

    # --------------------------------------------------------
    # GET ALL LEAGUES
    # --------------------------------------------------------

    for competition, league_name in COMPETITIONS.items():

        print(
            "Checking:",
            league_name
        )

        matches = get_matches(
            competition,
            date
        )

        for match in matches:

            match["league_code"] = (
                competition
            )

            match["league_name"] = (
                league_name
            )

            all_matches.append(
                match
            )

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    print(
        "TOTAL MATCHES:",
        len(all_matches)
    )

    # --------------------------------------------------------
    # NO MATCHES
    # --------------------------------------------------------

    if not all_matches:

        send_message(
            f"⚽ بازی‌ای برای امروز پیدا نشد.\n\n"
            f"📅 تاریخ: {date}"
        )

        return

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    header = (
        f"⚽ بازی‌های امروز\n"
        f"📅 تاریخ: {date}\n\n"
        f"🛡️ مسابقات ۹ لیگ منتخب"
    )

    send_message(
        header
    )

    # --------------------------------------------------------
    # SEND MATCH CARDS
    # --------------------------------------------------------

    for match in all_matches:

        competition = match[
            "league_code"
        ]

        league = match[
            "league_name"
        ]

        flag = COUNTRY_FLAGS.get(
            competition,
            "⚽"
        )

        send_match_card(
            match,
            league,
            flag
        )

        time.sleep(1)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
