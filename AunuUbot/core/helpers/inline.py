from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardButton
from pyrogram.errors import MessageNotModified
from pyrogram.types import *
from pyromod.helpers import ikb
from AunuUbot import *


def detect_url_links(text):
    link_pattern = (
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    )
    link_found = re.findall(link_pattern, text)
    return link_found


def detect_button_and_text(text):
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = (
        re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    )
    return button_matches, text_matches


def _format_url(url_str):
    if not url_str.startswith(("http://", "https://", "tg://")):
        return f"https://{url_str}"
    return url_str


def create_inline_keyboard(text, user_id=False, is_back=False):
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    prev_button_data = None
    for button_text, button_data in button_matches:
        raw_data = button_data.split("#")[0].strip()
        is_url = bool(detect_url_links(raw_data))
        if user_id and not is_url:
            try:
                uid_part = str(user_id).split("_")
                cb_data = f"_gtnote {int(uid_part[0])}_{uid_part[1]} {raw_data}"
            except Exception:
                cb_data = raw_data
        else:
            cb_data = raw_data

        button_obj = (
            InlineKeyboardButton(button_text, url=_format_url(cb_data))
            if is_url
            else InlineKeyboardButton(button_text, callback_data=cb_data)
        )

        if "#" in button_data and prev_button_data:
            keyboard[-1].append(button_obj)
        else:
            keyboard.append([button_obj])

        prev_button_data = button_data

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if user_id and is_back:
        try:
            uid_part = str(user_id).split("_")
            markup.inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        "ᴋᴇᴍʙᴀʟɪ",
                        callback_data=f"_gtnote {int(uid_part[0])}_{uid_part[1]}",
                    )
                ]
            )
        except Exception:
            pass

    return markup, text_matches


class BTN:
    def ALIVE(get_id):
        button = [
            [
                InlineKeyboardButton(
                    text="ᴛᴜᴛᴜᴘ",
                    callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="ʜᴇʟᴘ",
                    callback_data="help_back",
                )
            ]
        ]
        return button

    def BOT_HELP(message):
        button = [
            [InlineKeyboardButton("ʀᴇsᴛᴀʀᴛ", callback_data="reboot")],
            [InlineKeyboardButton("ꜱʏꜱᴛᴇᴍ", callback_data="system")],
            [InlineKeyboardButton("ᴜʙᴏᴛ", callback_data="ubot")],
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", callback_data="update")],
        ]
        return button
        
    def ADD_EXP(user_id):
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in range(1, 13):
            keyboard.append(
                InlineKeyboardButton(
                    f"{X} ʙᴜʟᴀɴ ",
                    callback_data=f"success {user_id} {X}",
                )
            )
        buttons.add(*keyboard)
        buttons.row(
            InlineKeyboardButton(
                "👤 ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏfɪʟ 👤", callback_data=f"profil {user_id}"
            )
        )
        buttons.row(
            InlineKeyboardButton(
                "❌ ᴛᴏʟᴀᴋ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ❌", callback_data=f"failed {user_id}"
            )
        )
        return buttons

    def EXP_UBOT():
        button = [
            [InlineKeyboardButton("🛍 ʙᴇʟɪ ᴜsᴇʀʙᴏᴛ", callback_data="bahan")],
        ]
        return button

    def START(message):
        if not message.from_user.id == OWNER_ID:
            button = [
                [InlineKeyboardButton("🌟 ʙᴇʟɪ ᴘʀᴇᴍɪᴜᴍ 🌟", callback_data="bahan")],
                [
                    InlineKeyboardButton("🤖 ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ 🤖", callback_data="buat_ubot"),
                    InlineKeyboardButton("🎉 ʜᴇʟᴘ ᴍᴇɴᴜ 🎉", callback_data="help_back")
                ],
                [
                    InlineKeyboardButton("💬 ʟɪᴠᴇ ᴄʜᴀᴛ 💬", callback_data="support")
                ]
            ]
        else:
            button = [
                [InlineKeyboardButton("🤖 ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ 🤖", callback_data="bahan")],
                [
                    InlineKeyboardButton("🛠️ ɢɪᴛᴘᴜʟʟ", callback_data="cb_gitpull"),
                    InlineKeyboardButton("ʀᴇsᴛᴀʀᴛ 🔁", callback_data="cb_restart")
                ],
                [
                    InlineKeyboardButton("🤖 ʟɪsᴛ ᴜsᴇʀʙᴏᴛ 🤖", callback_data="cek_ubot")
                ]
            ]
        return button

    def PLUS_MINUS(query, user_id):
        button = [
            [InlineKeyboardButton("✅ ᴋᴏɴꜰɪʀᴍᴀsɪ", callback_data="confirm")],
            [InlineKeyboardButton("🔙 ʙᴀᴛᴀʟᴋᴀɴ", callback_data=f"home {user_id}")],
        ]
        return button

    def UBOT(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "📁 ʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ 📁",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "⏳ ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪꜰ ⏳",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton("⬅️", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("➡️", callback_data=f"n_ub {int(count)}"),
            ],
        ]
        return button

    def DEAK(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "🔙 ᴋᴇᴍʙᴀʟɪ",
                    callback_data=f"p_ub {int(count)}"
                ),
                InlineKeyboardButton(
                    "sᴇᴛᴜᴊᴜɪ ✅", callback_data=f"deak_akun {int(count)}",
                ),
            ],
        ]
        return button


def get_text(message):
    if message.reply_to_message:
        if len(message.command) < 2:
            text = message.reply_to_message.text or message.reply_to_message.caption
        else:
            text = (
                (message.reply_to_message.text or message.reply_to_message.caption)
                + "\n\n"
                + message.text.split(None, 1)[1]
            )
    else:
        if len(message.command) < 2:
            text = ""
        else:
            text = message.text.split(None, 1)[1]
    return text
