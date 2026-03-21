from AunuUbot import *

__MODULE__ = "ᴄᴏᴘʏ"
__HELP__ = """
<blockquote>Bantuan Untuk Copy

perintah : <code>{0}copy</code> [link_konten_telegram]
    untuk mengambil pesan dan postingan chanel telegram melalui link mereka</blockquote>
"""
import asyncio
import os

from gc import get_objects
from time import time
from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import *
from pyrogram import *
from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent)

from AunuUbot import *

async def nyolongnih(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    try:
        await message.edit(f"{prs}proccesing...")
        link = get_arg(message)
        msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            try:
                chat = int("-100" + str(link.split("/")[-2]))
                dia = await client.get_messages(chat, msg_id)
            except RPCError:
                await message.edit(f"{ggl}**sepertinya terjadi kesalahan**")
        else:
            try:
                chat = str(link.split("/")[-2])
                dia = await client.get_messages(chat, msg_id)
            except RPCError:
                await message.edit(f"{ggl}**sepertinya terjadi kesalahan**")
        anjing = dia.caption or None
        if dia.text:
            await dia.copy(message.chat.id)
            await message.delete()
        if dia.photo:
            anu = await client.download_media(dia)
            await client.send_photo(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        
        if dia.video:
            anu = await client.download_media(dia)
            await client.send_video(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        
        if dia.audio:
            anu = await client.download_media(dia)
            await client.send_audio(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        
        if dia.voice:
            anu = await client.download_media(dia)
            await client.send_voice(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        
        if dia.document:
            anu = await client.download_media(dia)
            await client.send_document(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        else:
            await message.edit(f"{ggl}**sepertinya terjadi kesalahan**")
    except Exception as e:
        await message.reply_text(e)

@PY.UBOT("copy")
async def _(client, message):
    await nyolongnih(client, message)

