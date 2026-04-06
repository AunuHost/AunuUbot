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
    if user_id in ubot._get_my_id or has_build_access(access):
        buttons = [
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        exp = await get_expired_date(user_id)
        prefix = await get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "None"
        status = get_access_label(access)
        if status == "free":
            status = "premium"
        return await callback_query.edit_message_text(
            f"""
<blockquote>AunuHost
  sᴛᴀᴛᴜs : {Fonts.smallcap(status)}
  ᴘʀᴇғɪx : {prefix[0]}
  ᴇxᴘɪʀᴇᴅ_ᴏɴ : {waktu}</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [
            [InlineKeyboardButton("ʙᴇʟɪ ᴜsᴇʀʙᴏᴛ", callback_data="bahan")],
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            """
<blockquote><b>ᴍᴀᴀғ, ᴋᴀᴍᴜ ʙᴇʟᴜᴍ ᴘᴜɴʏᴀ ᴀᴋsᴇs ᴜsᴇʀʙᴏᴛ. sɪʟᴀᴋᴀɴ ʙᴇʟɪ ᴅᴜʟᴜ ᴀᴛᴀᴜ ʜᴜʙᴜɴɢɪ ᴀᴅᴍɪɴ.</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("buat_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    access = await get_access_flags(client, user_id)
    if user_id in ubot._get_my_id:
        buttons = [
            [InlineKeyboardButton("✅ ʀᴇsᴛᴀʀᴛ", callback_data=f"ress_ubot")],
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
            [InlineKeyboardButton("💸 ʙᴇʟɪ ᴜsᴇʀʙᴏᴛ 💸", callback_data="bahan")],
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>❌ ᴍᴀᴀғ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇᴍʙᴇʟɪ ᴜsᴇʀʙᴏᴛ, sɪʟᴀᴋᴀɴ ᴍᴇᴍʙᴇʟɪ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton("✅ ʟᴀɴᴊᴜᴛᴋᴀɴ", callback_data="add_ubot")]]
        return await callback_query.edit_message_text(
            """
<blockquote><b>✅ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ sɪᴀᴘᴋᴀɴ ʙᴀʜᴀɴ ʙᴇʀɪᴋᴜᴛ

    • <code>ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ</code>: ɴᴏᴍᴇʀ ʜᴘ ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ

☑️ ᴊɪᴋᴀ sᴜᴅᴀʜ ᴛᴇʀsᴇᴅɪᴀ sɪʟᴀʜᴋᴀɴ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.CALLBACK("bayar_dulu")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = BTN.PLUS_MINUS(1, user_id)
    return await callback_query.edit_message_text(
        MSG.TEXT_PAYMENT(30, 30, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("add_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    try:
        phone = await bot.ask(
            user_id,
            (
                "<b>sɪʟᴀʜᴋᴀɴ ᴍᴀsᴜᴋᴋᴀɴ ɴᴏᴍᴏʀ ᴛᴇʟᴇᴘᴏɴ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ ᴅᴇɴɢᴀɴ ғᴏʀᴍᴀᴛ ᴋᴏᴅᴇ ɴᴇɢᴀʀᴀ.\nᴄᴏɴᴛᴏʜ: +628xxxxxxx</b>\n"
                "\n<b>ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<blockquote>ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs!\nɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    get_otp = await bot.send_message(user_id, "<blockquote><b>ᴍᴇɴɢɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ...</b></blockquote>")
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except ApiIdInvalid as AID:
        await get_otp.delete()
        return await bot.send_message(user_id, AID)
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await bot.send_message(user_id, PNI)
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await bot.send_message(user_id, PNF)
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await bot.send_message(user_id, PNB)
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await bot.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await bot.send_message(user_id, f"ERROR: {error}")
    try:
        sent_code = {
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ</a> ʀᴇsᴍɪ",
            SentCodeType.SMS: "sᴍs ᴀɴᴅᴀ",
            SentCodeType.CALL: "ᴘᴀɴɢɢɪʟᴀɴ ᴛᴇʟᴇᴘᴏɴ",
            SentCodeType.FLASH_CALL: "ᴘᴀɴɢɢɪʟᴀɴ ᴋɪʟᴀᴛ ᴛᴇʟᴇᴘᴏɴ",
            SentCodeType.FRAGMENT_SMS: "ғʀᴀɢᴍᴇɴ sᴍs",
            SentCodeType.EMAIL_CODE: "ᴇᴍᴀɪʟ ᴀɴᴅᴀ",
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                "<b>sɪʟᴀᴋᴀɴ ᴘᴇʀɪᴋsᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴅᴀʀɪ ᴀᴋᴜɴ ʀᴇsᴍɪ ᴛᴇʟᴇɢʀᴀᴍ. ᴋɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ ᴋᴇ sɪɴɪ sᴇᴛᴇʟᴀʜ ᴍᴇᴍʙᴀᴄᴀ ғᴏʀᴍᴀᴛ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ.</b>\n"
                "\nᴊɪᴋᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴀᴅᴀʟᴀʜ <code>12345</code> ᴛᴏʟᴏɴɢ <b>[ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴘᴀsɪ ]</b> ᴋɪʀɪᴍᴋᴀɴ sᴇᴘᴇʀᴛɪ ɪɴɪ <code>1 2 3 4 5</code>\n"
                f"\n<b>ᴋᴏᴅᴇ ᴅɪᴋɪʀɪᴍ ᴍᴇʟᴀʟᴜɪ {sent_code.get(code.type, 'ᴛᴇʟᴇɢʀᴀᴍ')}</b>"
                "\n\n<b>ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<blockquote>ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs!\nɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
    if await is_cancel(callback_query, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        return await bot.send_message(user_id, PCI)
    except PhoneCodeExpired as PCE:
        return await bot.send_message(user_id, PCE)
    except BadRequest as error:
        return await bot.send_message(user_id, f"ERROR: {error}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "<b>ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇɴɢᴀᴋᴛɪғᴋᴀɴ ᴠᴇʀɪғɪᴋᴀsɪ ᴅᴜᴀ ʟᴀɴɢᴋᴀʜ. sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ ᴘᴀssᴡᴏʀᴅɴʏᴀ.\n\nɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "<blockquote>ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs!\nɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
        if await is_cancel(callback_query, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            return await bot.send_message(user_id, f"ERROR: {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    bot_msg = await bot.send_message(
        user_id,
        "sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs....\n\nsɪʟᴀʜᴋᴀɴ ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ",
        disable_web_page_preview=True,
    )
    await new_client.start()
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        return await bot_msg.edit(
            "<b>ʜᴀʀᴀᴘ ɢᴜɴᴀᴋᴀɴ ɴᴏᴍᴇʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ ᴅɪ ᴀᴋᴜɴ ᴀɴᴅᴀ sᴀᴀᴛ ɪɴɪ ᴅᴀɴ ʙᴜᴋᴀɴ ɴᴏᴍᴇʀ ᴛᴇʟᴇɢʀᴀᴍ ᴅᴀʀɪ ᴀᴋᴜɴ ʟᴀɪɴ</b>"
        )
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
#    await remove_from_vars(client.me.id, "PREM_USERS", user_id)
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"AunuUbot.modules.{mod}"))
    SH = await ubot.get_prefix(new_client.me.id)
    buttons = [
            [InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}")],
        ]
    text_done = f"""
<blockquote><b>ʙᴇʀʜᴀsɪʟ ᴅɪᴀᴋᴛɪғᴋᴀɴ
ɴᴀᴍᴀ : <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a>
ɪᴅ : {new_client.me.id}
ᴘʀᴇғɪx : {' '.join(SH)}
ᴊɪᴋᴀ ʙᴏᴛ ᴛɪᴅᴀᴋ ʀᴇsᴘᴏɴ, ᴋᴇᴛɪᴋ /restart</b></blockquote>
        """
    await bot_msg.edit(text_done, disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons))
    await bash("rm -rf *session*")
    await install_my_peer(new_client)
    try:
        await new_client.join_chat("alltestireyy")
        await new_client.join_chat("allubotrey")
    except UserAlreadyParticipant:
        pass

    return await bot.send_message(
        LOGS_MAKER_UBOT,
        f"""
<b>❏ ᴜsᴇʀʙᴏᴛ ᴅɪᴀᴋᴛɪғᴋᴀɴ</b>
<b> ├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ɪᴅ:</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📁 ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ 📁",
                        callback_data=f"cek_masa_aktif {new_client.me.id}",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
)

async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id, "<blockquote>ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs!\nɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>"
        )
        return True
    return False


@PY.BOT("control")
async def _(client, message):
    buttons = [
            [InlineKeyboardButton("ʀᴇsᴛᴀʀᴛ", callback_data=f"ress_ubot")],
        ]
    await message.reply(
            f"""
<blockquote><b>ᴀɴᴅᴀ ᴀᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ʀᴇsᴛᴀʀᴛ?!\nᴊɪᴋᴀ ɪʏᴀ sɪʟᴀʜᴋᴀɴ ᴘᴇɴᴄᴇᴛ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

@PY.CALLBACK("ress_ubot")
async def _(client, callback_query):
    if callback_query.from_user.id not in ubot._get_my_id:
        return await callback_query.answer(
            f"you don't have acces",
            True,
        )
    for X in ubot._ubot:
        if callback_query.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"AunuUbot.modules.{mod}")
                            )
                        return await callback_query.edit_message_text(
                            f"ʀᴇsᴛᴀʀᴛ ʙᴇʀʜᴀsɪʟ ᴅɪʟᴀᴋᴜᴋᴀɴ!\n\nɴᴀᴍᴀ: {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}"
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(f"{error}")

@PY.BOT("restart")
async def _(client, message):
    msg = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>")
    if message.from_user.id not in ubot._get_my_id:
        return await msg.edit(
            f"you don't have acces",
            True,
        )
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"AunuUbot.modules.{mod}")
                            )
                        return await msg.edit(
                            f"ʀᴇsᴛᴀʀᴛ ʙᴇʀʜᴀsɪʟ ᴅɪʟᴀᴋᴜᴋᴀɴ!\n\nɴᴀᴍᴀ: {UB.me.first_name} {UB.me.last_name or ''} | `{UB.me.id}`"
                        )
                    except Exception as error:
                        return await msg.edit(f"{error}")

@PY.BOT("announce")
@PY.OWNER
async def _(client, message):
    parts = message.text.split(maxsplit=1) if message.text else []
    if len(parts) < 2 or not parts[1].strip():
        return await message.reply("<b>ɢᴜɴᴀᴋᴀɴ: /announce ᴘᴇsᴀɴ</b>")

    text = parts[1].strip()
    users = await get_list_from_vars(client.me.id, "SAVED_USERS")
    if not users:
        return await message.reply("<b>ʙᴇʟᴜᴍ ᴀᴅᴀ ᴜsᴇʀ /start ʏᴀɴɢ ᴛᴇʀsɪᴍᴘᴀɴ.</b>")

    status = await message.reply(
        f"<b>ᴍᴇɴɢɪʀɪᴍ ᴀɴɴᴏᴜɴᴄᴇ ᴋᴇ {len(users)} ᴜsᴇʀ...</b>"
    )
    sent = 0
    failed = 0
    for user_id in users:
        try:
            await client.send_message(user_id, text, disable_web_page_preview=True)
            sent += 1
        except Exception:
            failed += 1

    await status.edit(
        f"<b>ᴀɴɴᴏᴜɴᴄᴇ sᴇʟᴇsᴀɪ.</b>\n"
        f"<b>ʙᴇʀʜᴀsɪʟ:</b> <code>{sent}</code>\n"
        f"<b>ɢᴀɢᴀʟ:</b> <code>{failed}</code>"
    )

@PY.CALLBACK("cek_ubot")
@PY.BOT("getubot")
@PY.ADMIN
async def _(client, callback_query):
    await bot.send_message(
        callback_query.from_user.id,
        await MSG.UBOT(0),
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[0].me.id, 0)),
    )

@PY.CALLBACK("cek_masa_aktif")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"⏳ ᴛɪɴɢɢᴀʟ {xxxx} ʜᴀʀɪ ʟᴀɢɪ", True)
    except:
        return await callback_query.answer("✅ sᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴀᴋᴛɪғ", True)

@PY.CALLBACK("del_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        return await callback_query.answer(
            f"❌ ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴜ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"{get_id}"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"{get_id}"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            await remove_ubot(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            await callback_query.answer(
                f"✅ {get_mention} ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ", True
            )
            await callback_query.edit_message_text(
                await MSG.UBOT(0),
                reply_markup=InlineKeyboardMarkup(
                    BTN.UBOT(ubot._ubot[0].me.id, 0)
                ),
            )
            await bot.send_message(
                X.me.id,
                MSG.EXP_MSG_UBOT(X),
                reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
            )

    
@PY.CALLBACK("^(p_ub|n_ub)")
async def _(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "n_ub":
        if count == len(ubot._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "p_ub":
        if count == 0:
            count = len(ubot._ubot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.UBOT(count),
        reply_markup=InlineKeyboardMarkup(
            BTN.UBOT(ubot._ubot[count].me.id, count)
        ),
    )
