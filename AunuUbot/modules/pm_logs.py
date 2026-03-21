import wget

from gc import get_objects
from pyrogram.errors.exceptions.not_acceptable_406 import UserRestricted
from pykeyboard import InlineKeyboard
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent)

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from AunuUbot import *


FLOOD = {}
MSG_ID = {}
PM_TEXT = """
<blockquote>🙋🏻‍♂halo {mention} ada yang bisa saya bantu?

perkenalkan saya adalah pm-security disini
silahkan tunggu majikan saya membalas pesan mu ini ya
jangan spam ya atau anda akan di blokir secara otomatis

��peringatan: {warn} hati-hati</blockquote>
"""


__MODULE__ = "ᴘᴍᴘᴇʀᴍɪᴛ"
__HELP__ = """
<blockquote>Bantuan Untuk Pmpermit

perintah : <code>{0}pmpermit</code> query > on or off
    mengaktifkan atau menonaktifkan pm permit

perintah : <code>{0}ok</code>
�   mengizinkan seseoranh untuk pm anda

perintah : <code>{0}no</code>
�   menolak seseorang untuk pm anda

perintah : <code>{0}setpm</code>
query: |pic |text |limit
�   mengatur configuration pada pm_permit

contoh menggunakan button  : <a href='https://t.me/halopyrogram/172'>tutorial</a>

contoh menggunakan gambar yang benar  : <a href='https://t.me/halopyrogram/192'>tutorial</a>

contoh menggunakan warning 
    command : setpm limit 5</blockquote>
"""


@PY.NO_CMD_UBOT("PMPERMIT", ubot)
async def _(client, message):
    DEVS = [5506568422]
    user = message.from_user
    if user.id in DEVS:
        return
    pm_on = await get_vars(client.me.id, "PMPERMIT")
    if pm_on:
        if user.id in MSG_ID:
            await delete_old_message(message, MSG_ID.get(user.id, 0))
        check = await get_pm_id(client.me.id)
        if user.id not in check:
            if user.id in FLOOD:
                FLOOD[user.id] += 1
            else:
                FLOOD[user.id] = 1
            pm_limit = await get_vars(client.me.id, "PM_LIMIT") or "5"
            try:
                if FLOOD[user.id] > int(pm_limit):
                    del FLOOD[user.id]
                    await message.reply(
                        "sudah diingatkan jangan spam, sekarang Anda diblokir."
                    )
                    return await client.block_user(user.id)
            except ValueError:
                await set_vars(client.me.id, "PM_LIMIT", "5")
            pm_msg = await get_vars(client.me.id, "PM_TEXT") or PM_TEXT
            if "~>" in pm_msg:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"pm_pr {id(message)} {FLOOD[user.id]}"
                )
                msg = await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=message.id,
                )
                MSG_ID[user.id] = int(msg.updates[0].id)
            else:
                try:
                    pm_pic = await get_vars(client.me.id, "PM_PIC")
                    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
                    peringatan = f"{FLOOD[user.id]} / {pm_limit}"
                    if pm_pic:
                        try:
                            msg = await message.reply_photo(
                                pm_pic, caption=pm_msg.format(mention=rpk, warn=peringatan)
                            )
                        except ValueError:
                            await set_vars(client.me.id, "PM_PIC", "https://telegra.ph//file/be22060c145c058bf4558.jpg")
                    else:
                        msg = await message.reply(
                            pm_msg.format(mention=rpk, warn=peringatan)
                        )
                    MSG_ID[user.id] = msg.id
                except UnboundLocalError:
                    pass


@PY.UBOT("setpm")
@PY.TOP_CMD
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    if len(message.command) < 3:
        return await message.reply(
            f"{ggl}{message.text.split()[0]} [query] [value]"
        )
    query = {"limit": "PM_LIMIT", "text": "PM_TEXT", "pic": "PM_PIC"}
    if message.command[1].lower() not in query:
        return await message.reply(f"{ggl}query yang di masukkan tidak valid")
    query_str, value_str = (
        message.text.split(None, 2)[1],
        message.text.split(None, 2)[2],
    )
    value = query[query_str]
    if value_str.lower() == "none":
        value_str = False
    await set_vars(client.me.id, value, value_str)
    return await message.reply(
        f"{brhsl}pmpermit berhasil disetting"
    )


@PY.UBOT("pmpermit")
@PY.TOP_CMD
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    if len(message.command) < 2:
        return await message.reply(
            f"{ggl}{message.text.split()[0]} [on/off]"
        )

    toggle_options = {"off": False, "on": True}
    toggle_option = message.command[1].lower()

    if toggle_option not in toggle_options:
        return await message.reply(f"{ggl}opsi tidak valid. Harap gunakan 'on' atau 'off'.")

    value = toggle_options[toggle_option]
    text = "diaktifkan" if value else "dinonaktifkan"

    await set_vars(client.me.id, "PMPERMIT", value)
    await message.reply(f"{brhsl}pmpermit berhasil {text}")


@PY.INLINE("pm_pr")
async def _(client, inline_query):
    get_id = inline_query.query.split()
    m = [obj for obj in get_objects() if id(obj) == int(get_id[1])][0]
    pm_msg = await get_vars(m._client.me.id, "PM_TEXT") or PM_TEXT
    pm_limit = await get_vars(m._client.me.id, "PM_LIMIT") or 5
    pm_pic = await get_vars(m._client.me.id, "PM_PIC")
    rpk = f"[{m.from_user.first_name} {m.from_user.last_name or ''}](tg://user?id={m.from_user.id})"
    peringatan = f"{int(get_id[2])} / {pm_limit}"
    buttons, text = await pmpermit_button(pm_msg)
    if pm_pic:
        photo_video = InlineQueryResultVideo if pm_pic.endswith(".mp4") else InlineQueryResultPhoto
        photo_video_url = {"video_url": pm_pic, "thumb_url": pm_pic} if pm_pic.endswith(".mp4") else {"photo_url": pm_pic}
        hasil = [
            photo_video(
                **photo_video_url,
                title="Dapatkan tombol!",
                caption=text.format(mention=rpk, warn=peringatan),
                reply_markup=buttons,
            )
        ]
    else:
        hasil = [
            (
                InlineQueryResultArticle(
                    title="Dapatkan tombol!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(text.format(mention=rpk, warn=peringatan)),
                )
            )
        ]
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=hasil,
    )


@PY.UBOT("ok|terima")
@PY.TOP_CMD
@PY.PRIVATE
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    brhsl = await EMO.BERHASIL(client)
    user = message.chat
    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    vars = await get_pm_id(client.me.id)
    if user.id not in vars:
        await add_pm_id(client.me.id, user.id)
        return await message.reply(f"{brhsl}baiklah, {rpk} telah diterima")
    else:
        return await message.reply(f"{brhsl}{rpk} sudah diterima")


@PY.UBOT("no|tolak")
@PY.TOP_CMD
@PY.PRIVATE
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    user = message.chat
    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    vars = await get_pm_id(client.me.id)
    if user.id not in vars:
        await message.reply(f"{ggl}🙏🏻 maaf ⁣{rpk} anda telah diblokir")
        return await client.block_user(user.id)
    else:
        await remove_pm_id(client.me.id, user.id)
        return await message.reply(
            f"{ggl}🙏🏻 maaf {rpk} anda telah ditolak untuk menghubungi akun ini lagi"
        )

async def pmpermit_button(m):
    buttons = InlineKeyboard(row_width=1)
    keyboard = []
    for X in m.split("~>", 1)[1].split():
        X_parts = X.split(":", 1)
        keyboard.append(InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1]))
    buttons.add(*keyboard)
    text = m.split("~>", 1)[0]

    return buttons, text


async def delete_old_message(message, msg_id):
    try:
        await message._client.delete_messages(message.chat.id, msg_id)
    except:
        pass


async def send_log(client, chat_id, message, message_text, msg):
    try:
        await client.send_message(chat_id, message_text, disable_web_page_preview=True)
        await message.forward(chat_id)
    except Exception as error:
        print(f"{msg} ERROR: GAGAL MENERUSKAN PESAN")

@PY.UBOT("logs")
@PY.TOP_CMD
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    if len(message.command) < 2:
        return await message.reply(
            f"{ggl}{message.text.split()[0]} [on/off]"
        )

    query = {"on": True, "off": False, "none": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(f"{ggl}opsi tidak valid!!")

    value = query[command]

    await set_vars(client.me.id, "ON_LOGS", value)
    return await message.reply(
        f"{brhsl}LOGS berhasil disetting ke: {value}"
    )


@PY.NO_CMD_UBOT("LOGS_GROUP", ubot)
async def _(client, message):
    on_logs = await get_vars(client.me.id, "ON_LOGS")
    if on_logs:
        user_link = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
        message_link = message.link
        message_text = f"""
🤖 ada pesan masuk dari {message.chat.title} 
👤 pengguna : {message.from_user.first_name} 
🗯 pesan : {message.text}
"""
        await bot.send_message(
            client.me.id,
            message_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("grup", url=f"{message_link}")],
            ]))
