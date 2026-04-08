import asyncio

from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait

from AunuUbot import *

sc = Fonts.smallcap

__MODULE__ = sc("broadcast")
__HELP__ = f"""
<blockquote><b>[9] {sc("broadcast center")}</b>

<code>{{0}}gcast group [text/reply]</code>
{sc("broadcast ke semua group kecuali yang diblacklist")}

<code>{{0}}gcast channels [text/reply]</code>
{sc("broadcast ke semua channel kecuali yang diblacklist")}

<code>{{0}}gcast dm [text/reply]</code>
{sc("broadcast ke semua private chat")}

<code>{{0}}gcastpin group [reply]</code>
<code>{{0}}gcastpin channels [reply]</code>
{sc("broadcast pin ke target yang dipilih dan tetap menghormati blacklist")}</blockquote>
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


def _status_card(title, target, sent, failed, skipped):
    return (
        f"<blockquote><b>[9] {title}</b></blockquote>\n"
        f"<blockquote>target: <code>{target}</code>\n"
        f"berhasil: <code>{sent}</code>\n"
        f"gagal: <code>{failed}</code>\n"
        f"blacklist: <code>{skipped}</code></blockquote>\n"
        f"<blockquote><b>[9] {sc('broadcast report')}</b></blockquote>"
    )


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
            f"<blockquote><b>{sc('gunakan')}:</b>\n"
            f"<code>{message.command[0]} group text</code>\n"
            f"<code>{message.command[0]} channels text</code>\n"
            f"<code>{message.command[0]} dm text</code></blockquote>"
        )
    if not payload:
        return await message.reply_text(
            f"<blockquote><b>{sc('masukkan text broadcast atau reply pesan terlebih dahulu')}.</b></blockquote>"
        )

    query_key = target_map[target]
    if query_key == "global_channel_only":
        dialogs = []
        async for dialog in client.get_dialogs():
            if dialog.chat.type == ChatType.CHANNEL:
                dialogs.append(dialog.chat.id)
    else:
        dialogs = await get_data_id(client, query_key)

    status = await message.reply_text(
        f"<blockquote><b>[9] {sc('broadcast sedang diproses')}...</b></blockquote>"
    )
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

    title = sc("broadcast pin selesai") if pin else sc("broadcast selesai")
    await status.edit(_status_card(title, target, sent, failed, skipped))


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
