import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.types import ChatPermissions
from AunuUbot import *


__MODULE__ = "ɢʟᴏʙᴀʟ"
__HELP__ = """
<blockquote>Bantuan Untuk Global

perintah : <code>{0}gban</code>
    banned user dari semua group chat 

perintah : <code>{0}ungban</code>
    unbanned user dari semua group chat

perintah : <code>{0}gmute</code>
    untuk mengemute user dari semua gc yg kmu admin 

perintah : <code>{0}ungmute</code>
    untuk meng ungmute user dari semua gc yg kmu admin</blockquote> 
"""

      

@PY.UBOT("gban")
@PY.TOP_CMD
@PY.COOLDOWN(12, bucket="global")
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    _msg = f"{prs}proceꜱꜱing..."

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"{ggl}user tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "global {}\n\nberhasil: {} chat\ngagal: {} chat\nuser: <a href='tg://user?id={}'>{} {}</a>"
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        if user.id == OWNER_ID:
            return await Tm.edit(f"{ggl}anda tidak bisa gban dia karena dia pembuat saya")
        try:
            await client.ban_chat_member(dialog, user.id)
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(
        text.format(
            "banned", done, failed, user.id, user.first_name, (user.last_name or "")
        )
    )
    return await Tm.delete()


@PY.UBOT("ungban")
@PY.TOP_CMD
@PY.COOLDOWN(12, bucket="global")
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    _msg = f"{prs}proceꜱꜱing..."

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"{ggl}user tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "global {}\n\nberhasil: {} chat\ngagal: {} chat\nuser: <a href='tg://user?id={}'>{} {}</a>"
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        try:
            await client.unban_chat_member(dialog, user.id)
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(
        text.format(
            "unbanned",
            done,
            failed,
            user.id,
            user.first_name,
            (user.last_name or ""),
        )
    )
    return await Tm.delete()

@PY.UBOT("gmute")
@PY.TOP_CMD
@PY.COOLDOWN(12, bucket="global")
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    _msg = f"{prs}proceꜱꜱing..."

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"{ggl}user tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "global {}\n\nberhasil: {} chat\ngagal: {} chat\nuser: <a href='tg://user?id={}'>{} {}</a>"
    global_id = await get_data_id(client, "group")
    for dialog in global_id:
        if user.id == OWNER_ID:
            return await Tm.edit(f"{ggl}anda tidak bisa gmute dia karena dia pembuat saya")
        try:
            await client.restrict_chat_member(dialog, user.id, ChatPermissions(can_send_messages=False))
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(
        text.format(
            "mute", done, failed, user.id, user.first_name, (user.last_name or "")
        )
    )
    return await Tm.delete()

@PY.UBOT("ungmute")
@PY.TOP_CMD
@PY.COOLDOWN(12, bucket="global")
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    _msg = f"{prs}proceꜱꜱing..."
    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"{ggl}user tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "global {}\n\nberhasil: {} chat\ngagal: {} chat\nuser: <a href='tg://user?id={}'>{} {}</a>"
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        try:
            await client.restrict_chat_member(dialog, user.id, ChatPermissions(can_send_messages=True))
            done += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1
            await asyncio.sleep(0.1)
    await message.reply(
        text.format(
            "ungmuted",
            done,
            failed,
            user.id,
            user.first_name,
            (user.last_name or ""),
        )
    )
    return await Tm.delete()
