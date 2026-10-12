import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from AunuUbot import *


async def expiredUserbots():
    tz = timezone("Asia/Jakarta")
    while True:
        for X in list(ubot._ubot):
            try:
                exp_date = await get_expired_date(X.me.id)
                if exp_date is None:
                    continue
                # ponytail: naive DB dates assumed WIB; make aware for correct comparison
                if exp_date.tzinfo is None:
                    exp_date = tz.localize(exp_date)
                now = datetime.now(tz)
                # FIX: pakai perbandingan tanggal >= bukan string == agar tidak miss jika bot offline lewat hari H
                if now.date() >= exp_date.date():
                    try:
                        await X.unblock_user(bot.me.username)
                    except Exception:
                        pass
                    await remove_ubot(X.me.id)
                    await remove_all_vars(X.me.id)
                    await rem_expired_date(X.me.id)
                    if X.me.id in ubot._get_my_id:
                        ubot._get_my_id.remove(X.me.id)
                    if X in ubot._ubot:
                        ubot._ubot.remove(X)
                    try:
                        await X.log_out()
                    except Exception:
                        pass
                    try:
                        await bot.send_message(
                            X.me.id,
                            MSG.EXP_MSG_UBOT(X),
                            reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
                        )
                    except Exception:
                        pass
            except Exception as e:
                print(f"[\U0001d197\U0001d197\U0001d197] - {getattr(getattr(X, 'me', None), 'id', '?')} - EXPIRED CHECK ERROR: {e}")
        await asyncio.sleep(60)
