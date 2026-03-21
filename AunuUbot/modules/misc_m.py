import asyncio
import os
import requests

from asyncio import sleep
from pyrogram.raw.functions.messages import DeleteHistory, StartBot

from bs4 import BeautifulSoup
from io import BytesIO

from telegraph import Telegraph, exceptions, upload_file

from AunuUbot import *



__MODULE__ = "ᴍɪꜱᴄ"
__HELP__ = """
<blockquote>Bantuan Untuk Misc

perintah : <code>{0}limit</code>
    mengecek status akun apakah terkena limit atau tidak

perintah : <code>{0}carbon</code>
    membuat text carbonara

perintah : <code>{0}qrGen</code>
    merubah qrcode text menjadi gambar

perintah : <code>{0}qrRead</code>
    merubah qrcode media menjadi text:

perintah : <code>{0}tg</code>
    mengapload media/text ke telegra.ph

perintah : <code>{0}font</code>
    merubah text menjadi berbeda</blockquote>
"""


@PY.UBOT("limit")
@PY.TOP_CMD
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    pong = await EMO.PING(client)
    tion = await EMO.MENTION(client)
    yubot = await EMO.UBOT(client)
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    msg = await message.reply(f"{prs}processing . . .")
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    await msg.delete()
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1) 
    if status and hasattr(status, "text"):
        pjg = len(status.text)
        print(pjg)
        if pjg <= 100:
            if client.me.is_premium:
                text = f"""
{pong} status akun premium : true {sks}
{tion} limit check : akun anda tidak dibatasi {sks}
{yubot} ubot : {bot.me.mention}
"""
            else:
                text = f"""
status akun : beli prem dulu ya
limit check : akun anda tidak di batasi
ubot : {bot.me.mention}
"""
            await client.send_message(message.chat.id, text)
            return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
        else:
            if client.me.is_premium:
                text = f"""
{pong} status akun premium : true
{tion} limit check : akun anda bermasalah{ggl} 
{yubot} ubot : {bot.me.mention}
"""
            else:
                text = f"""
status akun : beli prem dulu ya
limit check : akun anda bermasalah
ubot : {bot.me.mention}
"""
            await client.send_message(message.chat.id, text)
            return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
    else:
        print("Status tidak valid atau status.text tidak ada")

async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@PY.UBOT("carbon")
@PY.TOP_CMD
async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await message.reply("memproꜱeꜱ...")
    carbon = await make_carbon(text)
    await ex.edit("uploading...")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"carboniꜱed by :{client.me.mention}",
        ),
    )
    carbon.close()


def qr_gen(content):
    return {
        "data": content,
        "config": {
            "body": "circle-zebra",
            "eye": "frame13",
            "eyeBall": "ball14",
            "erf1": [],
            "erf2": [],
            "erf3": [],
            "brf1": [],
            "brf2": [],
            "brf3": [],
            "bodyColor": "#000000",
            "bgColor": "#FFFFFF",
            "eye1Color": "#000000",
            "eye2Color": "#000000",
            "eye3Color": "#000000",
            "eyeBall1Color": "#000000",
            "eyeBall2Color": "#000000",
            "eyeBall3Color": "#000000",
            "gradientColor1": "",
            "gradientColor2": "",
            "gradientType": "linear",
            "gradientOnEyes": "true",
            "logo": "",
            "logoMode": "default",
        },
        "size": 1000,
        "download": "imageUrl",
        "file": "png",
    }


@PY.UBOT("qrgen")
@PY.TOP_CMD
async def _(client, message):
    ID = message.reply_to_message or message
    if message.reply_to_message:
        data = qr_gen(message.reply_to_message.text)
    else:
        if len(message.command) < 2:
            return await message.delete()
        else:
            data = qr_gen(message.text.split(None, 1)[1])
    Tm = await message.reply("sedang memproses buat qrcode....")
    try:
        QRcode = (
            requests.post(
                "https://api.qrcode-monkey.com//qr/custom",
                json=data,
            )
            .json()["imageUrl"]
            .replace("//api", "https://api")
        )
        await client.send_photo(message.chat.id, QRcode, reply_to_message_id=ID.id)
        await Tm.delete()
    except Exception as error:
        await Tm.edit(error)



@PY.UBOT("qrread")
@PY.TOP_CMD
async def _(client, message):
    replied = message.reply_to_message
    if not (replied and replied.media and (replied.photo or replied.sticker)):
        await message.reply("balas kode qr untuk mendapatkan data...")
        return
    if not os.path.isdir("premiumQR/"):
        os.makedirs("premiumQR/")
    AM = await message.reply("mengunduh media...")
    down_load = await client.download_media(message=replied, file_name="premiumQR/")
    await AM.edit("memproses kode qr anda...")
    cmd = [
        "curl",
        "-X",
        "POST",
        "-F",
        "f=@" + down_load + "",
        "https://zxing.org/w/decode",
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    out_response = stdout.decode().strip()
    err_response = stderr.decode().strip()
    os.remove(down_load)
    if not (out_response or err_response):
        await AM.edit("tidak bisa mendapatkan data kode qr ini...")
        return
    try:
        soup = BeautifulSoup(out_response, "html.parser")
        qr_contents = soup.find_all("pre")[0].text
    except IndexError:
        await AM.edit("indeks daftar di luar jangkauan")
        return
    await AM.edit(f"data qrcode:\n{qr_contents}")


@PY.UBOT("tg")
@PY.TOP_CMD
async def _(client, message):
    XD = await message.reply("sedang memproses . . .")
    if not message.reply_to_message:
        return await XD.edit(
            "mohon balas ke pesan, untuk mendapatkan link dari telegraph."
        )
    telegraph = Telegraph()
    if message.reply_to_message.media:
        m_d = await dl_pic(client, message.reply_to_message)
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            return await XD.edit(f"{exc}")
        U_done = f"berhasil diupload ke <a href='https://telegra.ph/{media_url[0]}'>telegraph</a>"
        await XD.edit(U_done)
    elif message.reply_to_message.text:
        page_title = f"{client.me.first_name} {client.me.last_name or ''}"
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            return await XD.edit(f"{exc}")
        wow_graph = f"berhasil diupload ke <a href='https://telegra.ph/{response['path']}'>telegraph</a>"
        await XD.edit(wow_graph)

  
@PY.UBOT("font")
@PY.TOP_CMD
async def _(client, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            query = id(message)
        else:
            return await message.reply("harap reply ke text")
    else:
        if len(message.command) < 2:
            return await message.reply(f"{message.text} [reply/text]")
        else:
            query = id(message)
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"get_font {query}")
        return await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        return await message.reply(error)


@PY.INLINE("^get_font")
async def _(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    buttons = InlineKeyboard(row_width=3)
    keyboard = []
    for X in query_fonts[0]:
        keyboard.append(
            InlineKeyboardButton(X, callback_data=f"get {get_id} {query_fonts[0][X]}")
        )
    buttons.add(*keyboard)
    buttons.row(InlineKeyboardButton("►", callback_data=f"next {get_id}"))
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get font!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(
                        "silahkan pilih salah satu font dibawah"
                    ),
                )
            )
        ],
    )


@PY.CALLBACK("^get")
async def _(client, callback_query):
    try:
        q = int(callback_query.data.split()[1])
        m = [obj for obj in get_objects() if id(obj) == q][0]
        new = str(callback_query.data.split()[2])
        if m.reply_to_message:
            text = m.reply_to_message.text
        else:
            text = m.text.split(None, 1)[1]
        get_new_font = gens_font(new, text)
        return await callback_query.edit_message_text(get_new_font)
    except Exception as error:
        return await callback_query.answer(f"Error: {error}", True)


@PY.CALLBACK("^next")
async def _(client, callback_query):
    try:
        get_id = int(callback_query.data.split()[1])
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in query_fonts[1]:
            keyboard.append(
                InlineKeyboardButton(
                    X, callback_data=f"get {get_id} {query_fonts[1][X]}"
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("◄", callback_data=f"prev {get_id}"))
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"Error: {error}", True)


@PY.CALLBACK("^prev")
async def _(client, callback_query):
    try:
        get_id = int(callback_query.data.split()[1])
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in query_fonts[0]:
            keyboard.append(
                InlineKeyboardButton(
                    X, callback_data=f"get {get_id} {query_fonts[0][X]}"
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("►", callback_data=f"next {get_id}"))
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)
