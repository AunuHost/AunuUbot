from AunuUbot import *
import os
import json
import asyncio
import psutil
from datetime import datetime
from gc import get_objects
from time import time
from pyrogram.raw import *
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AunuUbot import *

@PY.INDRI("dping")
async def _(client, message):
    try:
        start = datetime.now()
        await client.invoke(Ping(ping_id=0))
        end = datetime.now()
        uptime = await get_time((time() - start_time))
        delta_ping_formatted = round((end - start).microseconds / 10000, 2)
        pong = await EMO.PING(client)
        tion = await EMO.MENTION(client)
        yubot = await EMO.UBOT(client)
        babi = client.me.is_premium
        if babi:
            _ping = f"""
<blockquote>{pong} pong : {str(delta_ping_formatted).replace('.', ',')} ms
{tion} userbot aktif bang ku</blockquote>
"""
            await message.reply(_ping)
        else:
            await message.reply(f"<blockquote>pong : {str(delta_ping_formatted).replace('.', ',')} ms\nuserbot aktif bang ku</blockquote>")
    except Exception as r:
        print(r)


@PY.INDRI("kuda")
async def _(client, message):
    await message.react("🦄")

@PY.INDRI("cinta")
async def _(client, message):
    await message.react("❤")