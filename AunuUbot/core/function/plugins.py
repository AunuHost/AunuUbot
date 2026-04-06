import importlib
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AunuUbot import bot, ubot
from AunuUbot.core.helpers import PY
from AunuUbot.core.helpers._cmd import get_total_commands
from AunuUbot.modules import loadModule
from AunuUbot.core.database import *
from AunuUbot.config import OWNER_ID
from platform import python_version
from pyrogram import __version__
HELP_COMMANDS = {}


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = importlib.import_module(f"AunuUbot.modules.{mod}")
        module_name = getattr(imported_module, "__MODULE__", "").replace(" ", "_").lower()
        if module_name:
            HELP_COMMANDS[module_name] = imported_module
    print(f"[🤖 @{bot.me.username} 🤖] [💠 TELAH BERHASIL DIAKTIFKAN! 💠]")
    await bot.send_message(OWNER_ID, 
       f"""                    
<b>🤖 {bot.me.mention} ʙᴇʀʜᴀsɪʟ ᴅɪᴀᴋᴛɪꜰᴋᴀɴ</b>

<b>📁 ᴍᴏᴅᴜʟᴇs: {len(HELP_COMMANDS)}</b>
<b>🧩 ᴄᴏᴍᴍᴀɴᴅs: {get_total_commands()}</b>
<b>📘 ᴘʏᴛʜᴏɴ: {python_version()}</b>
<b>📙 ᴘʏʀᴏɢʀᴀᴍ: {__version__}</b>

<b>👤 ᴜsᴇʀʙᴏᴛ: {len(ubot._ubot)}</b>
""",
   reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🤖 ʟɪꜱᴛ ᴜꜱᴇʀʙᴏᴛ 🤖", callback_data="cek_ubot"),
                ],
            ]
        ),
                          )
    
@PY.CALLBACK("0_cls")
async def _(client, callback_query):
    await callback_query.message.delete()
