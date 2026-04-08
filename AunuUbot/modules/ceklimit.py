from pyrogram.raw.functions.messages import StartBot

from AunuUbot import *

sc = Fonts.smallcap

__MODULE__ = sc("ceklimit")
__HELP__ = f"""
<blockquote><b>[9] {sc("limit checker")}</b>

<code>{{0}}ceklimit</code>
<code>{{0}}ceklimit @user</code>
<code>{{0}}ceklimit reply</code>
{sc("cek status akun melalui spambot. pemeriksaan tetap berjalan untuk akun session yang aktif")}</blockquote>
"""


@PY.UBOT("ceklimit")
@PY.TOP_CMD
async def ceklimit(client, message):
    target = await extract_user(message)
    if target and int(target) != int(client.me.id):
        return await message.reply_text(
            f"<blockquote><b>{sc('spambot hanya bisa mengecek akun session yang sedang aktif')}.</b>\n"
            f"{sc('command ini tetap akan mengecek akun kamu sendiri')}</blockquote>"
        )
    wait = await message.reply_text(
        f"<blockquote><b>{sc('menghubungi spambot')}...</b></blockquote>"
    )
    try:
        await client.unblock_user("SpamBot")
        peer = await client.resolve_peer("SpamBot")
        response = await client.invoke(
            StartBot(
                bot=peer,
                peer=peer,
                random_id=client.rnd_id(),
                start_param="start",
            )
        )
        await sleep(1.5)
        msg = await client.get_messages("SpamBot", response.updates[1].message.id + 1)
        text = (msg.text or "").strip()
        verdict = sc("aman")
        if "limited" in text.lower() or "cannot" in text.lower() or "sorry" in text.lower():
            verdict = sc("terbatas")
        card = (
            f"<blockquote><b>[9] {sc('spam bot check')}</b></blockquote>\n"
            f"<blockquote>akun: {client.me.mention}\n"
            f"status: <code>{verdict}</code>\n"
            f"premium: <code>{sc('ya') if client.me.is_premium else sc('tidak')}</code></blockquote>\n"
            f"<blockquote>{text or sc('tidak ada respon dari spambot')}</blockquote>\n"
            f"<blockquote><b>[9] {sc('limit diagnostics')}</b></blockquote>"
        )
        await wait.edit(card)
    except Exception as error:
        await wait.edit(
            f"<blockquote><b>{sc('gagal mengecek limit akun')}.</b>\n<code>{error}</code></blockquote>"
        )
