import asyncio
import os

from pyrogram.enums import MessageMediaType, MessagesFilter
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import InputMediaPhoto

from AunuUbot import *

__MODULE__ = "ᴄᴏɴᴠᴇʀᴛ"
__HELP__ = """
<blockquote>Bantuan Untuk Clnvert

perintah : <code>{0}toanime</code>
    untuk merubah photo/sticker/gif menjadi gambar anime
  
perintah : <code>{0}toimg</code>
    untuk merubah sticker/gif menjadi photo
  
perintah : <code>{0}tosticker</code>
    untuk merubah foto menjadi sticker
  
perintah : <code>{0}togif</code>
    untuk merubah sticker menjadi gif
  
perintah : <code>{0}toaudio</code>
    untuk merubah video menjadi audio mp3</blockquote>
"""



@PY.UBOT("toanime")
@PY.TOP_CMD
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    Tm = await message.reply(f"{prs}tunggu sebentar...")
    if message.reply_to_message:
        if len(message.command) < 2:
            if message.reply_to_message.photo:
                file = "foto"
                get_photo = message.reply_to_message.photo.file_id
            elif message.reply_to_message.sticker:
                file = "sticker"
                get_photo = await dl_pic(client, message.reply_to_message)
            elif message.reply_to_message.animation:
                file = "gift"
                get_photo = await dl_pic(client, message.reply_to_message)
            else:
                return await Tm.edit(
                    f"{ggl}mohon balas ke photo/striker/git"
                )
        else:
            if message.command[1] in ["foto", "profil", "photo"]:
                chat = (
                    message.reply_to_message.from_user
                    or message.reply_to_message.sender_chat
                )
                file = "foto profil"
                get = await client.get_chat(chat.id)
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
    else:
        if len(message.command) < 2:
            return await Tm.edit(
                f"{ggl}balas ke foto dan saya akan merubah foto anda menjadi anime"
            )
        else:
            try:
                file = "foto"
                get = await client.get_chat(message.command[1])
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
            except Exception as error:
                return await Tm.edit(error)
    await Tm.edit("proceꜱꜱing...")
    await client.unblock_user("@qq_neural_anime_bot")
    send_photo = await client.send_photo("@qq_neural_anime_bot", get_photo)
    await asyncio.sleep(30)
    await send_photo.delete()
    await Tm.delete()
    info = await client.resolve_peer("@qq_neural_anime_bot")
    anime_photo = []
    async for anime in client.search_messages(
        "@qq_neural_anime_bot", filter=MessagesFilter.PHOTO
    ):
        anime_photo.append(
            InputMediaPhoto(
                anime.photo.file_id, caption=f"{brhsl}powered by: {bot.me.mention}"
            )
        )
    if anime_photo:
        await client.send_media_group(
            message.chat.id,
            anime_photo,
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))

    else:
        await client.send_message(
            message.chat.id,
            f"{ggl}gagal merubah {file} menjadi gambar anime",
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))


@PY.UBOT("toimg")
@PY.TOP_CMD
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    _msg = f"{prs}proceꜱꜱing..."
    Tm = await message.reply(_msg)
  
    try:
        file_io = await dl_pic(client, message.reply_to_message)
        file_io.name = "sticker.png"
        await client.send_photo(
            message.chat.id,
            file_io,
            reply_to_message_id=message.id,
        )
        await Tm.delete()
    except Exception as e:
        await Tm.delete()
        return await client.send_message(
            message.chat.id,
            e,
            reply_to_message_id=message.id,
        )


@PY.UBOT("tosticker")
@PY.TOP_CMD
async def _(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            return await message.reply_text("reply ke foto untuk mengubah ke sticker")
        sticker = await client.download_media(
            message.reply_to_message.photo.file_id,
            f"sticker_{message.from_user.id}.webp",
        )
        await message.reply_sticker(sticker)
        os.remove(sticker)
    except Exception as e:
        await message.reply_text(str(e))


@PY.UBOT("togif")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    TM = await message.reply(f"{prs}proceꜱꜱing...")
    if not message.reply_to_message.sticker:
        return await TM.edit(f"{ggl}balas ke stiker...")
    await TM.edit(f"{prs}downloading sticker. . .")
    file = await client.download_media(
        message.reply_to_message,
        f"Gift_{message.from_user.id}.mp4",
    )
    try:
        await client.send_animation(
            message.chat.id, file, reply_to_message_id=message.id
        )
        os.remove(file)
        await TM.delete()
    except Exception as error:
        await TM.edit(error)


@PY.UBOT("toaudio")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    replied = message.reply_to_message
    Tm = await message.reply(f"{prs}tunggu sebentar")
    if not replied:
        return await Tm.edit(f"{ggl}mohon balas ke video")
    if replied.media == MessageMediaType.VIDEO:
        await Tm.edit(f"{prs}downloading video . . ..")
        file = await client.download_media(
            message=replied,
            file_name=f"toaudio_{replied.id}",
        )
        out_file = f"{file}.mp3"
        try:
            await Tm.edit(f"{ktrng}mencoba ekstrak audio. ..")
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await run_cmd(cmd)
            await Tm.edit(f"{brhsl}uploading audio . . .")
            await client.send_voice(
                message.chat.id,
                voice=out_file,
                reply_to_message_id=message.id,
            )
            os.remove(file)
            await Tm.delete()
        except Exception as error:
            await Tm.edit(error)
    else:
        return await Tm.edit(f"{ggl}mohon balas ke video")


@PY.UBOT("colong")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    dia = message.reply_to_message
    if not dia:
        return await message.reply(f"{ggl}mohon balas ke media")
    anjing = dia.caption or ""
    Tm = await message.reply(f"{prs}processing...")
    if dia.photo:
        if message.reply_to_message.photo.file_size > 10000000:
            return await Tm.edit(f"{ktrng}file di atas 10mb tidak di izinkan")
        anu = await client.download_media(dia)
        await client.send_photo(client.me.id, anu, anjing)
        os.remove(anu)
        await message.delete()
        return await Tm.delete()
    if dia.video:
        if message.reply_to_message.video.file_size > 10000000:
            return await Tm.edit(f"{ktrng}file di atas 10mb tidak di izinkan")
        anu = await client.download_media(dia)
        await client.send_video(client.me.id, anu, anjing)
        os.remove(anu)
        await message.delete()
        return await Tm.delete()
    if dia.audio:
        if message.reply_to_message.audio.file_size > 10000000:
            return await Tm.edit(f"{ktrng}file di atas 10mb tidak di izinkan")
        anu = await client.download_media(dia)
        await client.send_audio(client.me.id, anu, anjing)
        os.remove(anu)
        await message.delete()
        return await Tm.delete()
    if dia.voice:
        if message.reply_to_message.voice.file_size > 10000000:
            return await Tm.edit(f"{ktrng}file di atas 10mb tidak di izinkan")
        anu = await client.download_media(dia)
        await client.send_voice(client.me.id, anu, anjing)
        os.remove(anu)
        await message.delete()
        return await Tm.delete()
    if dia.document:
        if message.reply_to_message.document.file_size > 10000000:
            return await Tm.edit(f"{ktrng}file di atas 10mb tidak di izinkan")
        anu = await client.download_media(dia)
        await client.send_document(client.me.id, anu, anjing)
        os.remove(anu)
        await message.delete()
        return await Tm.delete()
    else:
        return await Tm.reply(f"{ggl}sepertinya terjadi kesalahan")
