from AunuUbot import *
import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message

__MODULE__ = "ʙɪɴɢᴀɪ"
__HELP__ = """
<blockquote><b>Bantuan Untuk ʙɪɴɢᴀɪ

perintah : <code>{0}bing</code>
    bbuat pertanyaan contoh <code>{0}bing</code> dimana letak Antartika</b></blockquote>
"""


@PY.UBOT("bing")
@PY.TOP_CMD
async def chat_gpt(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji>mohon gunakan format\ncontoh : .bing bagaimana membuat donat?"
            )
        else:
            prs = await message.reply_text(f"<emoji id=6226405134004389590>🔍</emoji>proccesing....")
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://widipe.com/bingai?text={a}')

            try:
                if "result" in response.json():
                    x = response.json()["result"]                  
                    await prs.edit(
                      f"<blockquote>{x}</blockquote>"
                    )
                else:
                    await message.reply_text("No 'results' key found in the response.")
            except KeyError:
                await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")
