import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from AunuUbot import *


async def expiredUserbots():
    tz = timezone("Asia/Jakarta")
    while True:
        # Iterate over a copy of the list to avoid modification during iteration
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
                    user_id = X.me.id
                    try:
                        await X.unblock_user(bot.me.username)
                    except Exception:
                        pass
                    # Cleanup database: remove all related data
                    await remove_ubot(user_id)
                    await remove_all_vars(user_id)
                    await rem_expired_date(user_id)
                    await rem_pref(user_id)
                    await remove_all_user_ids(user_id)
                    # Cleanup in-memory state
                    if user_id in ubot._get_my_id:
                        ubot._get_my_id.remove(user_id)
                    if user_id in ubot._prefix:
                        del ubot._prefix[user_id]
                    if user_id in ubot._translate:
                        del ubot._translate[user_id]
                    if user_id in ubot._get_my_peer:
                        del ubot._get_my_peer[user_id]
                    if X in ubot._ubot:
                        ubot._ubot.remove(X)
                    try:
                        await X.log_out()
                    except Exception:
                        pass
                    try:
                        await bot.send_message(
                            user_id,
                            MSG.EXP_MSG_UBOT(X),
                            reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
                        )
                    except Exception:
                        pass
            except Exception as e:
                print(f"[\U0001d197\U0001d197\U0001d197] - {getattr(getattr(X, 'me', None), 'id', '?')} - EXPIRED CHECK ERROR: {e}")
        await asyncio.sleep(60)
