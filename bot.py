import os
import time
import requests

from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# ENV
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")


# ============================================================
# API
# ============================================================

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


FLAGS = {
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
# TEAM NAMES
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

    # Germany
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
    "RC Strasbourg Alsace": "استراسبورگ",

    # Netherlands
    "AFC Ajax": "آژاکس",
    "PSV": "آیندهوون",
    "Feyenoord Rotterdam": "فاینورد",
    "AZ": "آلکمار",
    "FC Twente '65": "توئنته",
    "FC Utrecht": "اوترخت",

    # Portugal
    "SL Benfica": "بنفیکا",
    "FC Porto": "پورتو",
    "Sporting Clube de Portugal": "اسپورتینگ",
    "SC Braga": "براگا",
    "Vitória SC": "ویتوریا گیمارش",

    # Brazil
    "CR Flamengo": "فلامینگو",
    "SE Palmeiras": "پالمیراس",
    "Botafogo FR": "بوتافوگو",
    "Fluminense FC": "فلومیننزه",
    "Corinthians": "کورینتیانس",
    "São Paulo FC": "سائوپائولو",
}


# ============================================================
# LOGO CACHE
# ============================================================

logo_cache = {}


# ============================================================
# FONT
# ============================================================

def get_font(size, bold=False):

    paths = []

    custom = os.getenv("FONT_PATH")

    if custom:
        paths.append(custom)

    if bold:
        paths.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
        ])
    else:
        paths.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
        ])

    for path in paths:

        if os.path.exists(path):

            try:
                return ImageFont.truetype(path, size)

            except Exception:
                pass

    return ImageFont.load_default()


# ============================================================
# TELEGRAM MESSAGE
# ============================================================

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=30
        )

        print("Telegram message:", response.status_code)
        print(response.text)

        return response.ok

    except Exception as e:

        print("Telegram message error:", e)
        return False


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
            (90, 90),
            Image.Resampling.LANCZOS
        )

        logo_cache[url] = image

        return image

    except Exception as e:

        print("Logo error:", e)
        return None


# ============================================================
# PERSIAN TEXT
# ============================================================

def draw_text_center(draw, xy, text, font, fill):

    try:

        draw.text(
            xy,
            text,
            font=font,
            fill=fill,
            anchor="mm",
            direction="rtl",
            language="fa"
        )

    except Exception:

        draw.text(
            xy,
            text,
            font=font,
            fill=fill,
            anchor="mm"
        )


# ============================================================
# GET MATCH TIME
# ============================================================

def get_match_time(match):

    utc_date = match.get("utcDate")

    if not utc_date:
        return "--:--"

    try:

        dt = datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )

        tehran = ZoneInfo("Asia/Tehran")

        iran_time = dt.astimezone(tehran)

        return iran_time.strftime("%H:%M")

    except Exception as e:

        print("Time error:", e)

        return "--:--"


# ============================================================
# CREATE ALL MATCHES IMAGE
# ============================================================

def create_matches_image(matches):

    # --------------------------------------------------------
    # IMAGE SETTINGS
    # --------------------------------------------------------

    width = 1200

    header_height = 190

    league_height = 75

    match_height = 145

    bottom_padding = 45

    # هر بازی ارتفاع مخصوص خودش را دارد
    total_height = (
        header_height
        + bottom_padding
    )

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

        total_height += league_height
        total_height += (
            len(grouped[code])
            * match_height
        )

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    image = Image.new(
        "RGB",
        (
            width,
            total_height
        ),
        (245, 247, 250)
    )

    draw = ImageDraw.Draw(image)

    # --------------------------------------------------------
    # FONTS
    # --------------------------------------------------------

    title_font = get_font(
        52,
        bold=True
    )

    date_font = get_font(
        28
    )

    league_font = get_font(
        30,
        bold=True
    )

    team_font = get_font(
        30,
        bold=True
    )

    time_font = get_font(
        36,
        bold=True
    )

    vs_font = get_font(
        20
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    draw.rectangle(
        (
            0,
            0,
            width,
            header_height
        ),
        fill=(255, 255, 255)
    )

    draw_text_center(
        draw,
        (
            width // 2,
            65
        ),
        "⚽ بازی‌های امروز",
        title_font,
        (25, 30, 40)
    )

    today = get_today()

    draw_text_center(
        draw,
        (
            width // 2,
            125
        ),
        f"📅 {today}  •  به وقت تهران",
        date_font,
        (100, 105, 115)
    )

    # --------------------------------------------------------
    # MATCHES
    # --------------------------------------------------------

    y = header_height

    for league_code, league_matches in grouped.items():

        league_name = COMPETITIONS.get(
            league_code,
            "مسابقات"
        )

        flag = FLAGS.get(
            league_code,
            "⚽"
        )

        # ----------------------------------------------------
        # LEAGUE HEADER
        # ----------------------------------------------------

        draw.rounded_rectangle(
            (
                45,
                y + 10,
                width - 45,
                y + league_height - 5
            ),
            radius=20,
            fill=(235, 238, 243)
        )

        draw_text_center(
            draw,
            (
                width // 2,
                y + 40
            ),
            f"{flag}  {league_name}",
            league_font,
            (40, 45, 55)
        )

        y += league_height

        # ----------------------------------------------------
        # EACH MATCH
        # ----------------------------------------------------

        for match in league_matches:

            # کارت بازی
            card_top = y + 8
            card_bottom = y + match_height - 8

            draw.rounded_rectangle(
                (
                    45,
                    card_top,
                    width - 45,
                    card_bottom
                ),
                radius=24,
                fill=(255, 255, 255),
                outline=(225, 228, 233),
                width=2
            )

            # ------------------------------------------------
            # TEAMS
            # ------------------------------------------------

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
                "میزبان"
            )

            away_original = away_team.get(
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
                home_team.get("crest")
            )

            away_logo = download_logo(
                away_team.get("crest")
            )

            center_y = y + 72

            # ------------------------------------------------
            # HOME SIDE
            # ------------------------------------------------

            home_logo_x = 940
            home_text_x = 800

            if home_logo:

                logo = home_logo.copy()

                logo.thumbnail(
                    (82, 82),
                    Image.Resampling.LANCZOS
                )

                image.paste(
                    logo,
                    (
                        home_logo_x
                        - logo.width // 2,
                        center_y
                        - logo.height // 2
                    ),
                    logo
                )

            draw_text_center(
                draw,
                (
                    home_text_x,
                    center_y
                ),
                home,
                team_font,
                (25, 30, 40)
            )

            # ------------------------------------------------
            # AWAY SIDE
            # ------------------------------------------------

            away_logo_x = 260
            away_text_x = 400

            if away_logo:

                logo = away_logo.copy()

                logo.thumbnail(
                    (82, 82),
                    Image.Resampling.LANCZOS
                )

                image.paste(
                    logo,
                    (
                        away_logo_x
                        - logo.width // 2,
                        center_y
                        - logo.height // 2
                    ),
                    logo
                )

            draw_text_center(
                draw,
                (
                    away_text_x,
                    center_y
                ),
                away,
                team_font,
                (25, 30, 40)
            )

            # ------------------------------------------------
            # TIME BOX
            # ------------------------------------------------

            match_time = get_match_time(
                match
            )

            draw.rounded_rectangle(
                (
                    535,
                    center_y - 34,
                    665,
                    center_y + 34
                ),
                radius=18,
                fill=(245, 247, 250)
            )

            draw_text_center(
                draw,
                (
                    600,
                    center_y
                ),
                match_time,
                time_font,
                (20, 25, 35)
            )

            # VS
            draw_text_center(
                draw,
                (
                    600,
                    center_y + 45
                ),
                "VS",
                vs_font,
                (140, 145, 155)
            )

            y += match_height

    # --------------------------------------------------------
    # SAVE
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
# SEND ONE IMAGE
# ============================================================

def send_matches_image(matches):

    try:

        image_file = create_matches_image(
            matches
        )

        url = (
            f"https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendPhoto"
        )

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": (
                    "⚽ بازی‌های امروز\n"
                    "📊 ۹ لیگ منتخب\n"
                    "🕐 زمان‌ها به وقت تهران"
                )
            },
            files={
                "photo": (
                    "today_matches.png",
                    image_file,
                    "image/png"
                )
            },
            timeout=60
        )

        print(
            "Telegram image:",
            response.status_code
        )

        print(
            response.text
        )

        return response.ok

    except Exception as e:

        print(
            "Image send error:",
            e
        )

        return False


# ============================================================
# TODAY
# ============================================================

def get_today():

    return datetime.now(
        ZoneInfo("Asia/Tehran")
    ).strftime("%Y-%m-%d")


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

    try:

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

        if response.status_code == 429:

            print(
                "Rate limit. Waiting 45 seconds..."
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
                "API retry:",
                response.status_code
            )

        if response.status_code != 200:

            print(
                response.text[:500]
            )

            return []

        data = response.json()

        return data.get(
            "matches",
            []
        )

    except Exception as e:

        print(
            "API error:",
            competition,
            e
        )

        return []


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "================================"
    )

    print(
        "FOOTBALL ALERT BOT"
    )

    date = get_today()

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
            f"⚽ بازی‌ای برای امروز پیدا نشد.\n"
            f"📅 {date}"
        )

        return

    # --------------------------------------------------------
    # SEND ONE IMAGE
    # --------------------------------------------------------

    success = send_matches_image(
        all_matches
    )

    if success:

        print(
            "================================"
        )

        print(
            "TODAY MATCHES IMAGE SENT"
        )

        print(
            "================================"
        )

    else:

        print(
            "Image sending failed."
        )

        # پیام پشتیبان
        send_message(
            f"⚽ بازی‌های امروز\n"
            f"📅 {date}\n"
            f"تعداد بازی‌ها: {len(all_matches)}"
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
