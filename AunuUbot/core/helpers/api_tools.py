import asyncio
import random
import requests

from pyrogram.enums import MessagesFilter

class API:
    async def wall(client):
        anime_channel = random.choice(["@animehikarixa", "@Anime_WallpapersHD"])
        animenya = [
            anime
            async for anime in client.search_messages(
                anime_channel, filter=MessagesFilter.PHOTO
            )
        ]
        return random.choice(animenya)

    def waifu():
        url = "https://www.waifu.im/search"
        response = requests.get(url)
        content = response.text
        start_index = content.find("var files = [") + len("var files = ")
        end_index = content.find("]", start_index)
        files_str = content[start_index:end_index]
        files = [file.strip('" ') for file in files_str.split(",")]
        return random.choice(files)