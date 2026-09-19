# -*- coding: utf-8 -*-

import os
import json
import time
import requests


# ============================================================
# SETTINGS
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

API_URL = (
    f"https://api.telegram.org/bot{BOT_TOKEN}"
)

STATE_FILE = "futsal_ads.json"


# ============================================================
# AD TYPES
# ============================================================

AD_TYPES = {
    "empty_slot": "⚽ سانس خالی دارم",
    "transfer": "🔄 واگذاری سانس",
    "looking_player": "👥 دنبال یار هستم",
    "looking_team": "🏃 دنبال تیم هستم",
}


# ============================================================
# LOAD / SAVE ADS
# ============================================================

def load_ads():

    if not os.path.exists(STATE_FILE):
        return []

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_ads(ads):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            ads,
            file,
            ensure_ascii=False,
            indent=2
        )


# ============================================================
# TELEGRAM API
# ============================================================

def telegram(method, data=None):

    try:

        response = requests.post(
            f"{API_URL}/{method}",
            data=data or {},
            timeout=20
        )

        if response.status_code != 200:

            print(
                "Telegram error:",
                response.text
            )

            return None

        result = response.json()

        if not result.get("ok"):

            print(
                "Telegram API error:",
                result
            )

            return None

        return result.get("result")

    except Exception as e:

        print(
            "Telegram connection error:",
            e
        )

        return None


# ============================================================
# KEYBOARD
# ============================================================

def main_menu():

    return {
        "inline_keyboard": [

            [
                {
                    "text": "⚽ سانس خالی دارم",
                    "callback_data": "ad_empty_slot"
                }
            ],

            [
                {
                    "text": "🔄 واگذاری سانس",
                    "callback_data": "ad_transfer"
                }
            ],

            [
                {
                    "text": "👥 دنبال یار هستم",
                    "callback_data": "ad_looking_player"
                }
            ],

            [
                {
                    "text": "🏃 دنبال تیم هستم",
                    "callback_data": "ad_looking_team"
                }
            ]

        ]
    }


def cancel_keyboard():

    return {
        "inline_keyboard": [
            [
                {
                    "text": "❌ لغو",
                    "callback_data": "cancel_ad"
                }
            ]
        ]
    }


def found_keyboard(ad_id):

    return {
        "inline_keyboard": [
            [
                {
                    "text": "✅ پیدا شد / آگهی بسته شود",
                    "callback_data": f"close_{ad_id}"
                }
            ]
        ]
    }


# ============================================================
# SEND MESSAGE
# ============================================================

def send_message(
    chat_id,
    text,
    reply_markup=None
):

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:

        data["reply_markup"] = json.dumps(
            reply_markup,
            ensure_ascii=False
        )

    return telegram(
        "sendMessage",
        data
    )


# ============================================================
# EDIT MESSAGE
# ============================================================

def edit_message(
    chat_id,
    message_id,
    text,
    reply_markup=None
):

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:

        data["reply_markup"] = json.dumps(
            reply_markup,
            ensure_ascii=False
        )

    return telegram(
        "editMessageText",
        data
    )


# ============================================================
# ANSWER CALLBACK
# ============================================================

def answer_callback(callback_id):

    telegram(
        "answerCallbackQuery",
        {
            "callback_query_id": callback_id
        }
    )


# ============================================================
# USER NAME
# ============================================================

def get_user_name(user):

    first_name = user.get(
        "first_name",
        ""
    )

    last_name = user.get(
        "last_name",
        ""
    )

    full_name = (
        f"{first_name} {last_name}"
    ).strip()

    if not full_name:

        full_name = "کاربر"

    return full_name


# ============================================================
# FORMAT AD
# ============================================================

def build_ad_message(ad):

    ad_type = AD_TYPES.get(
        ad.get("type"),
        "⚽ آگهی فوتسال"
    )

    lines = []

    lines.append(
        f"<b>{ad_type}</b>"
    )

    lines.append("")

    if ad.get("date"):

        lines.append(
            f"📅 تاریخ: "
            f"<b>{ad['date']}</b>"
        )

    if ad.get("time"):

        lines.append(
            f"⏰ ساعت: "
            f"<b>{ad['time']}</b>"
        )

    if ad.get("hall"):

        lines.append(
            f"📍 سالن: "
            f"<b>{ad['hall']}</b>"
        )

    if ad.get("people"):

        lines.append(
            f"👥 تعداد: "
            f"<b>{ad['people']}</b>"
        )

    if ad.get("total_cost"):

        lines.append(
            f"💰 هزینه کل سالن: "
            f"<b>{ad['total_cost']} تومان</b>"
        )

    if ad.get("team_cost"):

        lines.append(
            f"👥 هزینه هر تیم: "
            f"<b>{ad['team_cost']} تومان</b>"
        )

    if ad.get("person_cost"):

        lines.append(
            f"👤 هزینه هر نفر: "
            f"<b>{ad['person_cost']} تومان</b>"
        )

    if ad.get("phone"):

        lines.append(
            f"📞 تماس: "
            f"<b>{ad['phone']}</b>"
        )

    lines.append("")

    lines.append(
        f"👤 ثبت‌کننده: "
        f"<b>{ad.get('user_name', 'کاربر')}</b>"
    )

    lines.append("")

    lines.append(
        "━━━━━━━━━━━━━━━━"
    )

    return "\n".join(lines)


# ============================================================
# ASK NEXT QUESTION
# ============================================================

def ask_next_question(chat_id, user_id):

    sessions = load_sessions()

    session = sessions.get(
        str(user_id)
    )

    if not session:
        return

    step = session.get(
        "step"
    )

    questions = {

        "date":
            "📅 تاریخ سانس را وارد کن:\n\nمثلاً: جمعه ۲۸ شهریور",

        "time":
            "⏰ ساعت سانس را وارد کن:\n\nمثلاً: 22:00",

        "hall":
            "📍 اسم سالن را وارد کن:\n\nمثلاً: سالن آزادی",

        "people":
            "👥 تعداد نفر یا جای خالی را وارد کن:\n\nمثلاً: 2 نفر",

        "total_cost":
            "💰 هزینه کل سالن چقدر است؟\n\nاگر نمی‌خواهی وارد کنی، بنویس: ندارد",

        "team_cost":
            "👥 هزینه هر تیم چقدر است؟\n\nاگر نمی‌خواهی وارد کنی، بنویس: ندارد",

        "person_cost":
            "👤 هزینه هر نفر چقدر است؟\n\nاگر نمی‌خواهی وارد کنی، بنویس: ندارد",

        "phone":
            "📞 شماره تماس خودت را وارد کن:\n\nمثلاً: 09xxxxxxxxx"

    }

    question = questions.get(
        step
    )

    if question:

        send_message(
            chat_id,
            question,
            cancel_keyboard()
        )


# ============================================================
# SESSION STORAGE
# ============================================================

SESSION_FILE = "futsal_sessions.json"


def load_sessions():

    if not os.path.exists(
        SESSION_FILE
    ):

        return {}

    try:

        with open(
            SESSION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


def save_sessions(sessions):

    with open(
        SESSION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sessions,
            file,
            ensure_ascii=False,
            indent=2
        )


# ============================================================
# START AD
# ============================================================

def start_ad(
    chat_id,
    user_id,
    ad_type
):

    sessions = load_sessions()

    sessions[str(user_id)] = {

        "type": ad_type,

        "step": "date",

        "date": "",
        "time": "",
        "hall": "",
        "people": "",

        "total_cost": "",
        "team_cost": "",
        "person_cost": "",

        "phone": ""

    }

    save_sessions(
        sessions
    )

    send_message(
        chat_id,
        "📝 <b>ثبت آگهی فوتسال</b>\n\n"
        "اطلاعات را یکی‌یکی وارد کن.\n"
        "در هر مرحله فقط جواب همان سؤال را بفرست."
    )

    ask_next_question(
        chat_id,
        user_id
    )


# ============================================================
# NEXT STEP
# ============================================================

STEPS = [

    "date",
    "time",
    "hall",
    "people",
    "total_cost",
    "team_cost",
    "person_cost",
    "phone"

]


def process_text(
    chat_id,
    user_id,
    text
):

    sessions = load_sessions()

    key = str(user_id)

    session = sessions.get(
        key
    )

    if not session:

        return False

    step = session.get(
        "step"
    )

    if step not in STEPS:

        return False

    if text.strip() == "/cancel":

        sessions.pop(
            key,
            None
        )

        save_sessions(
            sessions
        )

        send_message(
            chat_id,
            "❌ ثبت آگهی لغو شد."
        )

        return True

    if text.strip() == "ندارد":

        session[step] = ""

    else:

        session[step] = text.strip()

    current_index = STEPS.index(
        step
    )

    if current_index + 1 < len(STEPS):

        next_step = STEPS[
            current_index + 1
        ]

        session["step"] = next_step

        save_sessions(
            sessions
        )

        ask_next_question(
            chat_id,
            user_id
        )

        return True

    # ========================================================
    # COMPLETE
    # ========================================================

    ads = load_ads()

    ad_id = int(
        time.time()
    )

    session["id"] = ad_id

    session["user_id"] = user_id

    session["user_name"] = "کاربر"

    session["active"] = True

    ads.append(
        session.copy()
    )

    save_ads(
        ads
    )

    sessions.pop(
        key,
        None
    )

    save_sessions(
        sessions
    )

    message = build_ad_message(
        session
    )

    send_message(
        chat_id,
        "✅ <b>آگهی ثبت شد.</b>\n\n"
        + message,
        found_keyboard(ad_id)
    )

    return True


# ============================================================
# CLOSE AD
# ============================================================

def close_ad(
    chat_id,
    message_id,
    user_id,
    ad_id
):

    ads = load_ads()

    found = None

    for ad in ads:

        if int(
            ad.get("id", 0)
        ) == int(ad_id):

            found = ad

            break

    if not found:

        answer_callback(
            ""
        )

        return

    if int(
        found.get("user_id", 0)
    ) != int(user_id):

        return

    found["active"] = False

    save_ads(
        ads
    )

    old_text = build_ad_message(
        found
    )

    new_text = (
        "✅ <b>این آگهی بسته شد.</b>\n\n"
        + old_text
    )

    edit_message(
        chat_id,
        message_id,
        new_text
    )


# ============================================================
# HANDLE UPDATE
# ============================================================

def handle_update(update):

    # --------------------------------------------------------
    # CALLBACK
    # --------------------------------------------------------

    if update.get(
        "callback_query"
    ):

        callback = update[
            "callback_query"
        ]

        callback_id = callback.get(
            "id"
        )

        data = callback.get(
            "data",
            ""
        )

        message = callback.get(
            "message",
            {}
        )

        chat = message.get(
            "chat",
            {}
        )

        chat_id = chat.get(
            "id"
        )

        message_id = message.get(
            "message_id"
        )

        user = callback.get(
            "from",
            {}
        )

        user_id = user.get(
            "id"
        )

        answer_callback(
            callback_id
        )

        # ----------------------------------------------------
        # MAIN MENU
        # ----------------------------------------------------

        if data == "market":

            send_message(
                chat_id,
                "⚽ <b>بازار فوتسال</b>\n\n"
                "نوع آگهی را انتخاب کن:",
                main_menu()
            )

            return

        # ----------------------------------------------------
        # START AD
        # ----------------------------------------------------

        if data == "ad_empty_slot":

            start_ad(
                chat_id,
                user_id,
                "empty_slot"
            )

            return

        if data == "ad_transfer":

            start_ad(
                chat_id,
                user_id,
                "transfer"
            )

            return

        if data == "ad_looking_player":

            start_ad(
                chat_id,
                user_id,
                "looking_player"
            )

            return

        if data == "ad_looking_team":

            start_ad(
                chat_id,
                user_id,
                "looking_team"
            )

            return

        # ----------------------------------------------------
        # CANCEL
        # ----------------------------------------------------

        if data == "cancel_ad":

            sessions = load_sessions()

            sessions.pop(
                str(user_id),
                None
            )

            save_sessions(
                sessions
            )

            send_message(
                chat_id,
                "❌ ثبت آگهی لغو شد."
            )

            return

        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

        if data.startswith(
            "close_"
        ):

            try:

                ad_id = int(
                    data.split(
                        "_",
                        1
                    )[1]
                )

                close_ad(
                    chat_id,
                    message_id,
                    user_id,
                    ad_id
                )

            except Exception as e:

                print(
                    "Close error:",
                    e
                )

            return


    # --------------------------------------------------------
    # TEXT MESSAGE
    # --------------------------------------------------------

    if update.get(
        "message"
    ):

        message = update[
            "message"
        ]

        chat_id = message.get(
            "chat",
            {}
        ).get(
            "id"
        )

        user = message.get(
            "from",
            {}
        )

        user_id = user.get(
            "id"
        )

        text = message.get(
            "text",
            ""
        )

        if not text:

            return

        # ----------------------------------------------------
        # MARKET COMMAND
        # ----------------------------------------------------

        if text in [
            "/market",
            "بازار فوتسال",
            "⚽ بازار فوتسال"
        ]:

            send_message(
                chat_id,
                "⚽ <b>بازار فوتسال</b>\n\n"
                "چه کاری می‌خواهی انجام بدهی؟",
                main_menu()
            )

            return

        # ----------------------------------------------------
        # CURRENT FORM
        # ----------------------------------------------------

        process_text(
            chat_id,
            user_id,
            text
        )


# ============================================================
# GET UPDATES
# ============================================================

def get_updates(
    offset=None
):

    data = {
        "timeout": 5
    }

    if offset is not None:

        data["offset"] = offset

    return telegram(
        "getUpdates",
        data
    ) or []


# ============================================================
# RUN ONCE
# ============================================================

def run_once():

    updates = get_updates()

    if not updates:

        return

    for update in updates:

        try:

            handle_update(
                update
            )

        except Exception as e:

            print(
                "Update error:",
                e
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "⚽ Futsal Market started..."
    )

    run_once()

    print(
        "✅ Futsal Market finished."
    )
