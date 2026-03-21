import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from AunuUbot import *


async def expiredUserbots():
    while True:
        for X in ubot._ubot:
            try:
                time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
                exp = (await get_expired_date(X.me.id)).strftime("%d-%m-%Y")
                if time == exp:
                    await X.unblock_user(bot.me.username)
                    await remove_ubot(X.me.id)
                    await remove_all_vars(X.me.id)
                    await rem_expired_date(X.me.id)
                    ubot._get_my_id.remove(X.me.id)
                    ubot._ubot.remove(X)
                    await X.log_out()
                    await bot.send_message(
                        X.me.id,
                        MSG.EXP_MSG_UBOT(X),
                        reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
                    )
            except Exception as e:
                print(f"[𝗜𝗡𝗙𝗢] - {X.me.id} - EXPIRED END")
        await asyncio.sleep(60)
