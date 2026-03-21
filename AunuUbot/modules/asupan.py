import random
from pyrogram.enums import MessagesFilter
from AunuUbot import *

__MODULE__ = "ᴀꜱᴜᴘᴀɴ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Asupan

perintah : <code>{0}asupan</code>
    mengirim video asupan random 

perintah : <code>{0}cewek</code>
    mengirim photo cewe random

perintah : <code>{0}cowok</code>
    mengirim photo cowo random</b></blockquote>
"""


@PY.UBOT("asupan")
@PY.TOP_CMD
async def video_asupan(client, message):
    prs = await EMO.PROSES(client)
    y = await message.reply_text(f"{prs}mencari video asupan...")
    try:
        asupannya = []
        async for asupan in client.search_messages(
            "@AsupanNyaSaiki", filter=MessagesFilter.VIDEO
        ):
            asupannya.append(asupan)
        video = random.choice(asupannya)
        await video.copy(message.chat.id, reply_to_message_id=message.id)
        await y.delete()
    except Exception as error:
        await y.edit(error)


@PY.UBOT("cewek")
@PY.TOP_CMD
async def photo_cewek(client, message):
    prs = await EMO.PROSES(client)
    y = await message.reply_text(f"{prs}mencari ayang...")
    try:
        ayangnya = []
        async for ayang in client.search_messages(
            "@AyangSaiki", filter=MessagesFilter.PHOTO
        ):
            ayangnya.append(ayang)
        photo = random.choice(ayangnya)
        await photo.copy(message.chat.id, reply_to_message_id=message.id)
        await y.delete()
    except Exception as error:
        await y.edit(error)


@PY.UBOT("cowok")
@PY.TOP_CMD
async def photo_cowok(client, message):
    prs = await EMO.PROSES(client)
    y = await message.reply_text(f"{prs}mencari ayang...")
    try:
        ayang2nya = []
        async for ayang2 in client.search_messages(
            "@Ayang2Saiki", filter=MessagesFilter.PHOTO
        ):
            ayang2nya.append(ayang2)
        photo = random.choice(ayang2nya)
        await photo.copy(message.chat.id, reply_to_message_id=message.id)
        await y.delete()
    except Exception as error:
        await y.edit(error)
