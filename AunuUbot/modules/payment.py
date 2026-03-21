import asyncio
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from AunuUbot import *

CONFIRM_PAYMENT = []


@PY.CALLBACK("^confirm")
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    CONFIRM_PAYMENT.append(get.id)
    try:
        await callback_query.message.delete()
        pesan = await bot.ask(
            user_id,
            f"""
<b>💬 sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ ʙᴜᴋᴛɪ sᴄʀᴇᴇɴsʜᴏᴛ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ: {full_name}
ᴊɪᴋᴀ ʙᴇʟᴜᴍ ᴅɪ ᴋᴏɴғɪʀᴍᴀsɪ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ @AunuHostv</b></blockquote>
""",
            timeout=300,
        )
    except asyncio.TimeoutError as out:
        return await bot.send_message(get.id, "ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs")
    if get.id in CONFIRM_PAYMENT:
        if not pesan.photo:
            CONFIRM_PAYMENT.remove(get.id)
            buttons = [[InlineKeyboardButton("✅ ᴋᴏɴꜰɪʀᴍᴀsɪ", callback_data="confirm")]]
            return await bot.send_message(
                user_id,
                """
<blockquote><b>❌ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴅɪᴘʀᴏsᴇs</b>

<b>💬 ʜᴀʀᴀᴘ ᴋɪʀɪᴍᴋᴀɴ sᴄʀᴇᴇɴsʜᴏᴛ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ʏᴀɴɢ ᴠᴀʟɪᴅ</b>

<b>✅ sɪʟᴀʜᴋᴀɴ ᴋᴏɴꜰɪʀᴍᴀsɪ ᴜʟᴀɴɢ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ</b></blockquote>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        elif pesan.photo:
            buttons = BTN.ADD_EXP(get.id)
            await pesan.copy(
                OWNER_ID,
                reply_markup=buttons,
            )
            CONFIRM_PAYMENT.remove(get.id)
            buttons = [
                [InlineKeyboardButton("📞 ᴏᴡɴᴇʀ", url=f"tg://openmessage?user_id={OWNER_ID}")]
            ]
            return await bot.send_message(
                user_id,
                f"""
<blockquote><b>💬 ʙᴀɪᴋ {full_name} sɪʟᴀʜᴋᴀɴ ᴅɪᴛᴜɴɢɢᴜ ᴅᴀɴ ᴊᴀɴɢᴀɴ sᴘᴀᴍ ʏᴀ</b>

<b>🏦 ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ᴀᴋᴀɴ ᴅɪᴋᴏɴꜰɪʀᴍᴀsɪ sᴇᴛᴇʟᴀʜ 1-24 ᴊᴀᴍ ᴋᴇʀᴊᴀ</b></blockquote>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )


@PY.CALLBACK("^(kurang|tambah)")
async def _(client, callback_query):
    BULAN = int(callback_query.data.split()[1])
    HARGA = 20
    QUERY = callback_query.data.split()[0]
    try:
        if QUERY == "kurang":
            if BULAN > 1:
                BULAN -= 1
                TOTAL_HARGA = HARGA * BULAN
        elif QUERY == "tambah":
            if BULAN < 12:
                BULAN += 1
                TOTAL_HARGA = HARGA * BULAN
        buttons = Button.plus_minus(BULAN, callback_query.from_user.id)
        await callback_query.message.reply_text(
            MSG.TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        await callback_query.message.delete()
    except:
        pass

@PY.CALLBACK("^(success|failed|home)")
async def _(client, callback_query):
    query = callback_query.data.split()
    get_user = await bot.get_users(query[1])
    if query[0] == "success":
        buttons = [
            [InlineKeyboardButton("🔥 ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ 🔥", callback_data="buat_ubot")],
        ]
        await bot.send_message(
            get_user.id,
            f"""
<blockquote><b>✅ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ʙᴇʀʜᴀsɪʟ ᴅɪᴋᴏɴꜰɪʀᴍᴀsɪ</b>

<b>💬 sᴇᴋᴀʀᴀɴɢ ᴀɴᴅᴀ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b></blockquote>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_success = [
            [
                InlineKeyboardButton(
                    "👤 ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏꜰɪʟ 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        await add_to_vars(client.me.id, "PREM_USERS", get_user.id)
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(query[2]))
        await set_expired_date(get_user.id, expired)
        return await callback_query.edit_message_text(
            f"""
<blockquote><b>✅ {get_user.first_name} {get_user.last_name or ''} ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴀɴɢɢᴏᴛᴀ ᴘʀᴇᴍɪᴜᴍ</b></blockquote>
""",
        )
    if query[0] == "failed":
        buttons = [
            [
                InlineKeyboardButton(
                    "💳 ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ 💳", callback_data="bayar_dulu"
                )
            ],
        ]
        await bot.send_message(
            get_user.id,
            """
<b>❌ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴅɪᴋᴏɴꜰɪʀᴍᴀsɪ</b>

<b>💬 sɪʟᴀʜᴋᴀɴ ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴅᴇɴɢᴀɴ ʙᴇɴᴀʀ</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_failed = [
            [
                InlineKeyboardButton(
                    "👤 ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏꜰɪʟ 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        return await callback_query.edit_message_text(
            f"""
<b>❌ {get_user.first_name} {get_user.last_name or ''} ᴛɪᴅᴀᴋ ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴀɴɢɢᴏᴛᴀ ᴘʀᴇᴍɪᴜᴍ</b>
""",
        )
    if query[0] == "home":
        if get_user.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get_user.id)
            buttons_home = BTN.START(callback_query)
            return await callback_query.edit_message_text(
                MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
        else:
            buttons_home = BTN.START(callback_query)
            return await callback_query.edit_message_text(
                MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
