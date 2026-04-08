from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AunuUbot import OWNER_ID, bot, ubot, get_expired_date

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AunuUbot import OWNER_ID, bot, ubot


class MSG:
    def EXP_MSG_UBOT(X):
        return f"""
<blockquote><b>❏ ᴘᴇᴍʙᴇʀɪᴛᴀʜᴜᴀɴ</b>
<b>├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ɪᴅ:</b> <code>{X.me.id}</code>
<b>╰ ᴍᴀsᴀ ᴀᴋᴛɪғ ᴛᴇʟᴀʜ ʜᴀʙɪs</b></blockquote>
"""

    def START(message):
        return f"""
<blockquote><b>❖ ᴀᴜɴᴜ ᴜʙᴏᴛ sᴛᴀʀᴛ ᴘᴀɴᴇʟ ❖</b></blockquote>
<blockquote>👤 ʜᴀʟᴏ <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>
🤖 ʙᴏᴛ: @{bot.me.username}
🚀 sɪsᴛᴇᴍ ɪɴɪ ᴅɪsɪᴀᴘᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ᴅᴇɴɢᴀɴ ʟᴇʙɪʜ ᴄᴇᴘᴀᴛ</blockquote>

<blockquote>💬 ᴏᴡɴᴇʀ: <a href=tg://openmessage?user_id={OWNER_ID}>AunuXdev</a>
📜 ᴋᴇᴛᴇɴᴛᴜᴀɴ: <a href='https://t.me/AunuHostv'>ᴀᴜɴᴜʜᴏsᴛᴠ</a>
🧩 ᴛᴀᴘ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴜʟᴀɪ ᴘʀᴏsᴇs</blockquote>
"""

    def TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN):
        return f"""
<blockquote><b>❖ ᴘᴀʏᴍᴇɴᴛ ᴄᴇɴᴛᴇʀ ❖</b></blockquote>
<blockquote>🗓 ᴘᴀᴋᴇᴛ: <code>{BULAN} ʙᴜʟᴀɴ</code>
💸 ʜᴀʀɢᴀ ᴘᴇʀ ʙᴜʟᴀɴ: <code>ʀᴘ {HARGA}.000</code>
🧾 ᴛᴏᴛᴀʟ ᴘᴇᴍʙᴀʏᴀʀᴀɴ: <code>ʀᴘ {TOTAL_HARGA}.000</code></blockquote>

<blockquote><b>❖ ᴍᴇᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ❖</b>
├ ᴅᴀɴᴀ: <code>08132667596</code>
├ ɴᴀᴍᴀ: <code>AunuHost</code>
├ ɢᴏᴘᴀʏ: <code>ʙᴇʟᴜᴍ ᴛᴇʀsᴇᴅɪᴀ</code>
╰ ǫʀɪs: <code>ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ</code></blockquote>

<blockquote>💬 ᴋᴏɴᴛᴀᴋ ᴏᴡɴᴇʀ: <a href=tg://openmessage?user_id={OWNER_ID}>AunuHostv</a>
📎 sᴇᴛᴇʟᴀʜ ᴛʀᴀɴsғᴇʀ, ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴғɪʀᴍᴀsɪ ᴅᴀɴ ᴋɪʀɪᴍ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ</blockquote>
"""

    async def UBOT(count):
        return f"""
<blockquote><b>❏ ᴜsᴇʀʙᴏᴛ ᴋᴇ</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b>├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a>
<b>╰ ɪᴅ:</b> <code>{ubot._ubot[int(count)].me.id}</code></blockquote>
"""

    def POLICY():
        return """
ᴜɴᴛᴜᴋ ᴘᴇɴɢɢᴜɴᴀ ᴜsᴇʀʙᴏᴛ, ʟᴇʙɪʜ ᴀᴍᴀɴ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴀᴋᴜɴ ʏᴀɴɢ sᴜᴅᴀʜ ᴜsɪᴀ ᴅᴀɴ ᴘᴇᴍᴀᴋᴀɪᴀɴɴʏᴀ sᴛᴀʙɪʟ.
ʜɪɴᴅᴀʀɪ ᴀᴋᴜɴ ʙᴀʀᴜ ᴀᴛᴀᴜ ɪᴅ ᴀᴡᴀʟᴀɴ 0-5 ᴋᴀʀᴇɴᴀ ʟᴇʙɪʜ ʀᴀᴡᴀɴ sᴀᴀᴛ ᴅɪᴘᴀsᴀɴɢɪ ᴜsᴇʀʙᴏᴛ.
ᴀᴋᴜɴ ʟᴀᴍᴀ ᴀᴛᴀᴜ ɪᴅ ᴀᴡᴀʟᴀɴ 6-9 ʙɪᴀsᴀɴʏᴀ ʟᴇʙɪʜ sᴛᴀʙɪʟ, ᴛᴇᴛᴀᴘ sᴇᴍᴜᴀ ᴋᴇᴍʙᴀʟɪ ᴋᴇ ᴘᴏʟᴀ ᴘᴀᴋᴀɪ ᴍᴀsɪɴɢ-ᴍᴀsɪɴɢ.

ʙʏ @AunuHostv
"""

class MSG:     
    def EXP_MSG_UBOT(X):
        return f"""
<blockquote><b>❏ ᴘᴇᴍʙᴇʀɪᴛᴀʜᴜᴀɴ</b>
<b>├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ɪᴅ:</b> <code>{X.me.id}</code>
<b>╰ ᴍᴀsᴀ ᴀᴋᴛɪꜰ ᴛᴇʟᴀʜ ʜᴀʙɪs</b></blockquote>
"""

    def START(message):
        return f"""
<blockquote><b>👋🏻 ʜᴀʟᴏ <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>!

<b>💬 @{bot.me.username} ᴀᴅᴀʟᴀʜ ʙᴏᴛ ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ᴅᴇɴɢᴀɴ ᴍᴜᴅᴀʜ</b>

🚀 ꜱɪʟᴀʜᴋᴀɴ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ 
� ᴏᴡɴᴇʀ : <a href=tg://openmessage?user_id={OWNER_ID}>AunuXdev</a> 

ʟɪsᴛ ʜᴀʀɢᴀ & ᴋᴇʙᴜᴛᴜʜᴀɴ ᴜsᴇʀʙᴏᴛ :
<a href='https://t.me/AunuHostv'>ᴋᴇʙᴜᴛᴜʜᴀɴ ᴜsᴇʀʙᴏᴛ</a>

👉🏻 ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b></blockquote>
"""

    def TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN):
        return f"""
<blockquote><b>💬 sɪʟᴀʜᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>

<b>🎟️ ʜᴀʀɢᴀ ᴘᴇʀʙᴜʟᴀɴ: 10.000</b>

<b>💳 ᴍᴏᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:</b>
 </b>
 <b>├ ᴅᴀɴᴀ : `082328229523` <b>dwiaunu</b> </b>
 <b>├ ɢᴏᴘᴀʏ : `blom ada` <b>AunuXdev</b> </b>
 <b>├ ǫʀɪs : Maintance</b>
<b>🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ: ʀᴘ 15.000 ᴘᴇʀʙᴜʟᴀɴ</b> 

 🚀 ꜱɪʟᴀʜᴋᴀɴ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ 
� ᴏᴡɴᴇʀ : <a href=tg://openmessage?user_id={OWNER_ID}>AunuHostv</a>

<b>✅ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴꜰɪʀᴍᴀsɪ ᴜɴᴛᴜᴋ ᴋɪʀɪᴍ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ</b></blockquote>
"""

    async def UBOT(count):
        return f"""
<blockquote><b>❏ ᴜsᴇʀʙᴏᴛ ᴋᴇ</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b> ├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 
<b> ╰ ɪᴅ:</b> <code>{ubot._ubot[int(count)].me.id}</code></blockquote>
"""

    def POLICY():
        return """
ʙᴜᴀᴛ ʏᴀɴɢ ɴᴀɴʏᴀ ᴘᴇɴɢɢᴜɴᴀᴀɴ ᴜsᴇʀʙᴏᴛ ʏᴀɴɢ ᴀᴍᴀɴ ʙᴜᴀᴛ ᴅɪ ᴘᴀsᴀɴɢ ᴅɪ ᴀᴋᴜɴ ɪᴅ ᴀᴡᴀʟᴀɴ ʙᴇʀᴀᴘᴀ ʏᴀ??
ɢɪɴɪ ᴜɴᴛᴜᴋ ᴘᴇɴɢɢᴜɴᴀ ᴜsᴇʀʙᴏᴛ ɪᴛᴜ ᴊᴀɴɢᴀɴ ᴘᴇɴɢɢᴜɴᴀ ɪᴅ ᴀᴡᴀʟᴀɴ 𝟼-𝟽 ᴋᴀʀɴᴀ sᴀɴɢᴀᴛ ʀᴀᴡᴀɴ ᴊɪᴋᴀ ᴅɪ ᴘᴀsᴀɴɢ ᴜsᴇʀʙᴏᴛ.
ᴜɴᴛᴜᴋ ᴘᴇᴍᴀᴋᴀɪᴀɴ ᴜsᴇʀʙᴏᴛ ʙɪᴀsᴀ ᴅɪ ᴘᴀᴋᴀɪ ᴅɪ ᴀᴋᴜɴ ʟᴀᴍᴀ ᴀᴛᴀᴜ ʙɪᴀsᴀ ɪᴅ ᴀᴡᴀʟᴀɴ 𝟷-𝟻,
sᴇᴍᴜᴀ ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ɪᴅ ᴛᴇʀsᴇʙᴜᴛ sᴜᴅᴀʜ ᴛᴇʀʙɪʟᴀɴɢ ᴀᴍᴀɴ ᴛᴀᴘɪ sᴇᴍᴜᴀ ᴛᴇʀɢᴀɴᴛᴜɴɢ ᴘᴇᴍᴀᴋᴀɪᴀɴ ᴋᴀʟɪᴀɴ.

ʙʏ @AunuHostv
"""
