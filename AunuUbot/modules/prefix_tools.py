import asyncio
import os
import tempfile

from pyrogram.errors import (
    FloodWait,
    PhotoCropSizeSmall,
    ImageProcessFailed,
    BadRequest,
)
from pyrogram.types import InputPhotoFileLocation
from pyrogram.raw import functions, types as raw_types

from AunuUbot import *

__MODULE__ = "ᴘʀᴇꜰɪx ᴄʟᴏɴᴇ"
__HELP__ = """
<blockquote><b>ᴘʀᴇꜰɪx ᴄʟᴏɴᴇ — ꜱᴀʟɪɴ ᴘʀᴏꜰɪʟ ᴛᴀʀɢᴇᴛ ᴋᴇ ᴀᴋᴜɴ ᴋᴀᴍᴜ

ᴘᴇʀɪɴᴛᴀʜ:
  <code>{0}pclone</code> — reply/tag seseorang untuk menyalin profilnya
  <code>{0}unpclone</code> — kembalikan profil asli kamu

ᴄᴀᴛᴀᴛᴀɴ:
  • Menyalin: nama depan, nama belakang, bio, dan foto profil
  • Profil asli disimpan otomatis sebelum disalin
  • Gunakan {0}unpclone untuk revert kapan saja</b></blockquote>

<b>AunuUbot</b>
"""

# ── helpers ──────────────────────────────────────────────────────────────────

BACKUP_QUERY = "prefix_clone_backup"


async def _get_target_user(client, message):
    """Resolve target dari reply atau mention/username/id di args."""
    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.from_user and not reply.from_user.is_bot:
            return reply.from_user
        if reply.from_user:
            return reply.from_user
        return None

    args = message.command
    if len(args) < 2:
        return None

    target_str = args[1]
    try:
        if target_str.lstrip("-").isdigit():
            return await client.get_users(int(target_str))
        return await client.get_users(target_str.lstrip("@"))
    except Exception:
        return None


async def _download_profile_photo(client, user_id: int) -> str | None:
    """Download foto profil user, return path file sementara atau None."""
    try:
        photos = []
        async for photo in client.get_chat_photos(user_id, limit=1):
            photos.append(photo)
        if not photos:
            return None
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.close()
        await client.download_media(photos[0], file_name=tmp.name)
        return tmp.name
    except Exception:
        return None


async def _backup_my_profile(client):
    """Simpan profil asli ke DB jika belum ada backup."""
    existing = await get_vars(client.me.id, "backed_up", BACKUP_QUERY)
    if existing:
        return  # sudah ada backup, jangan timpa

    me = await client.get_me()
    backup = {
        "first_name": me.first_name or "",
        "last_name": me.last_name or "",
        "bio": "",
        "has_photo": False,
    }

    # ambil bio via raw API
    try:
        full = await client.invoke(
            functions.users.GetFullUser(
                id=await client.resolve_peer("me")
            )
        )
        backup["bio"] = full.full_user.about or ""
    except Exception:
        pass

    # simpan foto profil asli ke file permanen
    photo_path = await _download_profile_photo(client, client.me.id)
    if photo_path:
        perm_path = os.path.join(
            tempfile.gettempdir(), f"pclone_backup_{client.me.id}.jpg"
        )
        os.replace(photo_path, perm_path)
        backup["has_photo"] = True
        backup["photo_path"] = perm_path

    await set_vars(client.me.id, "data", str(backup), BACKUP_QUERY)
    await set_vars(client.me.id, "backed_up", "1", BACKUP_QUERY)


async def _restore_my_profile(client):
    """Pulihkan profil dari backup DB."""
    raw_data = await get_vars(client.me.id, "data", BACKUP_QUERY)
    if not raw_data:
        return False

    import ast
    try:
        backup = ast.literal_eval(raw_data)
    except Exception:
        return False

    # restore nama
    try:
        await client.update_profile(
            first_name=backup.get("first_name", "") or ".",
            last_name=backup.get("last_name", ""),
            bio=backup.get("bio", ""),
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.update_profile(
            first_name=backup.get("first_name", "") or ".",
            last_name=backup.get("last_name", ""),
            bio=backup.get("bio", ""),
        )
    except Exception:
        pass

    # restore foto
    photo_path = backup.get("photo_path", "")
    if backup.get("has_photo") and photo_path and os.path.exists(photo_path):
        try:
            await client.set_profile_photo(photo=photo_path)
        except (PhotoCropSizeSmall, ImageProcessFailed, BadRequest):
            pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_profile_photo(photo=photo_path)
            except Exception:
                pass
        except Exception:
            pass
    elif not backup.get("has_photo"):
        # hapus semua foto profil jika aslinya memang tidak ada
        try:
            photos = [p async for p in client.get_chat_photos("me", limit=5)]
            if photos:
                await client.delete_profile_photos([p.file_id for p in photos])
        except Exception:
            pass

    # hapus backup dari DB
    await remove_vars(client.me.id, "data", BACKUP_QUERY)
    await remove_vars(client.me.id, "backed_up", BACKUP_QUERY)
    return True


async def _apply_profile(client, target_user):
    """Terapkan profil target ke akun client."""
    first_name = target_user.first_name or "."
    last_name = target_user.last_name or ""
    bio = ""

    # ambil bio target
    try:
        full = await client.invoke(
            functions.users.GetFullUser(
                id=await client.resolve_peer(target_user.id)
            )
        )
        bio = full.full_user.about or ""
    except Exception:
        pass

    # update nama & bio
    try:
        await client.update_profile(
            first_name=first_name,
            last_name=last_name,
            bio=bio,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.update_profile(
            first_name=first_name,
            last_name=last_name,
            bio=bio,
        )

    # download & set foto profil target
    photo_path = await _download_profile_photo(client, target_user.id)
    if photo_path:
        try:
            await client.set_profile_photo(photo=photo_path)
        except (PhotoCropSizeSmall, ImageProcessFailed, BadRequest):
            pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_profile_photo(photo=photo_path)
            except Exception:
                pass
        except Exception:
            pass
        finally:
            try:
                os.unlink(photo_path)
            except Exception:
                pass


# ── commands ─────────────────────────────────────────────────────────────────


@PY.UBOT("pclone|prefixclone")
@PY.TOP_CMD
async def prefix_clone_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)

    target = await _get_target_user(client, message)
    if not target:
        return await message.reply(
            f"<blockquote><b>{ggl} Reply atau sertakan username/id target!\n\n"
            f"Contoh: reply pesan seseorang lalu ketik <code>.pclone</code>\n\n"
            f"<b>AunuUbot</b></b></blockquote>"
        )

    proc = await message.reply(
        f"<blockquote><b>{prs} Menyimpan profil asli & menyalin profil "
        f"<a href='tg://user?id={target.id}'>{target.first_name}</a>...</b></blockquote>\n\n<b>AunuUbot</b>"
    )

    try:
        await _backup_my_profile(client)
        await _apply_profile(client, target)
    except FloodWait as e:
        return await proc.edit(
            f"<blockquote><b>{ggl} FloodWait {e.value}s, coba lagi nanti.</b></blockquote>\n\n<b>AunuUbot</b>"
        )
    except Exception as e:
        return await proc.edit(
            f"<blockquote><b>{ggl} Gagal: <code>{e}</code></b></blockquote>\n\n<b>AunuUbot</b>"
        )

    target_mention = f"<a href='tg://user?id={target.id}'>{target.first_name}</a>"
    await proc.edit(
        f"<blockquote><b>{sks} Profil berhasil disalin dari {target_mention}!\n\n"
        f"Gunakan <code>.unpclone</code> untuk mengembalikan profil asli.</b></blockquote>\n\n<b>AunuUbot</b>"
    )


@PY.UBOT("unpclone|unprefixclone")
@PY.TOP_CMD
async def unprefix_clone_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)

    backed_up = await get_vars(client.me.id, "backed_up", BACKUP_QUERY)
    if not backed_up:
        return await message.reply(
            f"<blockquote><b>{ggl} Tidak ada backup profil yang tersimpan.\n\n"
            f"Gunakan <code>.pclone</code> terlebih dahulu.</b></blockquote>\n\n<b>AunuUbot</b>"
        )

    proc = await message.reply(
        f"<blockquote><b>{prs} Mengembalikan profil asli...</b></blockquote>\n\n<b>AunuUbot</b>"
    )

    try:
        ok = await _restore_my_profile(client)
    except FloodWait as e:
        return await proc.edit(
            f"<blockquote><b>{ggl} FloodWait {e.value}s, coba lagi nanti.</b></blockquote>\n\n<b>AunuUbot</b>"
        )
    except Exception as e:
        return await proc.edit(
            f"<blockquote><b>{ggl} Gagal: <code>{e}</code></b></blockquote>\n\n<b>AunuUbot</b>"
        )

    if not ok:
        return await proc.edit(
            f"<blockquote><b>{ggl} Backup tidak ditemukan atau sudah dihapus.</b></blockquote>\n\n<b>AunuUbot</b>"
        )

    await proc.edit(
        f"<blockquote><b>{sks} Profil asli berhasil dipulihkan!</b></blockquote>\n\n<b>AunuUbot</b>"
    )
