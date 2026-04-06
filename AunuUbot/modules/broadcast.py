import asyncio

from pyrogram.errors import FloodWait
from pyrogram.enums import ChatType

from AunuUbot import *

__MODULE__ = "Broadcast"
__HELP__ = f"""
<blockquote><b>{Fonts.smallcap("bantuan untuk broadcast")}</b>

{Fonts.smallcap("perintah")} : <code>{{0}}gcast group [text/reply]</code>
    {Fonts.smallcap("broadcast ke group kecuali yang diblacklist")}

{Fonts.smallcap("perintah")} : <code>{{0}}gcast channels [text/reply]</code>
    {Fonts.smallcap("broadcast ke channel kecuali yang diblacklist")}

{Fonts.smallcap("perintah")} : <code>{{0}}gcast dm [text/reply]</code>
    {Fonts.smallcap("broadcast ke private chat")}

{Fonts.smallcap("perintah")} : <code>{{0}}gcastpin group/channels [reply]</code>
    {Fonts.smallcap("broadcast pin ke target yang dipilih sambil tetap mengikuti blacklist")}</blockquote>
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


def _extract_target_and_payload(message):
    parts = message.text.split(None, 2) if message.text else []
    target = parts[1].lower() if len(parts) > 1 else None
    payload = message.reply_to_message if message.reply_to_message else (parts[2] if len(parts) > 2 else None)
    return target, payload


async def _run_broadcast(client, message, pin=False):
    blacklist_ids = set(await get_user_ids(client.me.id))
    target, payload = _extract_target_and_payload(message)
    target_map = {
        "group": "group",
        "groups": "group",
        "channel": "global_channel_only",
        "channels": "global_channel_only",
        "dm": "users",
        "user": "users",
        "users": "users",
    }
    if target not in target_map:
        return await message.reply_text(
            "<b>Gunakan <code>{} group/channels/dm [text]</code> atau reply pesan.</b>".format(message.command[0])
        )
    if not payload:
        return await message.reply_text(
            "<b>Masukkan text broadcast atau reply pesan terlebih dahulu.</b>"
        )

    query_key = target_map[target]
    if query_key == "global_channel_only":
        dialogs = []
        async for dialog in client.get_dialogs():
            if dialog.chat.type == ChatType.CHANNEL:
                dialogs.append(dialog.chat.id)
    else:
        dialogs = await get_data_id(client, query_key)

    status = await message.reply_text("<b>Broadcast sedang diproses...</b>")
    sent = 0
    failed = 0
    skipped = 0

    for target_id in dialogs:
        if query_key != "users" and target_id in blacklist_ids:
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
        f"Target: <code>{target}</code>\n"
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
