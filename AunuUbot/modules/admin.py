import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    ChatNotModified,
)

from AunuUbot import *


__MODULE__ = "ᴀᴅᴍɪɴ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Admin

perintah : <code>{0}kick</code> |<code>{0}ban</code> |<code>{0}mute</code> |<code>{0}etmin</code> |<code>{0}ceo</code> |<code>{0}demote</code>
    <code>{0}unmute</code> |<code>{0}unban</code>

perintah : <code>{0}zombies</code> [in group]
    mengeluarkan akun terhapus dari group

perintah : <code>{0}lock</code> | <code>{0}unlock</code> | <code>{0}locks</code>
    mengunci/membuka dan list izin group

example:
    |<code>{0}lock msg</code> |<code>{0}lock media</code> |<code>{0}lock pin</code>
    |<code>{0}lock polls</code> |<code>{0}lock info</code> |<code>{0}lock invite</code>
    |<code>{0}lock webprev</code> |<code>{0}lock stickers</code></b></blockquote>
"""


data = {
    "msg": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}


async def current_chat_permissions(client, chat_id):
    perms = []
    perm = (await client.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")
    return perms


async def tg_lock(
    client,
    message,
    parameter,
    permissions: list,
    perm: str,
    lock: bool,
):
    if lock:
        if perm not in permissions:
            return await message.reply(f"`{parameter}` ꜱudah terkunci")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.reply(f"`{parameter}` ꜱudah terbuka")
        permissions.append(perm)
    permissions = {perm: True for perm in set(permissions)}
    try:
        await client.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.reply(
            f"{message.text.split()[0]} [type]"
        )
    except ChatAdminRequired:
        return await message.reply("tidak mempunyai izin")
    await message.reply(
        (
            f"terkunci untuk non-admin!\ntipe: {parameter}\ngrup: {message.chat.title}"
            if lock
            else f"terbuka untuk non-admin!\ntipe: {parameter}\ngrup: {message.chat.title}"
        )
    )


@PY.UBOT("lock|unlock")
@PY.TOP_CMD
@PY.GROUP
async def _(client, message):
    if len(message.command) != 2:
        return await message.reply(f"{message.text.split()[0]} [type]")
    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()
    if parameter not in data and parameter != "all":
        return await message.reply(incorrect_parameters)
    permissions = await current_chat_permissions(client, chat_id)
    if parameter in data:
        await tg_lock(
            client,
            message,
            parameter,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        try:
            await client.set_chat_permissions(chat_id, ChatPermissions())
            await message.reply(
                f"terkunci untuk non-admin!\ntipe: {parameter}\ngrup: {message.chat.title}"
            )
        except ChatAdminRequired:
            return await message.reply("tidak mempunyai izin")
        except ChatNotModified:
            return await message.reply(
                f"terkunci untuk non-admin!\ntipe: {parameter}\ngrup: {message.chat.title}"
            )
    elif parameter == "all" and state == "unlock":
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
        except ChatAdminRequired:
            return await message.reply("tidak mempunyai izin")
        await message.reply(
            f"terbuka untuk non-admin!\ntipe: {parameter}\ngrup: {message.chat.title}"
        )


@PY.UBOT("locks")
@PY.TOP_CMD
@PY.GROUP
async def _(client, message):
    permissions = await current_chat_permissions(client, message.chat.id)
    if not permissions:
        return await message.reply("terkunci untuk ꜱemua")

    perms = " -> __**" + "\n -> __**".join(permissions) + "**__"
    await message.reply(perms)


@PY.UBOT("kick|ban|mute|unmute|unban")
@PY.TOP_CMD
@PY.GROUP
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    tion = await EMO.MENTION(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    if message.command[0] == "kick":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"{ggl}{message.text.split()[0]} [username/user_id/reply]")
        if user_id == OWNER_ID:
            return await message.reply_text(f"{ggl}anda tidak bisa menendang anggota ini")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                f"{ggl}saya tidak bisa menendang admin"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_kick = f"""
<blockquote>{bcs}ᴡᴀʀɴɪɴɢ: {mention}
{tion}ᴀᴅᴍɪɴ: {message.from_user.mention}
{ktrng}ᴀʟᴀꜱᴀɴ: {reason}</blockquote>

<b>-- USERBOT 15K/BULAN BY {USER_GROUP} --</b>
            """
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg_kick)
            await asyncio.sleep(1)
            await message.chat.unban_member(user_id)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "ban":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"{ggl}{message.text.split()[0]} [username/user_id/reply]")
        if user_id == OWNER_ID:
            return await message.reply_text(f"{ggl}anda tidak bisa membanned anggota ini")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                f"{ggl}saya tidak bisa membanned admin"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_ban = f"""
<blockquote>{bcs}ᴡᴀʀɴɪɴɢ: {mention}
{tion}ᴀᴅᴍɪɴ: {message.from_user.mention}
{ktrng}ᴀʟᴀꜱᴀɴ: {reason}</blockquote>

<b>-- USERBOT 15K/BULAN BY {USER_GROUP} --</b>
            """
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg_ban)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "mute":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"{ggl}{message.text.split()[0]} [username/user_id/reply]")
        if user_id == OWNER_ID:
            return await message.reply_text(f"{ggl}anda tidak bisa membisukan anggota ini")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                f"<blockquote>{ggl}saya tidak bisa membisukan admin</blockquote>\n\n<b>-- USERBOT 15K/BULAN BY {USER_GROUP} --</b>"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_mute = f"""
<blockquote>{bcs}ᴡᴀʀɴɪɴɢ: {mention}
{tion}ᴀᴅᴍɪɴ: {message.from_user.mention}
{ktrng}ᴀʟᴀꜱᴀɴ: {reason}</blockquote>

<b>-- USERBOT 15K/BULAN BY {USER_GROUP} --</b>
            """
        try:
            await message.chat.restrict_member(user_id, ChatPermissions())
            await message.reply(msg_mute)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unmute":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text(f"{ggl}{message.text.split()[0]} [username/user_id/reply]")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"{brhsl}{mention} sudah bisa chat lagi")
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unban":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text(f"{ggl}{message.text.split()[0]} [username/user_id/reply]")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<blockquote><b>{brhsl}{mention} sudah bisa join lagi</b><blockquote>\n\n<b>-- USERBOT 15K/BULAN BY {USER_GROUP} --</b>")
        except Exception as error:
            await message.reply(error)


@PY.UBOT("zombies")
@PY.TOP_CMD
@PY.GROUP
async def _(client, message):
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    Tm = await message.reply("sedang memeriksa")
    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                banned_users += 1
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
        await Tm.edit(f"<blockquote><b>{brhsl}berhasil mengeluarkan {banned_users} akun terhapus</b></blockquote>\n\n<b>-- USERBOT 15K/BULAN BY {USER_GROUP} --</b>")
    else:
        await Tm.edit(f"<blockquote><b>{ggl}tidak ada akun terhapus di group ini</b></blockquote>\n\n<b>-- USERBOT 15K/BULAN BY {USER_GROUP} --</b>")
