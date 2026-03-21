from pyrogram import *
from pyrogram import errors
from pyrogram import enums
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from AunuUbot import *

__MODULE__ = "ᴊᴏɪɴʟᴇᴀᴠᴇ"
__HELP__ = """
<blockquote>Bantuan Untuk Joinleave

perintah : <code>{0}kickme</code>
    keluar dari group telegram

perintah : <code>{0}join</code>
    join ke group melalui tautan atau username group

perintah : <code>{0}leaveallgc</code>
    keluar semua dari group telegram kecuali admin/owner

perintah : <code>{0}leaveallmute</code>
    keluar dari grup yang membatasi anda

perintah : <code>{0}leaveallch</code>
    kekuar semua dari channel kecuali admin/owner</blockquote>
"""


@PY.UBOT("kickme")
@PY.TOP_CMD
@PY.GROUP
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply(f"{prs}memproꜱeꜱ...")
    if message.chat.id in BLACKLIST_CHAT:
        return await xxnx.edit(f"{ggl}perintah ini dilarang digunakan di group ini")
    try:
        await xxnx.edit_text(f"{client.me.first_name} telah meninggalkan grup ini, bye!!{sks}")
        await client.leave_chat(Man)
    except Exception as ex:
        await xxnx.edit_text(f"{ggl}ERROR: \n\n{str(ex)}")



@PY.UBOT("join")
@PY.TOP_CMD
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply(f"{prs}memproꜱeꜱ...")
    try:
        await xxnx.edit(f"{sks}berhaꜱil bergabung ke chat id: {Man}")
        await client.join_chat(Man)
    except Exception as ex:
        await xxnx.edit(f"{ggl}ERROR: \n\n{str(ex)}")


@PY.UBOT("leaveallgc")
@PY.TOP_CMD
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    Man = await message.reply(f"{prs}global leave dari obrolan group...")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                member = await client.get_chat_member(chat, "me")
                if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                    done += 1
                    await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f"{sks}berhaꜱil keluar dari {done} group\n{ggl}gagal keluar dari {er} group"
    )


@PY.UBOT("leaveallch")
@PY.TOP_CMD
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    Man = await message.reply(f"{prs}global leave dari channel...")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.CHANNEL:
            chat = dialog.chat.id
            try:
                member = await client.get_chat_member(chat, "me")
                if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                    done += 1
                    await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f"{sks}berhaꜱil keluar dari {done} channel\n{ggl}gagal keluar dari {er} channel"
    )

@PY.UBOT("leaveallmute")
@PY.TOP_CMD
async def _(client, message):
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    done = 0
    Haku = await message.reply_text(f"{prs}proccesing...")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            chat_id = dialog.chat.id
            try:
                member = await client.get_chat_member(chat_id, "me")
                if member.status == ChatMemberStatus.RESTRICTED:
                    await client.leave_chat(chat_id)
                    done += 1
            except Exception:
                pass
    await Haku.edit(f"""
{sks}berhasil keluar dari : {done} grup yang telah membatasi kamu
""")
