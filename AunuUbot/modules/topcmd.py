from AunuUbot import *

async def get_top_module(client, message):
    vars = await all_vars(bot.me.id, "modules")
    sorted_vars = sorted(vars.items(), key=lambda item: item[1], reverse=True)

    command_count = 999
    text = message.text.split()

    if len(text) == 2:
        try:
            command_count = min(max(int(text[1]), 1), 10)
        except ValueError:
            pass

    total_count = sum(count for _, count in sorted_vars[:command_count])

    txt = "<emoji id=5231200819986047254>📊</emoji> top command\n\n"
    for command, count in sorted_vars[:command_count]:
        txt += f"<blockquote><b> �> {command} : {count}\n</b></blockquote>"

    txt += f"\n<emoji id=5282843764451195532>📈</emoji> total: {total_count} command"

    await message.reply(txt)

@PY.UBOT("top")
@PY.OWNER
async def _(client, message):
    await get_top_module(client, message)