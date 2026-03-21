import requests
from pyrogram import *
from AunuUbot import *
from pyrogram.types import *
import wget
import os
import glob

__MODULE__ = "ᴄᴏᴜᴘʟᴇ"
__HELP__ = """
<blockquote><b>『 ᴄᴏᴜᴘʟᴇ 』</b>

  <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}couple</code> <b>ᴊᴜᴍʟᴀʜ/ᴋᴀᴛᴀ_ᴋᴜɴᴄɪ</b> 
   <i>penjelasan:</b> untuk mencari photo couple secara random</i></blockquote>
"""

@PY.UBOT("couple")
async def pinterest(client, message):
    prs = await EMO.PROSES(client)
    err = await EMO.GAGAL(client)
    jalan = await message.reply(f"{prs}<b>ᴘʀᴏᴄᴇssɪɴɢ...</b>")
    chat_id = message.chat.id
    url = "https://api.botcahx.eu.org/api/randomgambar/couplepp?apikey=ApiKhususWannAza"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        male_url = data['result']['male']
        female_url = data['result']['female']

        # Download images using wget
        male_image_filename = wget.download(male_url, out="male.jpg")
        female_image_filename = wget.download(female_url, out="female.jpg")

        # Prepare media group
        media_group = [
            InputMediaPhoto(media=male_image_filename),
            InputMediaPhoto(media=female_image_filename)
        ]

        # Send media group
        janda = await client.send_media_group(chat_id, media_group)
        if janda:
            await jalan.delete()
        # Clean up downloaded files
        os.remove(male_image_filename)
        os.remove(female_image_filename)
    else:
        await message.reply(f"Request failed with status code {response.status_code}")
