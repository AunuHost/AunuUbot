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
            [InlineKeyboardButton("Ê€á´‡êœ±á´›á´€Ê€á´›", callback_data=f"ress_ubot")],
            [InlineKeyboardButton("á´‹á´‡á´Ê™á´€ÊŸÉª", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>á´€É´á´…á´€ êœ±á´œá´…á´€Êœ á´á´‡á´Ê™á´œá´€á´› á´œêœ±á´‡Ê€Ê™á´á´›\n\ná´ŠÉªá´‹á´€ á´œêœ±á´‡Ê€Ê™á´á´› á´€É´á´…á´€ á´›Éªá´…á´€á´‹ Ê™Éªêœ±á´€ á´…ÉªÉ¢á´œÉ´á´€á´‹á´€É´ êœ±ÉªÊŸá´€Êœá´‹á´€É´ á´›á´‡á´‹á´‡É´ á´›á´á´Ê™á´ÊŸ Ê€á´‡êœ±á´›á´€Ê€á´› á´…Éª á´€á´›á´€êœ±</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("á´‹á´‡á´Ê™á´€ÊŸÉª", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b><b>âŒ á´›Éªá´…á´€á´‹ Ê™Éªsá´€ á´á´‡á´Ê™á´œá´€á´› á´œsá´‡Ê€Ê™á´á´›!</b>

<b>ðŸ“š á´‹á´€Ê€á´‡É´á´€ á´á´€á´‹sÉªá´á´€ÊŸ á´œsá´‡Ê€Ê™á´á´› á´€á´…á´€ÊŸá´€Êœ {Fonts.smallcap(str(len(ubot._ubot)))} á´›á´‡ÊŸá´€Êœ á´›á´‡Ê€á´„á´€á´˜á´€Éª</b>

<b>â˜Žï¸ sÉªÊŸá´€Êœá´‹á´€É´ Êœá´œÊ™á´œÉ´É¢Éª: <a href=tg://openmessage?user_id={OWNER_ID}>á´€á´…á´ÉªÉ´</a>á´ŠÉªá´‹á´€ á´á´€á´œ á´…ÉªÊ™á´œá´€á´›á´‹á´€É´ Ê™á´á´› sá´‡á´˜á´‡Ê€á´›Éª sá´€Êá´€ </b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if not has_build_access(access):
        buttons = [
            [InlineKeyboardButton("ÊŸá´€É´á´Šá´œá´›á´‹á´€É´", callback_data="bayar_dulu")],
            [InlineKeyboardButton("á´‹á´‡á´Ê™á´€ÊŸÉª", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton("âœ… ÊŸá´€É´á´Šá´œá´›á´‹á´€É´", callback_data="buat_ubot")]]
        return await callback_query.edit_message_text(
            """
<blockquote><b>á´€É´á´…á´€ á´›á´‡ÊŸá´€Êœ á´á´‡á´Ê™á´‡ÊŸÉª á´œêœ±á´‡Ê€Ê™á´á´› êœ±ÉªÊŸá´€Êœá´‹á´€É´ á´˜á´‡É´á´„á´‡á´› á´›á´á´Ê™á´ÊŸ ÊŸá´€É´á´Šá´œá´›á´‹á´€É´ á´œÉ´á´›á´œá´‹ á´á´‡á´Ê™á´œá´€á´› á´œêœ±á´‡Ê€Ê™á´á´›</b></blockquote>
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
            [InlineKeyboardButton("back", callback_data=f"home {user_id}")],
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
  status : {status}
  prefix : {prefix[0]}
  expired_on : {waktu}</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [
            [InlineKeyboardButton("buy userbot", callback_data="bahan")],
            [InlineKeyboardButton("back", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            """
<blockquote><b>Sorry, kamu belum punya akses userbot. Silakan beli dulu atau hubungi admin.</b></blockquote>
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
            [InlineKeyboardButton("âœ… Ê€á´‡êœ±á´›á´€Ê€á´›", callback_data=f"ress_ubot")],
            [InlineKeyboardButton("á´‹á´‡á´Ê™á´€ÊŸÉª", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>á´€É´á´…á´€ êœ±á´œá´…á´€Êœ á´á´‡á´Ê™á´œá´€á´› á´œêœ±á´‡Ê€Ê™á´á´›\n\ná´ŠÉªá´‹á´€ á´œêœ±á´‡Ê€Ê™á´á´› á´€É´á´…á´€ á´›Éªá´…á´€á´‹ Ê™Éªêœ±á´€ á´…ÉªÉ¢á´œÉ´á´€á´‹á´€É´ êœ±ÉªÊŸá´€Êœá´‹á´€É´ á´›á´‡á´‹á´‡É´ á´›á´á´Ê™á´ÊŸ Ê€á´‡êœ±á´›á´€Ê€á´› á´…Éª á´€á´›á´€êœ±</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("á´‹á´‡á´Ê™á´€ÊŸÉª", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b><b>âŒ á´›Éªá´…á´€á´‹ Ê™Éªsá´€ á´á´‡á´Ê™á´œá´€á´› á´œsá´‡Ê€Ê™á´á´›!</b>

<b>ðŸ“š á´‹á´€Ê€á´‡É´á´€ á´á´€á´‹sÉªá´á´€ÊŸ á´œsá´‡Ê€Ê™á´á´› á´€á´…á´€ÊŸá´€Êœ {Fonts.smallcap(str(len(ubot._ubot)))} á´›á´‡ÊŸá´€Êœ á´›á´‡Ê€á´„á´€á´˜á´€Éª</b>

<b>â˜Žï¸ sÉªÊŸá´€Êœá´‹á´€É´ Êœá´œÊ™á´œÉ´É¢Éª: <a href=tg://openmessage?user_id={OWNER_ID}>á´€á´…á´ÉªÉ´</a>á´ŠÉªá´‹á´€ á´á´€á´œ á´…ÉªÊ™á´œá´€á´›á´‹á´€É´ Ê™á´á´› sá´‡á´˜á´‡Ê€á´›Éª sá´€Êá´€ </b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if not has_build_access(access):
        buttons = [
            [InlineKeyboardButton("ðŸ’¸ Ê™á´‡ÊŸÉª á´œêœ±á´‡Ê€Ê™á´á´› ðŸ’¸", callback_data="bahan")],
            [InlineKeyboardButton("á´‹á´‡á´Ê™á´€ÊŸÉª", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>âŒ á´á´€á´€êœ° á´€É´á´…á´€ Ê™á´‡ÊŸá´œá´ á´á´‡á´Ê™á´‡ÊŸÉª á´œêœ±á´‡Ê€Ê™á´á´›, êœ±ÉªÊŸá´€á´‹á´€É´ á´á´‡á´Ê™á´‡ÊŸÉª á´›á´‡Ê€ÊŸá´‡Ê™ÉªÊœ á´…á´€Êœá´œÊŸá´œ</b></blockquote>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = [[InlineKeyboardButton("âœ… ÊŸá´€É´á´Šá´œá´›á´‹á´€É´", callback_data="add_ubot")]]
        return await callback_query.edit_message_text(
            """
<blockquote><b>âœ… á´œÉ´á´›á´œá´‹ á´á´‡á´Ê™á´œá´€á´› á´œsá´‡Ê€sÊ™á´á´› sÉªá´€á´˜á´‹á´€É´ Ê™á´€Êœá´€É´ Ê™á´‡Ê€Éªá´‹á´œá´›

    ï¿½ <code>á´˜Êœá´É´á´‡_É´á´œá´Ê™á´‡Ê€</code>: É´á´á´á´‡Ê€ Êœá´˜ á´€á´‹á´œÉ´ á´›á´‡ÊŸá´‡É¢Ê€á´€á´

â˜‘ï¸ á´ŠÉªá´‹á´€ sá´œá´…á´€Êœ á´›á´‡Ê€sá´‡á´…Éªá´€ sÉªÊŸá´€Êœá´‹á´€É´ á´‹ÊŸÉªá´‹ á´›á´á´Ê™á´Éª á´…ÉªÊ™á´€á´¡á´€Êœ</b></blockquote>
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
                "<b>sÉªÊŸá´€Êœá´‹á´€É´ á´á´€sá´œá´‹á´‹á´€É´ É´á´á´á´Ê€ á´›á´‡ÊŸá´‡á´˜á´É´ á´›á´‡ÊŸá´‡É¢Ê€á´€á´ á´€É´á´…á´€ á´…á´‡É´É¢á´€É´ êœ°á´Ê€á´á´€á´› á´‹á´á´…á´‡ É´á´‡É¢á´€Ê€á´€.\ná´„á´É´á´›á´Êœ: +628xxxxxxx</b>\n"
                "\n<b>É¢á´œÉ´á´€á´‹á´€É´ /cancel á´œÉ´á´›á´œá´‹ á´á´‡á´Ê™á´€á´›á´€ÊŸá´‹á´€É´ á´˜Ê€á´sá´‡s á´á´‡á´Ê™á´œá´€á´› á´œsá´‡Ê€Ê™á´á´›</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<blockquote>á´˜á´‡á´Ê™á´€á´›á´€ÊŸá´€É´ á´á´›á´á´á´€á´›Éªêœ±!\nÉ´É¢á´œÉ´á´€á´‹á´€É´ /êœ±á´›á´€Ê€á´› á´œÉ´á´›á´œá´‹ á´á´‡á´á´œÊŸá´€Éª á´œÊŸá´€É´É¢</blockquote>")
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    get_otp = await bot.send_message(user_id, "<blockquote><b>á´á´‡É´É¢ÉªÊ€Éªá´ á´‹á´á´…á´‡ á´á´›á´˜...</b></blockquote>")
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
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>á´€á´‹á´œÉ´ á´›á´‡ÊŸá´‡É¢Ê€á´€á´</a> Ê€á´‡sá´Éª",
            SentCodeType.SMS: "sá´s á´€É´á´…á´€",
            SentCodeType.CALL: "á´˜á´€É´É¢É¢ÉªÊŸá´€É´ á´›á´‡ÊŸá´˜á´É´",
            SentCodeType.FLASH_CALL: "á´˜á´€É´É¢É¢ÉªÊŸá´€É´ á´‹ÉªÊŸá´€á´› á´›á´‡ÊŸá´‡á´˜á´É´",
            SentCodeType.FRAGMENT_SMS: "êœ°Ê€á´€É¢á´á´‡É´á´› sá´s",
            SentCodeType.EMAIL_CODE: "á´‡á´á´€ÉªÊŸ á´€É´á´…á´€",
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                "<b>sÉªÊŸá´€á´‹á´€É´ á´˜á´‡Ê€Éªá´‹sá´€ á´‹á´á´…á´‡ á´á´›á´˜ á´…á´€Ê€Éª á´€á´‹á´œÉ´ Ê€á´‡êœ±á´Éª á´›á´‡ÊŸá´‡É¢Ê€á´€á´. á´‹ÉªÊ€Éªá´ á´‹á´á´…á´‡ á´á´›á´˜ á´‹á´‡ sÉªÉ´Éª sá´‡á´›á´‡ÊŸá´€Êœ á´á´‡á´Ê™á´€á´„á´€ êœ°á´Ê€á´á´€á´› á´…Éª Ê™á´€á´¡á´€Êœ ÉªÉ´Éª.</b>\n"
                "\ná´ŠÉªá´‹á´€ á´‹á´á´…á´‡ á´á´›á´˜ á´€á´…á´€ÊŸá´€Êœ <á´„á´á´…á´‡>12345</á´„á´á´…á´‡> á´›á´ÊŸá´É´É¢ <b>[ á´›á´€á´Ê™á´€Êœá´‹á´€É´ sá´˜á´€sÉª ]</b> á´‹ÉªÊ€Éªá´á´‹á´€É´ sá´‡á´˜á´‡Ê€á´›Éª ÉªÉ´Éª <code>1 2 3 4 5</code>\n"
                "\n<b>É¢á´œÉ´á´€á´‹á´€É´ /cancel á´œÉ´á´›á´œá´‹ á´á´‡á´Ê™á´€á´›á´€ÊŸá´‹á´€É´ á´˜Ê€á´sá´‡s á´á´‡á´Ê™á´œá´€á´› á´œsá´‡Ê€Ê™á´á´›</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<blockquote>á´˜á´‡á´Ê™á´€á´›á´€ÊŸá´€É´ á´á´›á´á´á´€á´›Éªêœ±!\nÉ´É¢á´œÉ´á´€á´‹á´€É´ /êœ±á´›á´€Ê€á´› á´œÉ´á´›á´œá´‹ á´á´‡á´á´œÊŸá´€Éª á´œÊŸá´€É´É¢</blockquote>")
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
                "á´€á´‹á´œÉ´ á´€É´á´…á´€ á´›á´‡ÊŸá´€Êœ á´á´‡É´É¢á´€á´‹á´›Éªêœ°á´‹á´€É´ á´ á´‡Ê€Éªêœ°Éªá´‹á´€sÉª á´…á´œá´€ ÊŸá´€É´É¢á´‹á´€Êœ. sÉªÊŸá´€Êœá´‹á´€É´ á´‹ÉªÊ€Éªá´á´‹á´€É´ á´˜á´€ssá´¡á´Ê€á´…É´Êá´€.\n\nÉ¢á´œÉ´á´€á´‹á´€É´ /cancel á´œÉ´á´›á´œá´‹ á´á´‡á´Ê™á´€á´›á´€ÊŸá´‹á´€É´ á´˜Ê€á´sá´‡s á´á´‡á´Ê™á´œá´€á´› á´œsá´‡Ê€Ê™á´á´›</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "<blockquote>á´˜á´‡á´Ê™á´€á´›á´€ÊŸá´€É´ á´á´›á´á´á´€á´›Éªêœ±!\nÉ´É¢á´œÉ´á´€á´‹á´€É´ /êœ±á´›á´€Ê€á´› á´œÉ´á´›á´œá´‹ á´á´‡á´á´œÊŸá´€Éª á´œÊŸá´€É´É¢</blockquote>")
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
        "sá´‡á´…á´€É´É¢ á´á´‡á´á´˜Ê€á´sá´‡s....\n\nsÉªÊŸá´€Êœá´‹á´€É´ á´›á´œÉ´É¢É¢á´œ sá´‡Ê™á´‡É´á´›á´€Ê€",
        disable_web_page_preview=True,
    )
    await new_client.start()
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        return await bot_msg.edit(
            "<b>Êœá´€Ê€á´€á´˜ É¢á´œÉ´á´€á´‹á´€É´ É´á´á´á´‡Ê€ á´›á´‡ÊŸá´‡É¢Ê€á´€á´ á´€É´á´…á´€ á´…Éª á´€á´‹á´œÉ´ á´€É´á´…á´€ sá´€á´€á´› ÉªÉ´Éª á´…á´€É´ Ê™á´œá´‹á´€É´ É´á´á´á´‡Ê€ á´›á´‡ÊŸá´‡É¢Ê€á´€á´ á´…á´€Ê€Éª á´€á´‹á´œÉ´ ÊŸá´€ÉªÉ´</>"
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
            [InlineKeyboardButton("á´‹á´‡á´Ê™á´€ÊŸÉª", callback_data=f"home {user_id}")],
        ]
    text_done = f"""
<blockquote><b>Ê™á´‡Ê€Êœá´€êœ±ÉªÊŸ á´…Éªá´€á´‹á´›Éªêœ°á´‹á´€É´
É´á´€á´á´‡ : <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a>
Éªá´… : {new_client.me.id}
á´˜Ê€á´‡êœ°Éªxá´‡êœ± : {' '.join(SH)}
á´ŠÉªá´‹á´€ Ê™á´á´› á´›Éªá´…á´€á´‹ Ê€á´‡êœ±á´˜á´É´, á´‹á´‡á´›Éªá´‹ /restart</b></blockquote>
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
<b>â á´œsá´‡Ê€Ê™á´á´› á´…Éªá´€á´‹á´›ÉªÒ“á´‹á´€É´</b>
<b> â”œ á´€á´‹á´œÉ´:</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> â•° Éªá´…:</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ðŸ“ á´„á´‡á´‹ á´á´€sá´€ á´€á´‹á´›ÉªÒ“ ðŸ“",
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
            callback_query.from_user.id, "<blockquote>á´˜á´‡á´Ê™á´€á´›á´€ÊŸá´€É´ á´á´›á´á´á´€á´›Éªêœ±!\nÉ´É¢á´œÉ´á´€á´‹á´€É´ /êœ±á´›á´€Ê€á´› á´œÉ´á´›á´œá´‹ á´á´‡á´á´œÊŸá´€Éª á´œÊŸá´€É´É¢</blockquote>"
        )
        return True
    return False


@PY.BOT("control")
async def _(client, message):
    buttons = [
            [InlineKeyboardButton("Ê€á´‡êœ±á´›á´€Ê€á´›", callback_data=f"ress_ubot")],
        ]
    await message.reply(
            f"""
<blockquote><b>á´€É´á´…á´€ á´€á´‹á´€É´ á´á´‡ÊŸá´€á´‹á´œá´‹á´€É´ Ê€á´‡êœ±á´›á´€Ê€á´›?!\n á´ŠÉªá´‹á´€ ÉªÊá´€ á´˜á´‡É´á´„á´‡á´› á´›á´á´Ê™á´ÊŸ á´…Éª Ê™á´€á´¡á´€Êœ ÉªÉ´Éª</b></blockquote>
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
                            f"Ê€á´‡êœ±á´›á´€Ê€á´› Ê™á´‡Ê€Êœá´€êœ±ÉªÊŸ á´…ÉªÊŸá´€á´‹á´œá´‹á´€É´ !\n\n É´á´€á´á´‡: {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}"
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(f"{error}")

@PY.BOT("restart")
async def _(client, message):
    msg = await message.reply("<b>á´›á´œÉ´É¢É¢á´œ sá´‡Ê™á´‡É´á´›á´€Ê€</b>")
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
                            f"Ê€á´‡êœ±á´›á´€Ê€á´› Ê™á´‡Ê€Êœá´€êœ±ÉªÊŸ á´…ÉªÊŸá´€á´‹á´œá´‹á´€É´ !\n\n É´á´€á´á´‡: {UB.me.first_name} {UB.me.last_name or ''} | `{UB.me.id}`"
                        )
                    except Exception as error:
                        return await msg.edit(f"{error}")

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
        return await callback_query.answer(f"â³ á´›ÉªÉ´É¢É¢á´€ÊŸ {xxxx} Êœá´€Ê€Éª ÊŸá´€É¢Éª", True)
    except:
        return await callback_query.answer("âœ… sá´œá´…á´€Êœ á´›Éªá´…á´€á´‹ á´€á´‹á´›ÉªÒ“", True)

@PY.CALLBACK("del_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        return await callback_query.answer(
            f"âŒ á´›á´á´Ê™á´ÊŸ ÉªÉ´Éª Ê™á´œá´‹á´€É´ á´œÉ´á´›á´œá´‹ á´á´œ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
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
                f"âœ… {get_mention} Ê™á´‡Ê€Êœá´€sÉªÊŸ á´…ÉªÊœá´€á´˜á´œs á´…á´€Ê€Éª á´…á´€á´›á´€Ê™á´€sá´‡", True
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
