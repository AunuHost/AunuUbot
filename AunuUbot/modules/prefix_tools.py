from AunuUbot import *

__MODULE__ = "Prefix"
__HELP__ = """
<blockquote><b>Bantuan Untuk Prefix

perintah : <code>{0}setprefix</code> [prefix1 prefix2 ...]
    mengatur satu atau beberapa prefix userbot

perintah : <code>{0}getprefix</code>
    melihat prefix aktif

perintah : <code>{0}delprefix</code> / <code>{0}resetprefix</code>
    mengembalikan prefix ke default</b></blockquote>
"""


def _normalize_prefixes(raw_args):
    prefixes = []
    for item in raw_args:
        item = item.strip()
        if not item:
            continue
        if len(item) > 3:
            raise ValueError("Prefix maksimal 3 karakter.")
        if item not in prefixes:
            prefixes.append(item)
    if not prefixes:
        raise ValueError("Masukkan minimal 1 prefix.")
    if len(prefixes) > 5:
        raise ValueError("Maksimal 5 prefix.")
    return prefixes


@PY.UBOT("setprefix")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Gunakan: <code>setprefix . ! ?</code></b>")
    try:
        prefixes = _normalize_prefixes(message.command[1:])
    except ValueError as error:
        return await message.reply_text(f"<b>{error}</b>")

    await set_pref(client.me.id, prefixes)
    ubot.set_prefix(client.me.id, prefixes)
    await message.reply_text(
        "<b>Prefix berhasil diubah:</b> <code>{}</code>".format(" ".join(prefixes))
    )


@PY.UBOT("getprefix")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    prefixes = await ubot.get_prefix(client.me.id)
    await message.reply_text(
        "<b>Prefix aktif:</b> <code>{}</code>".format(" ".join(prefixes))
    )


@PY.UBOT("delprefix|resetprefix")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    await rem_pref(client.me.id)
    ubot.set_prefix(client.me.id, ["."])
    await message.reply_text("<b>Prefix berhasil direset ke default:</b> <code>.</code>")
