import random
import re
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from AunuUbot.config import OWNER_ID
import psutil
from AunuUbot import *
from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping
from pyrogram.types import *

from AunuUbot import *


def inline_disabled(error):
    return "BOT_INLINE_DISABLED" in str(error)


def sc(text):
    return Fonts.smallcap(text)


async def build_help_overview_text(client, user):
    SH = await ubot.get_prefix(user.id)
    help_modules = len(HELP_COMMANDS)
    status = sc("premium")
    if user.id == OWNER_ID:
        status = sc("owner")
    elif user.id in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        status = sc("admin")
    elif user.id in await get_list_from_vars(client.me.id, "SELER_USERS"):
        status = sc("seller")
    return (
        f"<blockquote><b>❖ ʜᴇʟᴘ ᴄᴇɴᴛᴇʀ ❖</b></blockquote>\n"
        f"<blockquote>👤 ᴜsᴇʀ: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a>\n"
        f"🪪 ʀᴏʟᴇ: <code>{status}</code>\n"
        f"⚙️ ᴘʀᴇғɪx: <code>{' '.join(SH)}</code></blockquote>\n"
        f"<blockquote>🧩 ᴍᴏᴅᴜʟᴇs: <code>{help_modules}</code>\n"
        f"🚀 ᴄᴏᴍᴍᴀɴᴅs: <code>{get_total_commands()}</code>\n"
        f"🧠 ɴᴀᴠɪɢᴀᴛᴇ: <code>ᴛᴀᴘ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ</code></blockquote>\n"
        f"<blockquote><b>⌞ ᴀᴜɴᴜ ᴜʙᴏᴛ ᴍᴀɴᴀɢᴇʀ ⌝</b></blockquote>"
    )


async def send_help_overview(client, message):
    text = await build_help_overview_text(client, message.from_user)
    buttons = InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help"))
    help_photo = await get_vars(client.me.id, "HELP_PHOTO")
    if help_photo:
        return await client.send_photo(
            message.chat.id,
            help_photo,
            caption=text,
            reply_markup=buttons,
            reply_to_message_id=message.id,
        )
    return await message.reply(text, quote=True, reply_markup=buttons)


async def edit_help_page(callback_query, text, buttons):
    if getattr(callback_query, "message", None) and getattr(callback_query.message, "photo", None):
        return await callback_query.edit_message_caption(
            caption=text,
            reply_markup=buttons,
        )
    return await callback_query.edit_message_text(
        text=text,
        reply_markup=buttons,
        disable_web_page_preview=True,
    )


async def build_alive_text(client, owner_client):
    try:
        peer = owner_client._get_my_peer[owner_client.me.id]
        users = len(peer["pm"])
        group = len(peer["gc"])
    except Exception:
        users = random.randrange(await owner_client.get_dialogs_count())
        group = random.randrange(await owner_client.get_dialogs_count())
    get_exp = await get_expired_date(owner_client.me.id)
    exp = get_exp.strftime("%d-%m-%Y") if get_exp else "None"
    if owner_client.me.id == OWNER_ID:
        status = "ᴀᴜɴᴜ-ᴜʙᴏᴛ <code>[ᴏᴡɴᴇʀ]</code>"
    elif owner_client.me.id in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        status = "ᴀᴜɴᴜ-ᴜʙᴏᴛ <code>[ᴀᴅᴍɪɴ]</code>"
    elif owner_client.me.id in await get_list_from_vars(client.me.id, "SELER_USERS"):
        status = "ᴀᴜɴᴜ-ᴜʙᴏᴛ <code>[sᴇʟʟᴇʀ]</code>"
    else:
        status = "ᴀᴜɴᴜ-ᴜʙᴏᴛ <code>[ᴘʀᴇᴍɪᴜᴍ]</code>"
    start = datetime.now()
    await owner_client.invoke(Ping(ping_id=0))
    ping = (datetime.now() - start).microseconds / 1000
    uptime = await get_time((time() - start_time))
    return f"""
<blockquote>{bot.me.mention}
    `sᴛᴀᴛᴜs: {status}`
        `ᴇxᴘɪʀᴇᴅ_ᴏɴ: {exp}` 
        `ᴅᴄ_ɪᴅ: {owner_client.me.dc_id}`
        `ᴘɪɴɢ_ᴅᴄ: {ping} ᴍs`
        `ᴘᴇᴇʀ_ᴜsᴇʀs: {users} ᴜsᴇʀs`
        `ᴘᴇᴇʀ_ɢʀᴏᴜᴘ: {group} ɢʀᴏᴜᴘ`
        `sᴛᴀʀᴛ_ᴜᴘᴛɪᴍᴇ: {uptime}`</blockquote>
"""


@PY.UBOT("alive")
@PY.TOP_CMD
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(
            bot.me.username, f"alive {message.id} {client.me.id}"
        )
        await message.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)
    except Exception as error:
        if not inline_disabled(error):
            return await message.reply(error)
        msg = await build_alive_text(client, client)
        await message.reply(msg, quote=True)
    



@PY.INLINE("^alive")
async def _(client, inline_query):
    get_id = inline_query.query.split()
    for my in ubot._ubot:
        if int(get_id[2]) == my.me.id:
            try:
                peer = my._get_my_peer[my.me.id]
                users = len(peer["pm"])
                group = len(peer["gc"])
            except Exception:
                users = random.randrange(await my.get_dialogs_count())
                group = random.randrange(await my.get_dialogs_count())
            get_exp = await get_expired_date(my.me.id)
            exp = get_exp.strftime("%d-%m-%Y") if get_exp else "None"
            if my.me.id == OWNER_ID:
                status = "ᴀᴜɴᴜ-ᴜʙᴏᴛ <code>[ᴏᴡɴᴇʀ]</code>"
            elif my.me.id in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
                status = "ᴀᴜɴᴜ-ᴜʙᴏᴛ <code>[ᴀᴅᴍɪɴ]</code>"
            elif my.me.id in await get_list_from_vars(client.me.id, "SELER_USERS"):
                status = "ᴀᴜɴᴜ-ᴜʙᴏᴛ <code>[sᴇʟʟᴇʀ]</code>"
            else:
                status = "ᴀᴜɴᴜ-ᴜʙᴏᴛ <code>[ᴘʀᴇᴍɪᴜᴍ]</code>"
            button = BTN.ALIVE(get_id)
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime = await get_time((time() - start_time))
            msg = f"""
<blockquote>{bot.me.mention}
    `sᴛᴀᴛᴜs: {status}`
        `ᴇxᴘɪʀᴇᴅ_ᴏɴ: {exp}` 
        `ᴅᴄ_ɪᴅ: {my.me.dc_id}`
        `ᴘɪɴɢ_ᴅᴄ: {ping} ᴍs`
        `ᴘᴇᴇʀ_ᴜsᴇʀs: {users} ᴜsᴇʀs`
        `ᴘᴇᴇʀ_ɢʀᴏᴜᴘ: {group} ɢʀᴏᴜᴘ`
        `sᴛᴀʀᴛ_ᴜᴘᴛɪᴍᴇ: {uptime}`</blockquote>
"""
            await client.answer_inline_query(
                inline_query.id,
                cache_time=300,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="ᴀʟɪᴠᴇ",
                            reply_markup=InlineKeyboardMarkup(button),
                            input_message_content=InputTextMessageContent(msg),
                        )
                    )
                ],
            )


@PY.CALLBACK("alv_cls")
async def _(client, callback_query):
    get_id = callback_query.data.split()
    if not callback_query.from_user.id == int(get_id[2]):
        return
    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for my in ubot._ubot:
        if callback_query.from_user.id == int(my.me.id):
            await my.delete_messages(
                unPacked.chat_id, [int(get_id[1]), unPacked.message_id]
            )


@PY.BOT("anu")
@PY.ADMIN
async def _(client, message):
    buttons = BTN.BOT_HELP(message)
    text = (
        "<blockquote><b>❖ ʙᴏᴛ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ ❖</b></blockquote>\n"
        "<blockquote>🛠 ᴘɪʟɪʜ ᴍᴇɴᴜ ᴅɪ ʙᴀᴡᴀʜ\n"
        "📦 ᴋᴇʟᴏʟᴀ ᴜʙᴏᴛ, sʏsᴛᴇᴍ, ᴜᴘᴅᴀᴛᴇ, ᴅᴀɴ ʀᴏʟᴇ ᴜsᴇʀ</blockquote>"
    )
    sh = await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))
    

@PY.CALLBACK("balik")
async def _(client, callback_query):
    buttons = BTN.BOT_HELP(callback_query)
    text = (
        "<blockquote><b>❖ ʙᴏᴛ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ ❖</b></blockquote>\n"
        "<blockquote>🛠 ᴘɪʟɪʜ ᴍᴇɴᴜ ᴅɪ ʙᴀᴡᴀʜ\n"
        "📦 ᴋᴇʟᴏʟᴀ ᴜʙᴏᴛ, sʏsᴛᴇᴍ, ᴜᴘᴅᴀᴛᴇ, ᴅᴀɴ ʀᴏʟᴇ ᴜsᴇʀ</blockquote>"
    )
    sh = await callback_query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

@PY.CALLBACK("reboot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        return await callback_query.answer("tombol ini bukan untuk lu", True)
    await callback_query.answer("system berhasil di restart", True)
    subprocess.call(["bash", "start.sh"])

@PY.CALLBACK("update")
async def _(client, callback_query):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    user_id = callback_query.from_user.id
    if not user_id == OWNER_ID:
        return await callback_query.answer("tombol ini bukan untuk lu", True)
    if "Already up to date." in str(out):
        return await callback_query.answer("sᴜᴅᴀʜ ᴛᴇʀᴜᴘᴅᴀᴛᴇ", True)
    else:
        await callback_query.answer("sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs ᴜᴘᴅᴀᴛᴇ.....", True)
    os.execl(sys.executable, sys.executable, "-m", "AunuUbot")


@PY.UBOT("help")
async def user_help(client, message):
    if not get_arg(message):
        help_photo = await get_vars(client.me.id, "HELP_PHOTO")
        if help_photo:
            return await send_help_overview(client, message)
        try:
            x = await client.get_inline_bot_results(bot.me.username, "user_help")
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        except Exception as error:
            if not inline_disabled(error):
                return await message.reply(error)
            await send_help_overview(client, message)
    else:
        module = (get_arg(message))
        if get_arg(message) in HELP_COMMANDS:
            prefix = await ubot.get_prefix(client.me.id)
            module_title = getattr(HELP_COMMANDS[get_arg(message)], "__MODULE__", module)
            await message.reply(
                "<blockquote><b>❖ {} ❖</b></blockquote>\n{}\n<blockquote><b>{}</b></blockquote>".format(
                    module_title,
                    HELP_COMMANDS[get_arg(message)].__HELP__.format(next((p) for p in prefix)),
                    "⌞ ᴛᴀᴘ ʙᴀᴄᴋ ᴛᴏ ʀᴇᴛᴜʀɴ ⌝",
                ),
                quote=True,
            )
        else:
            await message.reply(
                f"<b>❌ ɴᴏ ᴍᴏᴅᴜʟᴇ ғᴏᴜɴᴅ <code>{module}</code></b>"
            )

@PY.UBOT("helpall")
@PY.TOP_CMD
@PY.COOLDOWN(5)
async def _(client, message):
    prefix = next((p) for p in await ubot.get_prefix(client.me.id))
    chunks = []
    for module_name in sorted(HELP_COMMANDS):
        module = HELP_COMMANDS[module_name]
        help_text = getattr(module, "__HELP__", None)
        if not help_text:
            continue
        chunks.append(
            f"<b>{getattr(module, '__MODULE__', module_name)}</b>\n"
            f"{help_text.format(prefix)}"
        )
    if not chunks:
        return await message.reply_text("<b>Belum ada data help yang tersedia.</b>")
    text = "\n\n".join(chunks)
    for start in range(0, len(text), 3500):
        await message.reply_text(text[start:start + 3500], disable_web_page_preview=True)

@PY.INLINE("^user_help")
async def user_help_inline(client, inline_query):
    msg = await build_help_overview_text(client, inline_query.from_user)
    results = [InlineQueryResultArticle(
        title="Help Menu!",
        reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
        input_message_content=InputTextMessageContent(msg),
    )]
    await client.answer_inline_query(inline_query.id, cache_time=60, results=results)

@PY.CALLBACK("^close_user")
async def close_usernya(client, callback_query):
    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for x in ubot._ubot:
        if callback_query.from_user.id == int(x.me.id):
            await x.delete_messages(
                unPacked.chat_id, unPacked.message_id
            )

@PY.CALLBACK("help_(.*?)")
async def help_callback(client, callback_query):
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
    next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
    tutup_match = re.match(r"help_tutup\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    SH = await ubot.get_prefix(callback_query.from_user.id)
    top_text = await build_help_overview_text(client, callback_query.from_user)

    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        module_title = getattr(HELP_COMMANDS[module], "__MODULE__", module)
        text = (
            "<blockquote><b>❖ {} ❖</b></blockquote>\n{}\n<blockquote><b>{}</b></blockquote>".format(
                module_title,
                HELP_COMMANDS[module].__HELP__.format(next((p) for p in SH)),
                "⌞ ᴀᴜɴᴜ ᴜʙᴏᴛ ʜᴇʟᴘ ⌝",
            )
        )
        button = [[InlineKeyboardButton("⊲ ʙᴀᴄᴋ", callback_data="help_back")]]
        await edit_help_page(
            callback_query,
            text + '\n<blockquote><b>-- USERBOT 15K/BULAN BY @AunuHostv --</b></blockquote>',
            InlineKeyboardMarkup(button),
        )
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await edit_help_page(
            callback_query,
            top_text,
            InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELP_COMMANDS, "help")),
        )
    elif next_match:
        next_page = int(next_match.group(1))
        await edit_help_page(
            callback_query,
            top_text,
            InlineKeyboardMarkup(paginate_modules(next_page + 1, HELP_COMMANDS, "help")),
        )
    elif back_match:
        await edit_help_page(
            callback_query,
            top_text,
            InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
        )
