import requests
import wget
import os
from pyrogram import Client
from AunuUbot import *

__MODULE__ = "ᴄᴜᴀᴄᴀ"
__HELP__ = """
<blockquote><b>『 cuaca 』</b>

  <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}cuaca</code> 
   <i>penjelasan:</b> cek info cuaca di kota kota besar.</i></blockquote>
"""

@PY.UBOT("cuaca")
async def cuaca(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    
    jalan = await message.reply(f"{prs} Processing...")
    a = message.text.split(' ', 1)[1]
    chat_id = message.chat.id
    url = f"https://widipe.com/weather?text={a}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            hasil = data['result']
            location = hasil['location']
            country = hasil['country']
            weather = hasil['weather']
            currentTemp = hasil['currentTemp']
            maxTemp = hasil['maxTemp']
            minTemp = hasil['minTemp']
            humidity = hasil['humidity']
            windSpeed = hasil['windSpeed']
            photoUrl = f"https://telegra.ph//file/9354c197366cde09650fd.jpg"
            caption = f"""
<blockquote>╭─ �  「 <b>Info Cuaca Terkini</b> 」
│  ◦ <b>location: <code>{location}</code></b>
│  ◦ <b>country: <code>{country}</code></b>
│  ◦ <b>weather: <code>{weather}</code></b>
│  ◦ <b>currentTemp: <code>{currentTemp}</code></b>
│  ◦ <b>Temp: <code>{maxTemp}, {minTemp}</code></b>
│  ◦ <b>windSpeed: <code>{windSpeed}</code></b></blockquote>
╰──── �
"""
            photo_path = wget.download(photoUrl)
            await client.send_photo(chat_id, caption=caption, photo=photo_path)
            if os.path.exists(photo_path):
                os.remove(photo_path)
            
            await jalan.delete()
        else:
            await jalan.edit(f"{ggl} No 'result' key found in the response.")
    
    except requests.exceptions.RequestException as e:
        await jalan.edit(f"{ggl} Request failed: {e}")
    
    except Exception as e:
        await jalan.edit(f"{ggl} An error occurred: {e}")
