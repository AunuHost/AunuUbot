from AunuUbot import *

__MODULE__ = "Blacklist"
__HELP__ = """
<blockquote><b>Bantuan Untuk Blacklist

perintah : <code>{0}addbl</code>
    memasukan group/channel ke daftar blacklist broadcast

perintah : <code>{0}delbl</code> / <code>{0}unbl</code>
    menghapus group/channel dari daftar blacklist

perintah : <code>{0}rallbl</code>
    menghapus semua daftar blacklist broadcast

perintah : <code>{0}listbl</code>
    memeriksa daftar blacklist broadcast</b></blockquote>
"""


async def _resolve_target_chat(client, message):
    if len(message.command) > 1:
        target = message.text.split(None, 1)[1].strip()
        chat = await client.get_chat(target)
        return chat.id, chat.title or chat.first_name or str(chat.id)
    return message.chat.id, message.chat.title or message.chat.first_name or str(message.chat.id)


@PY.UBOT("addbl")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    target_id, target_name = await _resolve_target_chat(client, message)
    blacklist_ids = await get_user_ids(client.me.id)
    if target_id in blacklist_ids:
        return await message.reply_text(
            f"<b>{target_name}</b> sudah ada di blacklist broadcast."
        )
    await add_user_id(client.me.id, target_id)
    await message.reply_text(
        f"<b>{target_name}</b> berhasil ditambahkan ke blacklist broadcast."
    )


@PY.UBOT("delbl|unbl")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    target_id, target_name = await _resolve_target_chat(client, message)
    blacklist_ids = await get_user_ids(client.me.id)
    if target_id not in blacklist_ids:
        return await message.reply_text(
            f"<b>{target_name}</b> tidak ada di blacklist broadcast."
        )
    await remove_user_id(client.me.id, target_id)
    await message.reply_text(
        f"<b>{target_name}</b> berhasil dihapus dari blacklist broadcast."
    )


@PY.UBOT("rallbl")
@PY.TOP_CMD
@PY.COOLDOWN(5)
async def _(client, message):
    await remove_all_user_ids(client.me.id)
    await message.reply_text("<b>Semua blacklist broadcast berhasil dihapus.</b>")


@PY.UBOT("listbl")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    blacklist_ids = await get_user_ids(client.me.id)
    if not blacklist_ids:
        return await message.reply_text("<b>Blacklist broadcast masih kosong.</b>")

    lines = []
    for index, chat_id in enumerate(blacklist_ids, start=1):
        try:
            chat = await client.get_chat(chat_id)
            name = chat.title or chat.first_name or str(chat_id)
        except Exception:
            name = str(chat_id)
        lines.append(f"{index}. {name} | <code>{chat_id}</code>")

    await message.reply_text(
        "<b>Daftar blacklist broadcast:</b>\n\n" + "\n".join(lines)
    )
