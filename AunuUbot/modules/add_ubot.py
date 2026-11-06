import asyncio
import importlib
from datetime import datetime
from time import monotonic

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions

from AunuUbot import *

START_DEDUP = {}


async def get_access_flags(client, user_id):
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")
    seller_users = await get_list_from_vars(client.me.id, "SELER_USERS")
    premium_users = await get_list_from_vars(client.me.id, "PREM_USERS")
    ultra_premium_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")
    return {
        "owner": user_id == OWNER_ID,
        "admin": user_id in admin_users,
        "seller": user_id in seller_users,
        "premium": user_id in premium_users or user_id in ultra_premium_users,
    }


def get_access_label(flags):
    if flags["owner"]:
        return "owner"
    if flags["admin"]:
        return "admin"
    if flags["seller"]:
        return "seller"
    if flags["premium"]:
        return "premium"
    return "free"


def has_build_access(flags):
    return any(flags.values())


@PY.BOT("start")
@PY.START
@PY.PRIVATE
async def _(client, message):
    key = (message.chat.id, message.from_user.id if message.from_user else message.chat.id)
    now = monotonic()
    if now - START_DEDUP.get(key, 0) < 5:
        return
    START_DEDUP[key] = now
    buttons = BTN.START(message)
    msg = MSG.START(message)
    try:
        await message.reply(
            msg,
            reply_markup=InlineKeyboardMarkup(buttons))
    except Exception:
        return


@PY.CALLBACK("bahan")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    access = await get_access_flags(client, user_id)
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("ʀᴇsᴛᴀʀᴛ", callback_data=f"ress_ubot")],
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>ᴀɴᴅᴀ sᴜᴅᴀʜ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ

ᴊɪᴋᴀ ᴜsᴇʀʙᴏᴛ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴅɪɢᴜɴᴀᴋᴀɴ sɪʟᴀʜᴋᴀɴ ᴛᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ʀᴇsᴛᴀʀᴛ ᴅɪ ᴀᴛᴀs</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>❌ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ!</b>

<b>📚 ᴋᴀʀᴇɴᴀ ᴍᴀᴋsɪᴍᴀʟ ᴜsᴇʀʙᴏᴛ ᴀᴅᴀʟᴀʜ {Fonts.smallcap(str(len(ubot._ubot)))} ᴛᴇʟᴀʜ ᴛᴇʀᴄᴀᴘᴀɪ</b>

<b>☎️ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ: <a href=tg://openmessage?user_id={OWNER_ID}>ᴀᴅᴍɪɴ</a> ᴊɪᴋᴀ ᴍᴀᴜ ᴅɪʙᴜᴀᴛᴋᴀɴ ʙᴏᴛ sᴇᴘᴇʀᴛɪ sᴀʏᴀ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if not has_build_access(access):
        buttons = [
            [InlineKeyboardButton("ʟᴀɴᴊᴜᴛᴋᴀɴ", callback_data="bayar_dulu")],
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton("✅ ʟᴀɴᴊᴜᴛᴋᴀɴ", callback_data="buat_ubot")]]
        return await callback_query.edit_message_text(
            """
<blockquote><b>ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇᴍʙᴇʟɪ ᴜsᴇʀʙᴏᴛ sɪʟᴀʜᴋᴀɴ ᴘᴇɴᴄᴇᴛ ᴛᴏᴍʙᴏʟ ʟᴀɴᴊᴜᴛᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.CALLBACK("status")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    access = await get_access_flags(client, user_id)
    label = get_access_label(access)
    if user_id in ubot._get_my_id or has_build_access(access):
        buttons = [
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        await callback_query.edit_message_text(
            f"""
<blockquote><b>📊 sᴛᴀᴛᴜs ᴀᴋᴜɴ</b>

<b>👤 ᴜsᴇʀ:</b> <a href=tg://user?id={user_id}>{callback_query.from_user.first_name}</a>
<b>🆔 ɪᴅ:</b> <code>{user_id}</code>
<b>🏷 ᴀᴋsᴇs:</b> <code>{label}</code>
<b>🤖 ᴜsᴇʀʙᴏᴛ:</b> <code>{'ᴀᴋᴛɪꜰ' if user_id in ubot._get_my_id else 'ᴛɪᴅᴀᴋ ᴀᴋᴛɪꜰ'}</code></blockquote>

<b>AunuUbot</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        await callback_query.edit_message_text(
            f"""
<blockquote><b>📊 sᴛᴀᴛᴜs ᴀᴋᴜɴ</b>

<b>👤 ᴜsᴇʀ:</b> <a href=tg://user?id={user_id}>{callback_query.from_user.first_name}</a>
<b>🆔 ɪᴅ:</b> <code>{user_id}</code>
<b>🏷 ᴀᴋsᴇs:</b> <code>{label}</code>
<b>🤖 ᴜsᴇʀʙᴏᴛ:</b> <code>ᴛɪᴅᴀᴋ ᴀᴋᴛɪꜰ</code></blockquote>

<b>AunuUbot</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
