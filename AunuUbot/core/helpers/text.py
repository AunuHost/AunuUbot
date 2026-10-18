from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AunuUbot import OWNER_ID, bot, ubot, get_expired_date


class MSG:
    def EXP_MSG_UBOT(X):
        return f"""
<blockquote><b>❏ ᴘᴇᴍʙᴇʀɪᴛᴀʜᴜᴀɴ</b>
<b>├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ɪᴅ:</b> <code>{X.me.id}</code>
<b>╰ ᴍᴀsᴀ ᴀᴋᴛɪꜰ ᴛᴇʟᴀʜ ʜᴀʙɪs</b></blockquote>

<b>AunuUbot</b>
"""

    def START(message):
        return f"""
<blockquote><b>👋🏻 ʜᴀʟᴏ <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>!

<b>💬 @{bot.me.username} ᴀᴅᴀʟᴀʜ ʙᴏᴛ ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ᴅᴇɴɢᴀɴ ᴍᴜᴅᴀʜ</b>

🚀 ꜱɪʟᴀʜᴋᴀɴ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ 
💬 ᴏᴡɴᴇʀ : <a href=tg://openmessage?user_id={OWNER_ID}>AunuXdev</a> 

ʟɪsᴛ ʜᴀʀɢᴀ & ᴋᴇʙᴜᴛᴜʜᴀɴ ᴜsᴇʀʙᴏᴛ :
<a href='https://t.me/AunuHostv'>ᴋᴇʙᴜᴛᴜʜᴀɴ ᴜsᴇʀʙᴏᴛ</a>

👉🏻 ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b></blockquote>

<b>AunuUbot</b>
"""

    def TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN):
        return f"""
<blockquote><b>❖ ᴘᴀʏᴍᴇɴᴛ ᴄᴇɴᴛᴇʀ ❖</b></blockquote>
<blockquote>🗓 ᴘᴀᴋᴇᴛ: <code>{BULAN} ʙᴜʟᴀɴ</code>
💸 ʜᴀʀɢᴀ ᴘᴇʀ ʙᴜʟᴀɴ: <code>ʀᴘ {HARGA}.000</code>
🧾 ᴛᴏᴛᴀʟ ᴘᴇᴍʙᴀʏᴀʀᴀɴ: <code>ʀᴘ {TOTAL_HARGA}.000</code></blockquote>

<blockquote><b>❖ ᴍᴇᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ❖</b>
├ ᴅᴀɴᴀ: <code>082328229523</code>
├ ɴᴀᴍᴀ: <code>dwiaunu</code>
├ ɢᴏᴘᴀʏ: <code>ʙᴇʟᴜᴍ ᴛᴇʀsᴇᴅɪᴀ</code>
╰ ǫʀɪs: <code>ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ</code></blockquote>

<blockquote>💬 ᴋᴏɴᴛᴀᴋ ᴏᴡɴᴇʀ: <a href=tg://openmessage?user_id={OWNER_ID}>AunuHostv</a>
📎 sᴇᴛᴇʟᴀʜ ᴛʀᴀɴsғᴇʀ, ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴғɪʀᴍᴀsɪ ᴅᴀɴ ᴋɪʀɪᴍ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ</blockquote>

<b>AunuUbot</b>
"""

    async def UBOT(count):
        return f"""
<blockquote><b>❏ ᴜsᴇʀʙᴏᴛ ᴋᴇ</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b> ├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 
<b> ╰ ɪᴅ:</b> <code>{ubot._ubot[int(count)].me.id}</code></blockquote>

<b>AunuUbot</b>
"""

    def POLICY():
        return """
ᴜɴᴛᴜᴋ ᴘᴇɴɢɢᴜɴᴀ ᴜsᴇʀʙᴏᴛ, ʟᴇʙɪʜ ᴀᴍᴀɴ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴀᴋᴜɴ ʏᴀɴɢ sᴜᴅᴀʜ ᴜsɪᴀ ᴅᴀɴ ᴘᴇᴍᴀᴋᴀɪᴀɴɴʏᴀ sᴛᴀʙɪʟ.
ʜɪɴᴅᴀʀɪ ᴀᴋᴜɴ ʙᴀʀᴜ ᴀᴛᴀᴜ ɪᴅ ᴀᴡᴀʟᴀɴ 0-5 ᴋᴀʀᴇɴᴀ ʟᴇʙɪʜ ʀᴀᴡᴀɴ sᴀᴀᴛ ᴅɪᴘᴀsᴀɴɢɪ ᴜsᴇʀʙᴏᴛ.
ᴀᴋᴜɴ ʟᴀᴍᴀ ᴀᴛᴀᴜ ɪᴅ ᴀᴡᴀʟᴀɴ 6-9 ʙɪᴀsᴀɴʏᴀ ʟᴇʙɪʜ sᴛᴀʙɪʟ, ᴛᴇᴛᴀᴘ sᴇᴍᴜᴀ ᴋᴇᴍʙᴀʟɪ ᴋᴇ ᴘᴏʟᴀ ᴘᴀᴋᴀɪ ᴍᴀsɪɴɢ-ᴍᴀsɪɴɢ.

ʙʏ @AunuHostv

AunuUbot
"""
