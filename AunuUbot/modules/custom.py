from AunuUbot import *
from pyrogram.enums import ParseMode
__MODULE__ = "ᴄᴜꜱᴛᴏᴍ"
__HELP__ = """
<blockquote>Bantuan Untuk Custom

perintah : <code>{0}lihatemoji</code>

perintah : <code>{0}text</code>
   untuk merubah text pada tampilan tertentu

query:
  <code>{0}pong<code> | default : � pong
  <code>{0}owner<code> | default : � owner
  <code>{0}ubot<code> | default : � ubot

contoh :
     <code>{0}</code>text pong none | untuk menyeting ke default</blockquote>
"""
def extract_emojis_from_entities(message):
    emojis = []
    for entity in message.entities:
        emoji = message.text[entity.offset : entity.offset + entity.length]
        emojis.append(emoji)
    return emojis

@PY.UBOT("text")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    try:
        msg = await message.reply(f"{prs}memproses...", quote=True)

        if len(message.command) < 3:
            return await msg.edit(f"{ggl}tolong masukkan query dan valuenya")

        query_mapping = {
            "pong": "STRING_PONG",
            "owner": "STRING_OWNER",
            "ubot": "STRING_UBOT",
            "devs": "STRING_DEVS",
        }

        command = message.command[0]
        mapping = message.command[1]
        value = " ".join(message.command[2:])

        if mapping.lower() in query_mapping:
            if value.lower() == "none":
                value = False
            query_var = query_mapping[mapping.lower()]
            await set_vars(client.me.id, query_var, value)
            await msg.edit(
                f"{brhsl}text berhasil di setting ke: {value}"
            )
        else:
            await msg.edit(f"{ggl}mapping tidak ditemukan")

    except Exception as error:
        await msg.edit(str(error))

@PY.UBOT("lihatemoji")
async def extract_emoji(client, message):
    try:
        if not message.reply_to_message:
            return await message.reply_text("Please reply to a message to extract custom emoji IDs.")
        
        custom_emoji_ids = [entity.custom_emoji_id for entity in message.reply_to_message.entities]
        emojis = extract_emojis_from_entities(message.reply_to_message)
        
        formatted_emojis = "".join([f"<emoji id={emoji_id}>{emoji}</emoji>" if emoji_id is not None else emoji for emoji_id, emoji in zip(custom_emoji_ids, emojis)])
        
        await message.reply_text(f"{formatted_emojis}", parse_mode=ParseMode.DISABLED)
    
    except Exception as e:
        await message.reply_text(str(e))
