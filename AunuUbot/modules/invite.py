import asyncio

from pyrogram.enums import UserStatus

from AunuUbot import *

__MODULE__ = "ɪɴᴠɪᴛᴇ"
__HELP__ = """
<blockquote>Bantuan Untuk Invite

perintah : <code>{0}invite</code> [username]
    mengundang anggota ke group</blockquote>
"""


@PY.UBOT("invite")
@PY.TOP_CMD
@PY.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    mg = await message.reply(f"{prs}menambahkan pengguna!")
    if len(message.command) < 2:
        return await mg.delete()
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit(
            f"{ktrng}beri saya pengguna untuk ditambahkan!\nperiksa menu bantuan untuk info lebih lanjut!"
        )
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except Exception as e:
        return await mg.edit(f"{e}")
    await mg.edit(f"{brhsl}berhasil ditambahkan {len(user_list)} ke grup ini")



# invite_id = []


# @PY.UBOT("inviteall")
#@PY.TOP_CMD
# @PY.GROUP
# async def _(client, message):
    # prs = await EMO.PROSES(client)
    # brhsl = await EMO.BERHASIL(client)
    # ggl = await EMO.GAGAL(client)
    # ktrng = await EMO.BL_KETERANGAN(client)
    # Tm = await message.reply(f"{prs}processing . . .")
    # if len(message.command) < 3:
        # await message.delete()
        # return await Tm.delete()
    # try:
        # chat = await client.get_chat(message.command[1])
    # except Exception as error:
        # return await Tm.edit(error)
    # if message.chat.id in invite_id:
        # return await Tm.edit_text(
            # f"{ktrng}sedang menginvite member silahkan coba lagi nanti atau gunakan perintah : cancel"
        # )
    # else:
        # done = 0
        # failed = 0
        # invite_id.append(message.chat.id)
        # await Tm.edit_text(f"{prs}mengundang anggota dari {chat.title}")
        # async for member in client.get_chat_members(chat.id):
            # stats = [
                # UserStatus.ONLINE,
                # UserStatus.OFFLINE,
                # UserStatus.RECENTLY,
                # UserStatus.LAST_WEEK,
            # ]
            # if member.user.status in stats:
                # try:
                    # await client.add_chat_members(message.chat.id, member.user.id)
                    # done = done + 1
                    # await asyncio.sleep(int(message.command[2]))
                # except Exception:
                    # failed = failed + 1
                    # await asyncio.sleep(int(message.command[2]))
        # invite_id.remove(message.chat.id)
        # await Tm.delete()
        # return await message.reply(
            # f"""
# {ggl}{done} anggota yang berhasil diundang
# {brhsl}{failed} anggota yang gagal diundang
# """
        # )


# @PY.UBOT("cancel")
#@PY.TOP_CMD
# @PY.GROUP
# async def _(client, message):
    # brhsl = await EMO.BERHASIL(client)
    # if message.chat.id not in invite_id:
        # return await message.reply_text(
            # f"sedang tidak ada perintah : inviteall"
        # )
    # try:
        # invite_id.remove(message.chat.id)
        # await message.reply_text("perintah : inviteall berhasil dibatalkan")
    # except Exception as e:
        # await message.reply_text(e)
