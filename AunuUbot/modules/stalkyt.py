import requests
import wget
import os
from pyrogram import Client
from AunuUbot import *

__MODULE__ = "sᴛᴀʟᴋʏᴛ"
__HELP__ = """
<blockquote><b>『 sᴛᴀʟᴋʏᴛ 』</b>

  <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}stalkyt</code> 
   <i>penjelasan:</i> untuk stalk yt menggunakan username</i></blockquote>
"""

@PY.UBOT("stalkyt")
async def stalkyt(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    
    jalan = await message.reply(f"{prs} Processing...")
    
    if len(message.command) != 2:
        return await jalan.edit(f"{ggl} Please use the command `stalkyt` followed by the yt username.")
    
    username = message.command[1]
    chat_id = message.chat.id
    url = f"https://widipe.com/download/youtubestalk?text={username}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'data' in data['result'] and len(data['result']['data']) > 0:
                first_channel = data['result']['data'][0]
                photoUrl = first_channel['avatar']
                description = first_channel.get('description', 'no desk')
                caption = f"""
<blockquote><b>Channel Name:</b> <code>{first_channel['channelName']}</code>
<b>Subscribers:</b> <code>{first_channel['subscriberH']}</code>
<b>Description:</b> <code>{description}</code>
<b>Url:</b> <code>{first_channel['url']}</code></blockquote>
"""
                photo_path = wget.download(photoUrl)
                await client.send_photo(chat_id, caption=caption, photo=photo_path)
                if os.path.exists(photo_path):
                    os.remove(photo_path)
                
                await jalan.delete()
            else:
                await jalan.edit(f"{ggl} No channel data found.")
        else:
            await jalan.edit(f"{ggl} Failed to retrieve data. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        await jalan.edit(f"{ggl} Request failed: {e}")
    
    except Exception as e:
        await jalan.edit(f"{ggl} An error occurred: {e}")
