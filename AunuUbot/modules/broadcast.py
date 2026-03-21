import asyncio

from pyrogram.errors import FloodWait

from AunuUbot import *

__MODULE__ = "Broadcast"
__HELP__ = """
<blockquote><b>Bantuan Untuk Broadcast

perintah : <code>{0}gcast</code> [text/reply]
    broadcast ke group dan channel kecuali yang diblacklist

perintah : <code>{0}gcastpin</code> [reply]
    broadcast pin ke group dan channel kecuali blacklist</b></blockquote>
"""


async def _send_gcast(client, target_id, payload, pin=False):
    if hasattr(payload, "copy"):
        msg = await payload.copy(target_id)
    else:
        msg = await client.send_message(target_id, payload, disable_web_page_preview=True)
    if pin:
        try:
            await client.pin_chat_message(target_id, msg.id, disable_notification=True)
        except Exception:
            pass


async def _run_broadcast(client, message, pin=False):
    blacklist_ids = set(await get_user_ids(client.me.id))
    dialogs = await get_data_id(client, "global")
    if message.reply_to_message:
        payload = message.reply_to_message
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                f"<b>Gunakan <code>{message.text.split()[0]}</code> [text] atau reply pesan.</b>"
            )
        payload = message.text.split(None, 1)[1]

    status = await message.reply_text("<b>Broadcast sedang diproses...</b>")
    sent = 0
    failed = 0
    skipped = 0

    for target_id in dialogs:
        if target_id in blacklist_ids:
            skipped += 1
            continue
        try:
            await _send_gcast(client, target_id, payload, pin=pin)
            sent += 1
            await asyncio.sleep(1.2)
        except FloodWait as e:
            await asyncio.sleep(int(e.value) + 1)
            try:
                await _send_gcast(client, target_id, payload, pin=pin)
                sent += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1

    await status.edit(
        "<b>Broadcast selesai.</b>\n\n"
        f"Berhasil: <code>{sent}</code>\n"
        f"Gagal: <code>{failed}</code>\n"
        f"Blacklist: <code>{skipped}</code>"
    )


@PY.UBOT("gcast")
@PY.TOP_CMD
@PY.COOLDOWN(15, bucket="global")
async def _(client, message):
    await _run_broadcast(client, message, pin=False)


@PY.UBOT("gcastpin")
@PY.TOP_CMD
@PY.COOLDOWN(20, bucket="global")
async def _(client, message):
    await _run_broadcast(client, message, pin=True)
