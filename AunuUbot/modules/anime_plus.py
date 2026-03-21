from AunuUbot import *

__MODULE__ = "AnimePlus"
__HELP__ = """
<blockquote><b>AnimePlus

<code>{0}seasonnow</code> <code>{0}seasonupcoming</code> <code>{0}topairing</code>
<code>{0}topupcoming</code> <code>{0}topbypopularity</code> <code>{0}topfavorite</code>
<code>{0}schedmon</code> <code>{0}schedtue</code> <code>{0}schedwed</code> <code>{0}schedthu</code>
<code>{0}schedfri</code> <code>{0}schedsat</code> <code>{0}schedsun</code></b></blockquote>
"""


async def _jikan(url, params=None):
    async with aiosession.get(url, params=params, timeout=30) as response:
        response.raise_for_status()
        return await response.json()


async def _send_top_list(message, title, url, params=None):
    data = await _jikan(url, params)
    lines = []
    for index, item in enumerate((data.get("data") or [])[:10], start=1):
        lines.append(f"{index}. {item.get('title')} | score {item.get('score', '-')}")
    await message.reply_text(f"<b>{title}</b>\n\n" + "\n".join(lines))


@PY.UBOT("seasonnow")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    data = await _jikan("https://api.jikan.moe/v4/seasons/now")
    lines = [f"{i+1}. {x.get('title')} | {x.get('status')}" for i, x in enumerate((data.get("data") or [])[:10])]
    await message.reply_text("<b>Anime Season Now</b>\n\n" + "\n".join(lines))


@PY.UBOT("seasonupcoming")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    data = await _jikan("https://api.jikan.moe/v4/seasons/upcoming")
    lines = [f"{i+1}. {x.get('title')} | {x.get('status')}" for i, x in enumerate((data.get("data") or [])[:10])]
    await message.reply_text("<b>Anime Season Upcoming</b>\n\n" + "\n".join(lines))


@PY.UBOT("topairing")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    await _send_top_list(message, "Top Airing Anime", "https://api.jikan.moe/v4/top/anime", {"filter": "airing"})


@PY.UBOT("topupcoming")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    await _send_top_list(message, "Top Upcoming Anime", "https://api.jikan.moe/v4/top/anime", {"filter": "upcoming"})


@PY.UBOT("topbypopularity")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    await _send_top_list(message, "Top Anime by Popularity", "https://api.jikan.moe/v4/top/anime", {"filter": "bypopularity"})


@PY.UBOT("topfavorite")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    await _send_top_list(message, "Top Favorite Anime", "https://api.jikan.moe/v4/top/anime", {"filter": "favorite"})


def _register_schedule(command, day):
    @PY.UBOT(command)
    @PY.TOP_CMD
    @PY.COOLDOWN(3)
    async def _handler(client, message, day=day):
        data = await _jikan("https://api.jikan.moe/v4/schedules", {"filter": day})
        lines = []
        for index, item in enumerate((data.get("data") or [])[:10], start=1):
            lines.append(f"{index}. {item.get('title')} | {item.get('status')}")
        await message.reply_text(f"<b>Schedule {day.title()}</b>\n\n" + "\n".join(lines))

    return _handler


for _command, _day in {
    "schedmon": "monday",
    "schedtue": "tuesday",
    "schedwed": "wednesday",
    "schedthu": "thursday",
    "schedfri": "friday",
    "schedsat": "saturday",
    "schedsun": "sunday",
}.items():
    _register_schedule(_command, _day)
