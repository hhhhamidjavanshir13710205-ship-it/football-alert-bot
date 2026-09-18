import os
import time
import requests

from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

# برای درست نمایش دادن فارسی
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    PERSIAN_SHAPING = True
except ImportError:
    PERSIAN_SHAPING = False


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
# CACHE
# ============================================================

logo_cache = {}


# ============================================================
# FONT
# ============================================================

def get_font(size, bold=False):

    custom_font = os.getenv("FONT_PATH")

    paths = []

    if custom_font:
        paths.append(custom_font)

    if bold:
        paths.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        ])
    else:
        paths.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        ])

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

def shape_persian(text):

    if not text:
        return text

    if not PERSIAN_SHAPING:
        return text

    try:

        reshaped = arabic_reshaper.reshape(text)

        return get_display(reshaped)

    except Exception:

        return text


def draw_rtl_text(
    draw,
    xy,
    text,
    font,
    fill,
    anchor="mm"
):

    draw.text(
        xy,
        shape_persian(text),
        font=font,
        fill=fill,
        anchor=anchor
    )


# ============================================================
# TELEGRAM MESSAGE
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
# TELEGRAM PHOTO
# ============================================================

def send_photo(photo):

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
                "today_matches.png",
                photo,
                "image/png"
            )
        },
        timeout=60
    )

    print(
        "Telegram poster:",
        response.status_code
    )

    print(response.text)

    return response.ok


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
                "Logo download failed:",
                response.status_code,
                url
            )

            return None

        image = Image.open(
            BytesIO(response.content)
        ).convert("RGBA")

        image.thumbnail(
            (72, 72),
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
# TIME CONVERSION
# ============================================================

def get_time_text(utc_date):

    if not utc_date:
        return "--:--"

    try:

        dt = datetime.fromisoformat(
            utc_date.replace(
                "Z",
                "+00:00"
            )
        )

        iran_time = dt.astimezone(
            ZoneInfo("Asia/Tehran")
        )

        return iran_time.strftime(
            "%H:%M"
        )

    except Exception as e:

        print(
            "Time conversion error:",
            e
        )

        return "--:--"


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

    try:

        data = response.json()

        return data.get(
            "matches",
            []
        )

    except Exception as e:

        print(
            "JSON error:",
            e
        )

        return []


# ============================================================
# FIT TEAM NAME
# ============================================================

def fit_text(
    draw,
    text,
    font,
    max_width
):

    shaped = shape_persian(text)

    bbox = draw.textbbox(
        (0, 0),
        shaped,
        font=font
    )

    current_width = (
        bbox[2] - bbox[0]
    )

    if current_width <= max_width:
        return text

    short = text

    while len(short) > 3:

        short = short[:-1]

        test = shape_persian(
            short + "…"
        )

        bbox = draw.textbbox(
            (0, 0),
            test,
            font=font
        )

        if (
            bbox[2] - bbox[0]
            <= max_width
        ):
            return short + "…"

    return text


# ============================================================
# PASTE LOGO
# ============================================================

def paste_logo(
    canvas,
    logo,
    center_x,
    center_y,
    size=72
):

    if not logo:
        return

    logo = logo.copy()

    logo.thumbnail(
        (size, size),
        Image.Resampling.LANCZOS
    )

    x = int(
        center_x
        - logo.width / 2
    )

    y = int(
        center_y
        - logo.height / 2
    )

    canvas.paste(
        logo,
        (x, y),
        logo
    )


# ============================================================
# CREATE TODAY POSTER
# ============================================================

def create_today_poster(
    grouped_matches,
    date_text
):

    # --------------------------------------------------------
    # IMAGE SIZE
    # --------------------------------------------------------

    width = 1100

    header_height = 155
    league_height = 65
    match_height = 125
    footer_height = 45

    number_of_rows = 0

    for competition, matches in grouped_matches:

        number_of_rows += (
            len(matches)
        )

    number_of_leagues = len(
        grouped_matches
    )

    height = (
        header_height
        + footer_height
        + (
            number_of_leagues
            * league_height
        )
        + (
            number_of_rows
            * match_height
        )
    )

    # --------------------------------------------------------
    # COLORS
    # --------------------------------------------------------

    background = (
        247,
        248,
        250
    )

    white = (
        255,
        255,
        255
    )

    dark = (
        30,
        34,
        40
    )

    gray = (
        105,
        110,
        118
    )

    border = (
        225,
        228,
        233
    )

    league_background = (
        238,
        241,
        245
    )

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    image = Image.new(
        "RGB",
        (width, height),
        background
    )

    draw = ImageDraw.Draw(
        image
    )

    # --------------------------------------------------------
    # FONTS
    # --------------------------------------------------------

    title_font = get_font(
        44,
        bold=True
    )

    date_font = get_font(
        24,
        bold=False
    )

    league_font = get_font(
        27,
        bold=True
    )

    team_font = get_font(
        30,
        bold=True
    )

    time_font = get_font(
        35,
        bold=True
    )

    small_font = get_font(
        18,
        bold=False
    )

    # --------------------------------------------------------
    # MAIN HEADER
    # --------------------------------------------------------

    draw.rounded_rectangle(
        (
            25,
            20,
            width - 25,
            header_height - 15
        ),
        radius=28,
        fill=white,
        outline=border,
        width=2
    )

    draw_rtl_text(
        draw,
        (
            width // 2,
            62
        ),
        "⚽ بازی‌های امروز",
        title_font,
        dark
    )

    draw_rtl_text(
        draw,
        (
            width // 2,
            112
        ),
        f"📅 {date_text} • ساعت ایران",
        date_font,
        gray
    )

    # --------------------------------------------------------
    # START DRAWING LEAGUES
    # --------------------------------------------------------

    y = header_height

    for (
        competition,
        matches
    ) in grouped_matches:

        league_name = COMPETITIONS.get(
            competition,
            competition
        )

        flag = COUNTRY_FLAGS.get(
            competition,
            "⚽"
        )

        # ----------------------------------------------------
        # LEAGUE HEADER
        # ----------------------------------------------------

        draw.rounded_rectangle(
            (
                25,
                y + 8,
                width - 25,
                y + league_height - 7
            ),
            radius=18,
            fill=league_background
        )

        draw_rtl_text(
            draw,
            (
                width // 2,
                y + league_height // 2
            ),
            f"{flag}  {league_name}",
            league_font,
            dark
        )

        y += league_height

        # ----------------------------------------------------
        # MATCHES
        # ----------------------------------------------------

        for match in matches:

            home_team = match.get(
                "homeTeam",
                {}
            )

            away_team = match.get(
                "awayTeam",
                {}
            )

            # ------------------------------------------------
            # TEAM NAMES
            # ------------------------------------------------

            home_original = home_team.get(
                "name",
                "تیم میزبان"
            )

            away_original = away_team.get(
                "name",
                "تیم مهمان"
            )

            home = TEAM_NAMES.get(
                home_original,
                home_original
            )

            away = TEAM_NAMES.get(
                away_original,
                away_original
            )

            # ------------------------------------------------
            # TIME
            # ------------------------------------------------

            time_text = get_time_text(
                match.get("utcDate")
            )

            # ------------------------------------------------
            # LOGOS
            # ------------------------------------------------

            home_logo = download_logo(
                home_team.get("crest")
            )

            away_logo = download_logo(
                away_team.get("crest")
            )

            # ------------------------------------------------
            # MATCH CARD
            # ------------------------------------------------

            draw.rounded_rectangle(
                (
                    25,
                    y + 4,
                    width - 25,
                    y + match_height - 6
                ),
                radius=22,
                fill=white,
                outline=border,
                width=2
            )

            center_y = (
                y
                + match_height // 2
                + 2
            )

            # ------------------------------------------------
            # TIME
            # ------------------------------------------------

            draw_rtl_text(
                draw,
                (
                    width // 2,
                    center_y - 5
                ),
                time_text,
                time_font,
                dark
            )

            draw_rtl_text(
                draw,
                (
                    width // 2,
                    center_y + 35
                ),
                "شروع بازی",
                small_font,
                gray
            )

            # ------------------------------------------------
            # HOME TEAM - RIGHT
            # ------------------------------------------------

            home_display = fit_text(
                draw,
                home,
                team_font,
                280
            )

            draw_rtl_text(
                draw,
                (
                    815,
                    center_y
                ),
                home_display,
                team_font,
                dark
            )

            paste_logo(
                image,
                home_logo,
                970,
                center_y,
                72
            )

            # ------------------------------------------------
            # AWAY TEAM - LEFT
            # ------------------------------------------------

            away_display = fit_text(
                draw,
                away,
                team_font,
                280
            )

            draw_rtl_text(
                draw,
                (
                    285,
                    center_y
                ),
                away_display,
                team_font,
                dark
            )

            paste_logo(
                image,
                away_logo,
                130,
                center_y,
                72
            )

            # ------------------------------------------------
            # CENTER SEPARATOR
            # ------------------------------------------------

            draw.line(
                (
                    520,
                    center_y,
                    580,
                    center_y
                ),
                fill=border,
                width=2
            )

            y += match_height

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    draw_rtl_text(
        draw,
        (
            width // 2,
            height - 20
        ),
        "Football Alert • زمان‌ها به وقت تهران",
        small_font,
        gray
    )

    # --------------------------------------------------------
    # SAVE PNG
    # --------------------------------------------------------

    output = BytesIO()

    image.save(
        output,
        format="PNG",
        optimize=True
    )

    output.seek(0)

    return output


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
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # CHECK ENVIRONMENT
    # --------------------------------------------------------

    if not BOT_TOKEN:

        print(
            "ERROR: BOT_TOKEN is missing"
        )

        return

    if not CHAT_ID:

        print(
            "ERROR: CHAT_ID is missing"
        )

        return

    if not FOOTBALL_API_TOKEN:

        print(
            "ERROR: FOOTBALL_API_TOKEN is missing"
        )

        return

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # GROUP MATCHES BY LEAGUE
    # --------------------------------------------------------

    grouped_matches = []

    for (
        competition,
        league_name
    ) in COMPETITIONS.items():

        print(
            "Checking:",
            league_name
        )

        matches = get_matches(
            competition,
            date
        )

        if matches:

            grouped_matches.append(
                (
                    competition,
                    matches
                )
            )

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    total_matches = sum(
        len(matches)
        for competition, matches
        in grouped_matches
    )

    print(
        "TOTAL MATCHES:",
        total_matches
    )

    # --------------------------------------------------------
    # NO MATCHES
    # --------------------------------------------------------

    if total_matches == 0:

        send_message(
            f"⚽ بازی‌ای برای امروز پیدا نشد.\n"
            f"📅 تاریخ: {date}"
        )

        return

    # --------------------------------------------------------
    # CREATE ONE IMAGE
    # --------------------------------------------------------

    print(
        "Creating one poster..."
    )

    poster = create_today_poster(
        grouped_matches,
        date
    )

    # --------------------------------------------------------
    # SEND ONLY ONE PHOTO
    # --------------------------------------------------------

    success = send_photo(
        poster
    )

    if success:

        print(
            "TODAY POSTER SENT SUCCESSFULLY"
        )

    else:

        print(
            "Poster sending failed."
        )

        # Fallback
        lines = [
            "⚽ بازی‌های امروز",
            f"📅 تاریخ: {date}",
            ""
        ]

        for (
            competition,
            matches
        ) in grouped_matches:

            flag = COUNTRY_FLAGS.get(
                competition,
                "⚽"
            )

            lines.append(
                f"{flag} "
                f"{COMPETITIONS.get(competition, competition)}"
            )

            for match in matches:

                home_team = match.get(
                    "homeTeam",
                    {}
                )

                away_team = match.get(
                    "awayTeam",
                    {}
                )

                home_original = home_team.get(
                    "name",
                    "تیم میزبان"
                )

                away_original = away_team.get(
                    "name",
                    "تیم مهمان"
                )

                home = TEAM_NAMES.get(
                    home_original,
                    home_original
                )

                away = TEAM_NAMES.get(
                    away_original,
                    away_original
                )

                match_time = get_time_text(
                    match.get("utcDate")
                )

                lines.append(
                    f"{home} - {away} | {match_time}"
                )

            lines.append("")

        send_message(
            "\n".join(lines)
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
