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
# CONFIG
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_TOKEN = os.getenv("FOOTBALL_API_TOKEN")

API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

TEHRAN = ZoneInfo("Asia/Tehran")

# Logical design size.
# Final PNG is exported at 2x.
WIDTH = 1600
MARGIN = 70
GAP = 28

# High resolution export multiplier.
EXPORT_SCALE = 2

# Larger source logo cache for sharper output.
LOGO_MAX_SIZE = 420


# ============================================================
# COMPETITIONS
# ============================================================

COMPETITIONS = {
    "PL": "ط¸â€‍ط؛إ’ط¹آ¯ ط·آ¨ط·آ±ط·ع¾ط·آ± ط·آ§ط¸â€ ط¹آ¯ط¸â€‍ط؛إ’ط·آ³",
    "PD": "ط¸â€‍ط·آ§ط¸â€‍ط؛إ’ط¹آ¯ط·آ§",
    "SA": "ط·آ³ط·آ±ط؛إ’ ط·آ¢ ط·آ§ط؛إ’ط·ع¾ط·آ§ط¸â€‍ط؛إ’ط·آ§",
    "BL1": "ط·آ¨ط¸ث†ط¸â€ ط·آ¯ط·آ³ط¸â€‍ط؛إ’ط¹آ¯ط·آ§",
    "FL1": "ط¸â€‍ط؛إ’آ¯ ط؛آ± ط¸ظ¾ط·آ±ط·آ§ط¸â€ ط·آ³ط¸â€،",
    "DED": "ط·آ§ط·آ±ط·ع¾ط؛إ’ط¸ث†ط؛إ’ط·آ³ط¸â€،",
    "PPL": "ط¸â€‍ط؛إ’ط¹آ¯ ط¸آ¾ط·آ±ط·ع¾ط·ط›ط·آ§ط¸â€‍",
    "BSA": "ط·آ³ط·آ±ط؛إ’ ط·آ¢ ط·آ¨ط·آ±ط·آ²ط؛إ’ط¸â€‍",
    "CL": "ط¸â€‍ط؛إ’ط¹آ¯ ط¸â€ڑط¸â€،ط·آ±ط¸â€¦ط·آ§ط¸â€ ط·آ§ط¸â€  ط·آ§ط·آ±ط¸ث†ط¸آ¾ط·آ§",
}


LEAGUE_COLORS = {
    "PL": (132, 82, 246),
    "PD": (236, 70, 91),
    "SA": (42, 132, 238),
    "BL1": (232, 66, 72),
    "FL1": (50, 120, 236),
    "DED": (242, 145, 42),
    "PPL": (38, 170, 118),
    "BSA": (38, 158, 103),
    "CL": (92, 103, 238),
}


LEAGUE_ICONS = {
    "PL": "PL",
    "PD": "LaLiga",
    "SA": "Serie A",
    "BL1": "BL",
    "FL1": "L1",
    "DED": "NL",
    "PPL": "PT",
    "BSA": "BR",
    "CL": "UCL",
}


# ============================================================
# TEAM NAMES
# ============================================================

TEAM_NAMES = {
    "Brentford FC": "ط·آ¨ط·آ±ط¸â€ ط·ع¾ط¸ظ¾ط¸ث†ط·آ±ط·آ¯",
    "Chelsea FC": "ط¹â€ ط¸â€‍ط·آ³ط؛إ’",
    "Arsenal FC": "ط·آ¢ط·آ±ط·آ³ط¸â€ ط·آ§ط¸â€‍",
    "Liverpool FC": "ط¸â€‍ط؛إ’ط¸ث†ط·آ±ط·آ¾ط¸ث†ط¸â€‍",
    "Manchester City FC": "ط¸â€¦ط¸â€ ط¹â€ ط·آ³ط·ع¾ط·آ±ط·آ³ط؛إ’ط·ع¾ط؛إ’",
    "Manchester United FC": "ط¸â€¦ط¸â€ ط¹â€ ط·آ³ط·ع¾ط·آ±ط؛إ’ط¸ث†ط¸â€ ط·آ§ط؛إ’ط·ع¾ط·آ¯",
    "Tottenham Hotspur FC": "ط·ع¾ط·آ§ط·ع¾ط¸â€ ط¸â€،ط·آ§ط¸â€¦",
    "Newcastle United FC": "ط¸â€ ط؛إ’ط¸ث†ط¹آ©ط·آ§ط·آ³ط¸â€‍",
    "Aston Villa FC": "ط·آ§ط·آ³ط·ع¾ط¸ث†ط¸â€  ط¸ث†ط؛إ’ط¸â€‍ط·آ§",
    "Everton FC": "ط·آ§ط¸ث†ط·آ±ط·ع¾ط¸ث†ط¸â€ ",
    "West Ham United FC": "ط¸ث†ط·آ³ط·ع¾ط¸â€،ط¸â€¦",
    "Fulham FC": "ط¸ظ¾ط¸ث†ط¸â€‍ط·آ§ط¸â€¦",
    "Crystal Palace FC": "ط¹آ©ط·آ±ط؛إ’ط·آ³ط·ع¾ط·آ§ط¸â€‍ ط¸آ¾ط·آ§ط¸â€‍ط·آ§ط·آ³",
    "Brighton & Hove Albion FC": "ط·آ¨ط·آ±ط؛إ’ط·ع¾ط¸ث†ط¸â€ ",
    "Wolverhampton Wanderers FC": "ط¸ث†ط¸â€‍ط¸ث†ط¸â€‍ط¸ث†ط·آ±ط¸â€،ط¸â€¦ط¸آ¾ط·ع¾ط¸ث†ط¸â€ ",
    "Nottingham Forest FC": "ط¸â€ ط·آ§ط·ع¾ط؛إ’ط¸â€ ط¹آ¯ط¸â€،ط·آ§ط¸â€¦ ط¸ظ¾ط·آ§ط·آ±ط·آ³ط·ع¾",
    "AFC Bournemouth": "ط·آ¨ط¸ث†ط·آ±ط¸â€ ط¸â€¦ط¸ث†ط·آ«",
    "Burnley FC": "ط·آ¨ط·آ±ط¸â€ ط¸â€‍ط؛إ’",
    "Leeds United FC": "ط¸â€‍ط؛إ’ط·آ¯ط·آ²",
    "Sunderland AFC": "ط·آ³ط·آ§ط¸â€ ط·آ¯ط·آ±ط¸â€‍ط¸â€ ط·آ¯",

    "Real Madrid CF": "ط·آ±ط·آ¦ط·آ§ط¸â€‍ ط¸â€¦ط·آ§ط·آ¯ط·آ±ط؛إ’ط·آ¯",
    "FC Barcelona": "ط·آ¨ط·آ§ط·آ±ط·آ³ط¸â€‍ط¸ث†ط¸â€ ط·آ§",
    "RCD Espanyol de Barcelona": "ط·آ§ط·آ³ط¸آ¾ط·آ§ط¸â€ ط؛إ’ط¸ث†ط¸â€‍",
    "Elche CF": "ط·آ§ط¸â€‍ط¹â€ ط¸â€،",
    "Club Atlط£آ©tico de Madrid": "ط·آ§ط·ع¾ط¸â€‍ط·ع¾ط؛إ’ط¹آ©ط¸ث† ط¸â€¦ط·آ§ط·آ¯ط·آ±ط؛إ’ط·آ¯",
    "Club Atlط·آ£ط¢آ©tico de Madrid": "ط·آ§ط·ع¾ط¸â€‍ط·ع¾ط؛إ’ط¹آ©ط¸ث† ط¸â€¦ط·آ§ط·آ¯ط·آ±ط؛إ’ط·آ¯",
    "Sevilla FC": "ط·آ³ط¸ث†ط؛إ’ط·آ§",
    "Valencia CF": "ط¸ث†ط·آ§ط¸â€‍ط¸â€ ط·آ³ط؛إ’ط·آ§",
    "Villarreal CF": "ط¸ث†ط؛إ’ط·آ§ط·آ±ط·آ¦ط·آ§ط¸â€‍",
    "Athletic Club": "ط·آ§ط·ع¾ط¸â€‍ط·ع¾ط؛إ’ط¹آ© ط·آ¨ط؛إ’ط¸â€‍ط·آ¨ط·آ§ط·آ¦ط¸ث†",
    "Real Betis Balompiط£آ©": "ط·آ±ط·آ¦ط·آ§ط¸â€‍ ط·آ¨ط·ع¾ط؛إ’ط·آ³",
    "Real Betis Balompiط·آ£ط¢آ©": "ط·آ±ط·آ¦ط·آ§ط¸â€‍ ط·آ¨ط·ع¾ط؛إ’ط·آ³",
    "Getafe CF": "ط·آ®ط·ع¾ط·آ§ط¸ظ¾ط¸â€،",
    "Girona FC": "ط¹ع©ط؛إ’ط·آ±ط¸ث†ط¸â€ ط·آ§",
    "RC Celta de Vigo": "ط·آ³ط¸â€‍ط·ع¾ط·آ§ط¸ث†ط؛إ’ط¹آ¯ط¸ث†",
    "CA Osasuna": "ط·آ§ط¸ث†ط·آ³ط·آ§ط·آ³ط¸ث†ط¸â€ ط·آ§",
    "Rayo Vallecano de Madrid": "ط·آ±ط·آ§ط؛إ’ط¸ث† ط¸ث†ط·آ§ط؛إ’ط¹آ©ط·آ§ط¸â€ ط¸ث†",
    "RCD Mallorca": "ط¸â€¦ط·آ§ط؛إ’ط¸ث†ط·آ±ط¹آ©ط·آ§",
    "Deportivo Alavط£آ©s": "ط·آ¢ط¸â€‍ط·آ§ط¸ث†ط·آ³",
    "Deportivo Alavط·آ£ط¢آ©s": "ط·آ¢ط¸â€‍ط·آ§ط¸ث†ط·آ³",
    "Real Sociedad de Fط£ط›tbol": "ط·آ±ط·آ¦ط·آ§ط¸â€‍ ط·آ³ط¸ث†ط·آ³ط؛إ’ط·آ¯ط·آ§ط·آ¯",
    "Real Sociedad de Fط·آ£ط·â€؛tbol": "ط·آ±ط·آ¦ط·آ§ط¸â€‍ ط·آ³ط¸ث†ط·آ³ط؛إ’ط·آ¯ط·آ§ط·آ¯",

    "FC Internazionale Milano": "ط·آ§ط؛إ’ط¸â€ ط·ع¾ط·آ±",
    "Inter Milan": "ط·آ§ط؛إ’ط¸â€ ط·آ±",
    "AC Milan": "ط·آ¢ط·آ´ ط¸â€¦ط؛إ’ط¸â€‍ط·آ§ط¸â€ ",
    "Juventus FC": "ط؛إ’ط¸ث†ط¸ث†ط¸â€ ط·ع¾ط¸ث†ط·آ³",
    "SSC Napoli": "ط¸â€ ط·آ§ط¸آ¾ط¸ث†ط¸â€‍ط؛إ’",
    "AS Roma": "ط·آ±ط¸â€¦",
    "SS Lazio": "ط¸â€‍ط·آ§ط·ع¾ط·آ²ط؛إ’ط¸ث†",
    "Atalanta BC": "ط·آ¢ط·ع¾ط·آ§ط¸â€‍ط·آ§ط¸â€ ط·ع¾ط·آ§",
    "ACF Fiorentina": "ط¸ظ¾ط؛إ’ط¸ث†ط·آ±ط¸â€ ط·ع¾ط؛إ’ط¸â€ ط·آ§",
    "Torino FC": "ط·ع¾ط¸ث†ط·آ±ط؛إ’ط¸â€ ط¸ث†",
    "Bologna FC 1909": "ط·آ¨ط¸ث†ط¸â€‍ط¸ث†ط¸â€ ط؛إ’ط·آ§",
    "Genoa CFC": "ط·آ¬ط¸â€ ط¸ث†ط·آ§",
    "Udinese Calcio": "ط·آ§ط¸ث†ط·آ¯ط؛إ’ط¸â€ ط·آ²ط¸â€،",
    "Parma Calcio 1913": "ط¸آ¾ط·آ§ط·آ±ط¸â€¦ط·آ§",
    "US Lecce": "ط¸â€‍ط¹â€ ط¸â€،",
    "Cagliari Calcio": "ط¹آ©ط·آ§ط¸â€‍ط؛إ’ط·آ§ط·آ±ط؛إ’",
    "Como 1907": "ط¹آ©ط¸ث†ط¸â€¦ط¸ث†",
    "US Sassuolo Calcio": "ط·آ³ط·آ§ط·آ³ط¸ث†ط¸â€‍ط¸ث†",
    "Sassuolo Calcio": "ط·آ³ط·آ§ط·آ³ط¸ث†ط¸â€‍ط¸ث†",

    "FC Bayern Mط£آ¼nchen": "ط·آ¨ط·آ§ط؛إ’ط·آ±ط¸â€  ط¸â€¦ط¸ث†ط¸â€ ط؛إ’ط·آ®",
    "FC Bayern Mط·آ£ط¢آ¼nchen": "ط·آ¨ط·آ§ط؛إ’ط·آ±ط¸â€  ط¸â€¦ط¸ث†ط¸â€ ط؛إ’ط·آ®",
    "Borussia Dortmund": "ط·آ¯ط¸ث†ط·آ±ط·ع¾ط¸â€¦ط¸ث†ط¸â€ ط·آ¯",
    "RB Leipzig": "ط¸â€‍ط·آ§ط؛إ’ط¸آ¾ط·آ²ط؛إ’ط¹آ¯",
    "Bayer 04 Leverkusen": "ط·آ¨ط·آ§ط؛إ’ط·آ±ط¸â€‍ط¸ث†ط·آ±ط¹آ©ط¸ث†ط·آ²ط¸â€ ",
    "Eintracht Frankfurt": "ط·آ¢ط؛إ’ط¸â€ ط·ع¾ط·آ±ط·آ§ط·آ®ط·ع¾ ط¸ظ¾ط·آ±ط·آ§ط¸â€ ط¹آ©ط¸ظ¾ط¸ث†ط·آ±ط·ع¾",
    "VfB Stuttgart": "ط·آ§ط·آ´ط·ع¾ط¸ث†ط·ع¾ط¹آ¯ط·آ§ط·آ±ط·ع¾",
    "VfL Wolfsburg": "ط¸ث†ط¸â€‍ط¸ظ¾ط·آ³ط·آ¨ط¸ث†ط·آ±ط¹آ¯",
    "Borussia Mط£آ¶nchengladbach": "ط¸â€¦ط¸ث†ط¸â€ ط·آ´ط¸â€  ط¹آ¯ط¸â€‍ط·آ§ط·آ¯ط·آ¨ط·آ§ط·آ®",
    "Borussia Mط·آ£ط¢آ¶nchengladbach": "ط¸â€¦ط¸ث†ط¸â€ ط·آ´ط¸â€  ط¹آ¯ط¸â€‍ط·آ§ط·آ¯ط·آ¨ط·آ§ط·آ®",
    "SV Werder Bremen": "ط¸ث†ط·آ±ط·آ¯ط·آ±ط·آ¨ط·آ±ط¸â€¦ط¸â€ ",
    "1. FSV Mainz 05": "ط¸â€¦ط·آ§ط؛إ’ط¸â€ ط·آ²",
    "TSG 1899 Hoffenheim": "ط¸â€،ط¸ث†ط¸ظ¾ط¸â€ ط¸â€،ط·آ§ط؛إ’ط¸â€¦",
    "Sport-Club Freiburg": "ط¸ظ¾ط·آ±ط·آ§ط؛إ’ط·آ¨ط¸ث†ط·آ±ط¹آ¯",
    "FC Augsburg": "ط·آ¢ط¹آ¯ط·آ³ط·آ¨ط¸ث†ط·آ±ط¹آ¯",
    "1. FC Union Berlin": "ط؛إ’ط¸ث†ط¸â€ ط؛إ’ط¸ث†ط¸â€  ط·آ¨ط·آ±ط¸â€‍ط؛إ’ط¸â€ ",
    "1. FC Kط£آ¶ln": "ط¹آ©ط¸â€‍ط¸â€ ",
    "1. FC Kط·آ£ط¢آ¶ln": "ط¹آ©ط¸â€‍ط¸â€ ",
    "Hamburger SV": "ط¸â€،ط·آ§ط¸â€¦ط·آ¨ط¸ث†ط·آ±ط¹آ¯",

    "Paris Saint-Germain FC": "ط¸آ¾ط·آ§ط·آ±ط؛إ’ ط·آ³ط¸â€  ط¹ع©ط·آ±ط¸â€¦ط·آ§ط¸â€ ",
    "Olympique de Marseille": "ط¸â€¦ط·آ§ط·آ±ط·آ³ط؛إ’",
    "AS Monaco FC": "ط¸â€¦ط¸ث†ط¸â€ ط·آ§ط¹آ©ط¸ث†",
    "Olympique Lyonnais": "ط¸â€‍ط؛إ’ط¸ث†ط¸â€ ",
    "Lille OSC": "ط¸â€‍ط؛إ’ط¸â€‍",
    "OGC Nice": "ط¸â€ ط؛إ’ط·آ³",
    "Stade Rennais FC 1901": "ط·آ±ط¸â€ ",
    "FC Nantes": "ط¸â€ ط·آ§ط¸â€ ط·ع¾",
    "Toulouse FC": "ط·ع¾ط¸ث†ط¸â€‍ط¸ث†ط·آ²",
    "RC Lens": "ط¸â€‍ط·آ§ط¸â€ ط·آ³",
    "Racing Club de Lens": "ط¸â€‍ط·آ§ط¸â€ ط·آ³",
    "RC Strasbourg Alsace": "ط·آ§ط·آ³ط·ع¾ط·آ±ط·آ§ط·آ³ط·آ¨ط¸ث†ط·آ±ط¹آ¯",

    "AFC Ajax": "ط·آ¢ط¹ع©ط·آ§ط¹آ©ط·آ³",
    "PSV": "ط·آ¢ط؛إ’ط¸â€ ط·آ¯ط¸â€،ط¸ث†ط¸ث†ط¸â€ ",
    "Feyenoord Rotterdam": "ط¸ظ¾ط·آ§ط؛إ’ط¸â€ ط¸ث†ط·آ±ط·آ¯",
    "AZ": "ط·آ¢ط¸â€‍ط¹آ©ط¸â€¦ط·آ§ط·آ±",
    "FC Twente '65": "ط·ع¾ط¸ث†ط·آ¦ط¸â€ ط·ع¾ط¸â€،",
    "FC Utrecht": "ط·آ§ط¸ث†ط·ع¾ط·آ±ط·آ®ط·ع¾",
    "PEC Zwolle": "ط·آ²ط¸ث†ط¸â€‍ط¸â€،",
    "FC Groningen": "ط·آ®ط·آ±ط¸ث†ط¸â€ ط؛إ’ط¸â€ ط¹آ¯ط¸â€ ",

    "SL Benfica": "ط·آ¨ط¸â€ ط¸ظ¾ط؛إ’ط¹آ©ط·آ§",
    "FC Porto": "ط¸آ¾ط¸ث†ط·آ±ط·ع¾ط¸ث†",
    "Sporting Clube de Portugal": "ط·آ§ط·آ³ط¸آ¾ط¸ث†ط·آ±ط·ع¾ط؛إ’ط¸â€ ط¹آ¯",
    "SC Braga": "ط·آ¨ط·آ±ط·آ§ط¹آ¯ط·آ§",
    "Vitط£آ³ria SC": "ط¸ث†ط؛إ’ط·ع¾ط¸ث†ط·آ±ط؛إ’ط·آ§ ط¹آ¯ط؛إ’ط¸â€¦ط·آ§ط·آ±ط·آ´",
    "Vitط·آ£ط¢آ³ria SC": "ط¸ث†ط؛إ’ط·ع¾ط¸ث†ط·آ±ط؛إ’ط·آ§ ط¹آ¯ط؛إ’ط¸â€¦ط·آ§ط·آ±ط·آ´",

    "CR Flamengo": "ط¸ظ¾ط¸â€‍ط·آ§ط¸â€¦ط؛إ’ط¸â€ ط¹آ¯ط¸ث†",
    "SE Palmeiras": "ط¸آ¾ط·آ§ط¸â€‍ط¸â€ ط؛إ’ط·آ±ط·آ§ط·آ³",
    "Botafogo FR": "ط·آ¨ط¸ث†ط·ع¾ط·آ§ط¸ظ¾ط¸â€،ط¸ث†ط¹آ¯ط¸ث†",
    "Fluminense FC": "ط¸ظ¾ط¸â€‍ط¸ث†ط¸â€¦ط؛إ’ط¸â€ ط¸â€ ط·آ²ط¸â€،",
    "Corinthians": "ط¹آ©ط¸ث†ط·آ±ط؛إ’ط¸â€ ط·ع¾ط؛إ’ط·آ§ط¸â€ ط·آ³",
    "Sط£آ£o Paulo FC": "ط·آ³ط·آ§ط·آ¦ط¸ث†ط¸آ¾ط·آ§ط·آ¦ط¸ث†ط¸â€‍ط¸ث†",
    "Sط·آ£ط¢آ£o Paulo FC": "ط·آ³ط·آ§ط·آ¦ط¸ث†ط¸آ¾ط·آ§ط·آ¦ط¸ث†ط¸â€‍ط¸ث†",
}


# ============================================================
# FONTS
# ============================================================

FONT_PATHS = {
    "bold": [
        "/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf",
        "/usr/share/fonts/opentype/noto/NotoKufiArabic-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "regular": [
        "/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoKufiArabic-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "english": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
}


def get_font(size, bold=False, english=False):
    custom = os.getenv("FONT_PATH")

    if custom and os.path.exists(custom):
        return ImageFont.truetype(custom, size)

    key = "english" if english else ("bold" if bold else "regular")

    for path in FONT_PATHS[key]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


# ============================================================
# TEXT / RTL HELPERS
# ============================================================

def repair_text(text):
    """
    The original project contains strings that were accidentally
    decoded as CP1256 before being saved. This repairs them when
    possible while leaving normal Unicode text untouched.
    """

    if text is None:
        return ""

    text = str(text)

    # Fast path: already normal Persian / Unicode.
    if not any(ch in text for ch in ("ط¸", "ط·", "ط؛", "إ’", "ط£", "آ©")):
        return text

    try:
        repaired = text.encode("cp1256").decode("utf-8")

        if repaired != text and "ï؟½" not in repaired:
            return repaired

    except Exception:
        pass

    return text


def english_digits(text):
    """
    IMPORTANT:
    Numbers in the graphic must ALWAYS remain English.
    """
    return str(text)


def rtl_args(font, fill, anchor="ra", align="right"):
    return {
        "font": font,
        "fill": fill,
        "anchor": anchor,
        "align": align,
        "direction": "rtl",
        "language": "fa",
    }


def draw_rtl(draw, xy, text, font, fill, anchor="ra"):
    draw.text(
        xy,
        repair_text(text),
        **rtl_args(font, fill, anchor),
    )


def bbox(draw, text, font, rtl=True):
    text = repair_text(text)

    if rtl:
        return draw.textbbox(
            (0, 0),
            text,
            font=font,
            direction="rtl",
            language="fa",
        )

    return draw.textbbox(
        (0, 0),
        str(text),
        font=font,
    )


def centered(draw, cx, y, text, font, fill, rtl=True):
    text = repair_text(text)

    b = bbox(draw, text, font, rtl)
    w = b[2] - b[0]

    if rtl:
        draw.text(
            (cx + w / 2, y),
            text,
            **rtl_args(font, fill, "ra", "center"),
        )
    else:
        draw.text(
            (cx - w / 2, y),
            text,
            font=font,
            fill=fill,
            anchor="la",
        )


def fit_font(draw, text, max_width, max_size, min_size=18, bold=True):
    text = repair_text(text)

    for size in range(max_size, min_size - 1, -2):
        font = get_font(size, bold=bold)

        b = bbox(draw, text, font)
        width = b[2] - b[0]

        if width <= max_width:
            return font

    return get_font(min_size, bold=bold)


# ============================================================
# DATE / TIME
# ============================================================

def get_today():
    return datetime.now(TEHRAN).strftime("%Y-%m-%d")


def format_date(value):
    try:
        d = datetime.strptime(value, "%Y-%m-%d")

        # English digits intentionally.
        return f"{d.year}/{d.month:02d}/{d.day:02d}"

    except Exception:
        return english_digits(value)


def match_time(value):
    try:
        return (
            datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
            .astimezone(TEHRAN)
            .strftime("%H:%M")
        )

    except Exception:
        return "--:--"


# ============================================================
# LOGOS
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
            timeout=15,
            headers={
                "User-Agent": "FootballDailyBot/1.0"
            },
        )

        response.raise_for_status()

        image = Image.open(
            io.BytesIO(response.content)
        ).convert("RGBA")

        image.thumbnail(
            (LOGO_MAX_SIZE, LOGO_MAX_SIZE),
            Image.Resampling.LANCZOS,
        )

        LOGO_CACHE[url] = image

        return image

    except Exception as exc:
        print("Logo download failed:", exc)
        LOGO_CACHE[url] = None
        return None


# ============================================================
# FOOTBALL API
# ============================================================

def get_matches(code, date_string):
    headers = {
        "X-Auth-Token": FOOTBALL_API_TOKEN
    }

    params = {
        "dateFrom": date_string,
        "dateTo": date_string,
    }

    for attempt in range(3):
        try:
            response = requests.get(
                API_URL.format(code),
                headers=headers,
                params=params,
                timeout=30,
            )

            if response.status_code == 429:
                print("Rate limited. Waiting 45 seconds...")
                time.sleep(45)
                continue

            response.raise_for_status()

            return response.json().get("matches", [])

        except Exception as exc:
            print(f"Error {code}: {exc}")

            if attempt < 2:
                time.sleep(5)

    return []


# ============================================================
# TEAM NAME LOOKUP
# ============================================================

def get_team_display_name(api_name):
    if not api_name:
        return ""

    api_name = repair_text(api_name)

    # Direct lookup first.
    if api_name in TEAM_NAMES:
        return repair_text(TEAM_NAMES[api_name])

    # More robust lookup for names containing mojibake.
    for original, translated in TEAM_NAMES.items():
        repaired_original = repair_text(original)

        if repaired_original == api_name:
            return repair_text(translated)

    return api_name


# ============================================================
# BACKGROUND
# ============================================================

def background(width, height):
    image = Image.new(
        "RGBA",
        (width, height),
        (7, 10, 24, 255),
    )

    pixels = image.load()

    # Smooth dark gradient.
    for y in range(height):
        t = y / max(1, height - 1)

        base = (
            7 + int(5 * t),
            10 + int(5 * t),
            24 + int(12 * t),
        )

        for x in range(width):
            dx = (x - width * 0.5) / width
            dy = (y - height * 0.18) / height

            glow = max(
                0,
                1 - math.sqrt(dx * dx + dy * dy) * 3,
            )

            pixels[x, y] = (
                min(255, int(base[0] + glow * 8)),
                min(255, int(base[1] + glow * 8)),
                min(255, int(base[2] + glow * 18)),
                255,
            )

    overlay = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(overlay)

    # Ambient purple / blue lights.
    draw.ellipse(
        (-350, -250, 500, 650),
        fill=(91, 70, 245, 26),
    )

    draw.ellipse(
        (width - 550, 0, width + 300, 800),
        fill=(35, 110, 240, 22),
    )

    # Subtle diagonal sports texture.
    for x in range(-height, width + height, 260):
        draw.line(
            (x, height, x + height, 0),
            fill=(255, 255, 255, 6),
            width=2,
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(18)
    )

    image.alpha_composite(overlay)

    return image


# ============================================================
# SHADOW
# ============================================================

def shadow(image, box, radius=30):
    shadow_layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(shadow_layer)

    x1, y1, x2, y2 = box

    draw.rounded_rectangle(
        (
            x1,
            y1 + 12,
            x2,
            y2 + 12,
        ),
        radius=radius,
        fill=(0, 0, 0, 135),
    )

    shadow_layer = shadow_layer.filter(
        ImageFilter.GaussianBlur(24)
    )

    image.alpha_composite(shadow_layer)


# ============================================================
# LOGO PLATE
# ============================================================

def draw_logo(
    image,
    logo,
    cx,
    cy,
    size=150,
    accent=(120, 100, 240),
):
    plate_size = size + 42

    plate = Image.new(
        "RGBA",
        (plate_size, plate_size),
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(plate)

    # Soft bottom shadow.
    draw.ellipse(
        (
            7,
            11,
            plate_size - 3,
            plate_size + 2,
        ),
        fill=(0, 0, 0, 90),
    )

    # Outer plate.
    draw.ellipse(
        (
            0,
            0,
            plate_size - 9,
            plate_size - 9,
        ),
        fill=(247, 249, 253, 255),
        outline=accent,
        width=4,
    )

    # Inner ring.
    draw.ellipse(
        (
            10,
            10,
            plate_size - 19,
            plate_size - 19,
        ),
        outline=(220, 224, 235, 255),
        width=2,
    )

    if logo:
        logo_copy = logo.copy()

        logo_copy.thumbnail(
            (size - 5, size - 5),
            Image.Resampling.LANCZOS,
        )

        plate.alpha_composite(
            logo_copy,
            (
                (plate_size - logo_copy.width) // 2,
                (plate_size - logo_copy.height) // 2,
            ),
        )

    else:
        draw.ellipse(
            (
                38,
                38,
                plate_size - 47,
                plate_size - 47,
            ),
            outline=(185, 190, 205, 255),
            width=4,
        )

    image.alpha_composite(
        plate,
        (
            int(cx - plate_size / 2),
            int(cy - plate_size / 2),
        ),
    )


# ============================================================
# LEAGUE BADGE
# ============================================================

def league_badge(draw, x, y, code, accent):
    radius = 27

    # Outer glow.
    draw.ellipse(
        (
            x - radius - 4,
            y - radius - 4,
            x + radius + 4,
            y + radius + 4,
        ),
        fill=(*accent, 35),
    )

    draw.ellipse(
        (
            x - radius,
            y - radius,
            x + radius,
            y + radius,
        ),
        fill=accent,
    )

    label = LEAGUE_ICONS.get(code, code)

    font = get_font(
        14,
        bold=True,
        english=True,
    )

    b = draw.textbbox(
        (0, 0),
        label,
        font=font,
    )

    label_width = b[2] - b[0]
    label_height = b[3] - b[1]

    draw.text(
        (
            x - label_width / 2,
            y - label_height / 2 - 2,
        ),
        label,
        font=font,
        fill="white",
    )


# ============================================================
# MATCH CARD
# ============================================================

def draw_match_card(
    image,
    match,
    x,
    y,
    width,
    height,
    number,
):
    draw = ImageDraw.Draw(image)

    accent = LEAGUE_COLORS.get(
        match["competition_code"],
        (100, 110, 235),
    )

    # Card shadow.
    shadow(
        image,
        (x, y, x + width, y + height),
        30,
    )

    # Main card.
    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + height,
        ),
        radius=30,
        fill=(17, 22, 41, 255),
        outline=(255, 255, 255, 18),
        width=1,
    )

    # Top league strip.
    draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + 8,
        ),
        radius=5,
        fill=accent,
    )

    # Inner accent border.
    draw.rounded_rectangle(
        (
            x + 3,
            y + 3,
            x + width - 3,
            y + height - 3,
        ),
        radius=27,
        outline=(*accent, 38),
        width=2,
    )

    # League badge.
    league_badge(
        draw,
        x + 49,
        y + 48,
        match["competition_code"],
        accent,
    )

    # League title.
    league_font = fit_font(
        draw,
        match["league_name"],
        width - 170,
        29,
        18,
        True,
    )

    draw_rtl(
        draw,
        (x + width - 30, y + 30),
        match["league_name"],
        league_font,
        (242, 244, 249),
        "ra",
    )

    # Divider.
    draw.line(
        (
            x + 30,
            y + 92,
            x + width - 30,
            y + 92,
        ),
        fill=(255, 255, 255, 35),
        width=2,
    )

    # Match number pill.
    number_font = get_font(
        18,
        bold=True,
    )

    number_text = english_digits(number)

    number_box = bbox(
        draw,
        number_text,
        number_font,
    )

    number_width = (
        number_box[2] - number_box[0]
    )

    pill_width = max(
        54,
        number_width + 26,
    )

    draw.rounded_rectangle(
        (
            x + 24,
            y + 112,
            x + 24 + pill_width,
            y + 150,
        ),
        radius=18,
        fill=(255, 255, 255, 12),
        outline=(255, 255, 255, 22),
        width=1,
    )

    draw.text(
        (
            x + 24 + pill_width / 2,
            y + 131,
        ),
        number_text,
        font=number_font,
        fill=(220, 224, 235),
        anchor="mm",
    )

    # Team positions.
    home_x = x + width * 0.27
    away_x = x + width * 0.73

    logo_y = y + 185

    draw_logo(
        image,
        match["home_logo"],
        home_x,
        logo_y,
        138,
        accent,
    )

    draw_logo(
        image,
        match["away_logo"],
        away_x,
        logo_y,
        138,
        accent,
    )

    # VS.
    vs_font = get_font(
        18,
        bold=True,
        english=True,
    )

    draw.text(
        (
            x + width / 2,
            y + 165,
        ),
        "VS",
        font=vs_font,
        fill=(113, 123, 151),
        anchor="mm",
    )

    # Time pill.
    pill_w = 170
    pill_h = 68

    tx = x + width / 2 - pill_w / 2
    ty = y + 220

    # Time shadow.
    draw.rounded_rectangle(
        (
            tx + 2,
            ty + 5,
            tx + pill_w + 2,
            ty + pill_h + 5,
        ),
        radius=20,
        fill=(0, 0, 0, 65),
    )

    # Time background.
    draw.rounded_rectangle(
        (
            tx,
            ty,
            tx + pill_w,
            ty + pill_h,
        ),
        radius=20,
        fill=accent,
    )

    time_font = get_font(
        34,
        bold=True,
    )

    # English digits.
    time_text = english_digits(
        match["time"]
    )

    draw.text(
        (
            x + width / 2,
            ty + pill_h / 2 - 2,
        ),
        time_text,
        font=time_font,
        fill=(255, 255, 255),
        anchor="mm",
    )

    # Team names.
    home_font = fit_font(
        draw,
        match["home"],
        width * 0.36,
        31,
        18,
        True,
    )

    away_font = fit_font(
        draw,
        match["away"],
        width * 0.36,
        31,
        18,
        True,
    )

    centered(
        draw,
        home_x,
        y + 301,
        match["home"],
        home_font,
        (249, 250, 253),
    )

    centered(
        draw,
        away_x,
        y + 301,
        match["away"],
        away_font,
        (249, 250, 253),
    )

    # Home / Away labels.
    small_font = get_font(
        16,
        bold=False,
    )

    centered(
        draw,
        home_x,
        y + 350,
        "ط¸â€¦ط؛إ’ط·آ²ط·آ¨ط·آ§ط¸â€ ",
        small_font,
        (113, 122, 149),
    )

    centered(
        draw,
        away_x,
        y + 350,
        "ط¸â€¦ط¸â€،ط¸â€¦ط·آ§ط¸â€ ",
        small_font,
        (113, 122, 149),
    )


# ============================================================
# POSTER
# ============================================================

def create_poster(matches):
    columns = 2

    card_width = int(
        (WIDTH - MARGIN * 2 - GAP) / 2
    )

    card_height = 395

    rows = math.ceil(
        len(matches) / columns
    )

    header = 385
    footer = 105

    height = (
        header
        + rows * card_height
        + max(0, rows - 1) * GAP
        + footer
        + 60
    )

    image = background(
        WIDTH,
        height,
    )

    draw = ImageDraw.Draw(image)

    # ========================================================
    # HEADER
    # ========================================================

    # Main top accent.
    draw.rectangle(
        (0, 0, WIDTH, 8),
        fill=(132, 82, 246),
    )

    draw.rectangle(
        (0, 8, WIDTH, 11),
        fill=(65, 125, 240, 120),
    )

    # Brand.
    english_font = get_font(
        24,
        bold=True,
        english=True,
    )

    draw.text(
        (MARGIN, 50),
        "FOOTBALL DAILY",
        font=english_font,
        fill=(151, 139, 255),
    )

    draw.text(
        (MARGIN, 86),
        "MATCH CENTER",
        font=get_font(
            14,
            bold=True,
            english=True,
        ),
        fill=(93, 101, 130),
    )

    # Main Persian title.
    title = "ط·آ¨ط·آ§ط·آ²ط؛إ’أ¢â‚¬إ’ط¸â€،ط·آ§ط؛إ’ ط·آ§ط¸â€¦ط·آ±ط¸ث†ط·آ²"

    title_font = get_font(
        72,
        bold=True,
    )

    draw_rtl(
        draw,
        (WIDTH - MARGIN, 92),
        title,
        title_font,
        (250, 251, 255),
        "ra",
    )

    # Subtitle.
    subtitle = (
        "ط·آ¨ط·آ±ط¸â€ ط·آ§ط¸â€¦ط¸â€، ط¸â€¦ط·آ³ط·آ§ط·آ¨ط¸â€ڑط·آ§ط·ع¾ "
        "ط¸ظ¾ط¸ث†ط·ع¾ط·آ¨ط·آ§ط¸â€‍ ط·آ§ط¸â€¦ط·آ±ط¸ث†آ²"
    )

    draw_rtl(
        draw,
        (WIDTH - MARGIN, 181),
        subtitle,
        get_font(25),
        (145, 153, 180),
        "ra",
    )

    # ========================================================
    # DATE GLASS PANEL
    # ========================================================

    date_text = (
        "ط·ع¾ط·آ§ط·آ±ط؛إ’ط·آ® "
        + format_date(get_today())
    )

    date_font = get_font(
        24,
        bold=True,
    )

    date_box = bbox(
        draw,
        date_text,
        date_font,
    )

    date_width = (
        date_box[2] - date_box[0]
    )

    panel_width = max(
        300,
        date_width + 60,
    )

    draw.rounded_rectangle(
        (
            MARGIN,
            145,
            MARGIN + panel_width,
            211,
        ),
        radius=20,
        fill=(255, 255, 255, 14),
        outline=(255, 255, 255, 30),
        width=2,
    )

    draw_rtl(
        draw,
        (
            MARGIN + panel_width - 28,
            160,
        ),
        date_text,
        date_font,
        (236, 239, 247),
        "ra",
    )

    # Header divider.
    draw.line(
        (
            MARGIN,
            285,
            WIDTH - MARGIN,
            285,
        ),
        fill=(255, 255, 255, 35),
        width=2,
    )

    # ========================================================
    # MATCH COUNT
    # ========================================================

    count_text = (
        english_digits(len(matches))
        + " ط¸â€¦ط·آ³ط·آ§ط·آ¨ط¸â€ڑط¸â€، ط·آ§ط¸â€¦ط·آ±ط¸ث†ط·آ²"
    )

    draw_rtl(
        draw,
        (WIDTH - MARGIN, 326),
        count_text,
        get_font(
            23,
            bold=True,
        ),
        (143, 151, 178),
        "ra",
    )

    # Small sports icon.
    draw.ellipse(
        (
            MARGIN,
            316,
            MARGIN + 20,
            336,
        ),
        fill=(132, 82, 246),
    )

    draw.arc(
        (
            MARGIN + 4,
            320,
            MARGIN + 16,
            332,
        ),
        0,
        270,
        fill=(255, 255, 255),
        width=2,
    )

    # ========================================================
    # MATCH CARDS
    # ========================================================

    start_y = header

    for index, match in enumerate(matches):
        row = index // 2
        column = index % 2

        x = (
            MARGIN
            + column * (card_width + GAP)
        )

        y = (
            start_y
            + row * (card_height + GAP)
        )

        draw_match_card(
            image,
            match,
            x,
            y,
            card_width,
            card_height,
            index + 1,
        )

    # ========================================================
    # FOOTER
    # ========================================================

    footer_y = (
        start_y
        + rows * card_height
        + max(0, rows - 1) * GAP
        + 30
    )

    draw.line(
        (
            MARGIN,
            footer_y,
            WIDTH - MARGIN,
            footer_y,
        ),
        fill=(255, 255, 255, 30),
        width=2,
    )

    draw_rtl(
        draw,
        (
            WIDTH - MARGIN,
            footer_y + 29,
        ),
        "ط·ع¾ط¸â€¦ط·آ§ط¸â€¦ط؛إ’ ط·آ³ط·آ§ط·آ¹ط·ع¾أ¢â‚¬إ’ط¸â€،ط·آ§ ط·آ¨ط¸â€، ط¸ث†ط¸â€ڑط·ع¾ ط·ع¾ط¸â€،ط·آ±ط·آ§ط¸â€ ",
        get_font(20),
        (112, 121, 148),
        "ra",
    )

    draw.ellipse(
        (
            MARGIN,
            footer_y + 30,
            MARGIN + 16,
            footer_y + 46,
        ),
        fill=(132, 82, 246),
    )

    # ========================================================
    # HIGH-RES EXPORT
    # ========================================================

    final_width = WIDTH * EXPORT_SCALE
    final_height = height * EXPORT_SCALE

    high_res = image.resize(
        (final_width, final_height),
        Image.Resampling.LANCZOS,
    )

    output = io.BytesIO()

    # PNG = no JPEG compression.
    high_res.save(
        output,
        format="PNG",
        optimize=True,
        compress_level=6,
    )

    output.seek(0)

    return output


# ============================================================
# TELEGRAM
# ============================================================

def send_photo(photo, caption):
    """
    Send the generated PNG as a Telegram Photo instead of a
    Document so Telegram displays it as a normal image.

    The original PNG is kept as PNG and is not converted to JPEG
    or resized by this code before uploading.
    """

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendPhoto"
    )

    # Keep the original high-resolution PNG in memory.
    photo.seek(0)

    files = {
        "photo": (
            "football_daily.png",
            photo,
            "image/png",
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
        timeout=90,
    )

    response.raise_for_status()

    print(
        "Telegram PNG photo sent successfully."
    )


def send_message(text):
    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
        },
        timeout=30,
    )

    response.raise_for_status()


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("FOOTBALL DAILY BOT")
    print("=" * 60)

    # --------------------------------------------------------
    # Environment validation
    # --------------------------------------------------------

    required = [
        ("BOT_TOKEN", BOT_TOKEN),
        ("CHAT_ID", CHAT_ID),
        ("FOOTBALL_API_TOKEN", FOOTBALL_API_TOKEN),
    ]

    for name, value in required:
        if not value:
            raise ValueError(
                f"{name} is missing"
            )

    # --------------------------------------------------------
    # Date
    # --------------------------------------------------------

    today = get_today()

    print(
        "Today in Tehran:",
        today,
    )

    all_matches = []

    # --------------------------------------------------------
    # Fetch competitions
    # --------------------------------------------------------

    for code, league_name in COMPETITIONS.items():
        print(
            "Checking",
            code,
        )

        matches = get_matches(
            code,
            today,
        )

        print(
            code,
            len(matches),
            "matches",
        )

        for match in matches:

            status = match.get(
                "status"
            )

            if status in (
                "CANCELLED",
                "POSTPONED",
            ):
                continue

            utc_date = match.get(
                "utcDate"
            )

            if not utc_date:
                continue

            home_raw = (
                match
                .get("homeTeam", {})
                .get("name", "")
            )

            away_raw = (
                match
                .get("awayTeam", {})
                .get("name", "")
            )

            home_name = get_team_display_name(
                home_raw
            )

            away_name = get_team_display_name(
                away_raw
            )

            home_logo = download_logo(
                match
                .get("homeTeam", {})
                .get("crest")
            )

            away_logo = download_logo(
                match
                .get("awayTeam", {})
                .get("crest")
            )

            all_matches.append(
                {
                    "competition_code": code,
                    "league_name": league_name,
                    "home": home_name,
                    "away": away_name,
                    "home_logo": home_logo,
                    "away_logo": away_logo,
                    "time": match_time(
                        utc_date
                    ),
                    "utc": utc_date,
                }
            )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    all_matches.sort(
        key=lambda item: item["utc"]
    )

    print(
        "TOTAL MATCHES:",
        len(all_matches),
    )

    # --------------------------------------------------------
    # No matches
    # --------------------------------------------------------

    if not all_matches:
        message = (
            "âڑ½ ط¨ط§ط²غŒâ€Œظ‡ط§غŒ ط§ظ…ط±ظˆط²\n\n"
            "ًں“… طھط§ط±غŒط®: "
            + format_date(today)
            + "\n\n"
            "ط¯ط± ظ„غŒع¯â€Œظ‡ط§غŒ ظ…ظ†طھط®ط¨ ط§ظ…ط±ظˆط² ظ…ط³ط§ط¨ظ‚ظ‡â€Œط§غŒ "
            "ظ¾غŒط¯ط§ ظ†ط´ط¯."
        )

        send_message(message)

        print(
            "No matches found."
        )

        return

    # --------------------------------------------------------
    # Create PNG
    # --------------------------------------------------------

    poster = create_poster(
        all_matches
    )

    # --------------------------------------------------------
    # Caption
    # --------------------------------------------------------

    caption = (
        "âڑ½ ط¨ط§ط²غŒâ€Œظ‡ط§غŒ ط§ظ…ط±ظˆط²\n"
        "ًں“… "
        + format_date(today)
        + "\n"
        "ًںژ¯ "
        + english_digits(
            len(all_matches)
        )
        + " ظ…ط³ط§ط¨ظ‚ظ‡\n"
        "ًں•گ طھظ…ط§ظ…غŒ ط³ط§ط¹طھâ€Œظ‡ط§ ط¨ظ‡ ظˆظ‚طھ طھظ‡ط±ط§ظ†"
    )

    # --------------------------------------------------------
    # Send PNG as normal Telegram photo
    # --------------------------------------------------------

    send_photo(
        poster,
        caption,
    )

    print("DONE")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
