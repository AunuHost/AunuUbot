import asyncio
from functools import partial

from yt_dlp import YoutubeDL
from AunuUbot.config import USER_GROUP


async def run_sync(func, *args, **kwargs):
    # ponytail: get_event_loop() deprecated 3.12+; use get_running_loop() inside async context
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))


async def YoutubeDownload(url, as_video=False):
    if as_video:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "cookiefile": "cookies.txt",
        }
    else:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "cookiefile": "cookies.txt",
        }
    data_ytp = (
        "<emoji id=6005994005148471369>💡</emoji> informasi {}\n\n"
        "<emoji id=5904544038643569182>🏷</emoji> nama: {}\n"
        "<emoji id=6030547358222127917>🧭</emoji> durasi: {}\n"
        "<emoji id=5233246225146332642>👀</emoji> dlihat: {}\n"
        "<emoji id=6005896024059547548>📢</emoji> channel: {}\n"
        "<emoji id=6005993794695076239>🔗</emoji> tautan: <a href={}>youtube</a>\n\n"
        f"<b>-- USERBOT 15K/BULAN BY {USER_GROUP} --</b>\n"
        "<b>AunuUbot</b>"
    )
    ydl = YoutubeDL(ydl_opts)
    ytdl_data = await run_sync(ydl.extract_info, url, download=True)
    file_name = ydl.prepare_filename(ytdl_data)
    videoid = ytdl_data.get("id", "")
    title = ytdl_data.get("title", "Unknown")
    url = f"https://youtu.be/{videoid}"
    duration = ytdl_data.get("duration") or 0
    channel = ytdl_data.get("uploader") or "Unknown"
    view_count = ytdl_data.get("view_count") or 0
    views = f"{view_count:,}".replace(",", ".")
    thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    return file_name, title, url, duration, views, channel, thumb, data_ytp
