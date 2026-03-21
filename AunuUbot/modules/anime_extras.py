from AunuUbot import *

WAIFU_COMMANDS = {
    "waifu": "waifu",
    "neko": "neko",
    "shinobu": "shinobu",
    "megumin": "megumin",
    "bully": "bully",
    "cuddle": "cuddle",
    "cry": "cry",
    "hug": "hug",
    "awoo": "awoo",
    "kiss": "kiss",
    "lick": "lick",
    "pat": "pat",
    "smug": "smug",
    "bonk": "bonk",
    "yeet": "yeet",
    "blush": "blush",
    "smile": "smile",
    "wave": "wave",
    "highfive": "highfive",
    "handhold": "handhold",
    "nom": "nom",
    "bite": "bite",
    "glomp": "glomp",
    "slap": "slap",
    "kill": "kill",
    "kicka": "kick",
    "happy": "happy",
    "wink": "wink",
    "dance": "dance",
    "cringe": "cringe",
}

__MODULE__ = "AnimeX"
__HELP__ = """
<blockquote><b>AnimeX Tools

Info:
<code>{0}anime</code> <code>{0}manga</code> <code>{0}character</code> <code>{0}seiyuu</code>
<code>{0}topanime</code> <code>{0}topmanga</code> <code>{0}randomanime</code> <code>{0}randommanga</code>

Reaction:
waifu, neko, shinobu, megumin, bully, cuddle, cry, hug, awoo, kiss, lick,
pat, smug, bonk, yeet, blush, smile, wave, highfive, handhold, nom, bite,
glomp, slap, kill, kicka, happy, wink, dance, cringe</b></blockquote>
"""


async def fetch_json(url, params=None):
    async with aiosession.get(url, params=params, timeout=30) as response:
        response.raise_for_status()
        return await response.json()


def _safe_text(value, fallback="-"):
    if value in (None, "", [], {}):
        return fallback
    if isinstance(value, list):
        return ", ".join(map(str, value[:5])) or fallback
    return str(value)


@PY.UBOT("anime")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Gunakan: <code>anime judul</code></b>")
    query = message.text.split(None, 1)[1]
    data = await fetch_json("https://api.jikan.moe/v4/anime", {"q": query, "limit": 1})
    results = data.get("data") or []
    if not results:
        return await message.reply_text("<b>Anime tidak ditemukan.</b>")
    anime = results[0]
    caption = (
        f"<b>{anime.get('title')}</b>\n"
        f"Score: <code>{_safe_text(anime.get('score'))}</code>\n"
        f"Episodes: <code>{_safe_text(anime.get('episodes'))}</code>\n"
        f"Status: <code>{_safe_text(anime.get('status'))}</code>\n"
        f"Source: <code>{_safe_text(anime.get('source'))}</code>\n"
        f"Genres: <code>{_safe_text([x['name'] for x in anime.get('genres', [])])}</code>\n\n"
        f"{_safe_text(anime.get('synopsis'))[:900]}"
    )
    await message.reply_photo(anime["images"]["jpg"]["image_url"], caption=caption)


@PY.UBOT("manga")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Gunakan: <code>manga judul</code></b>")
    query = message.text.split(None, 1)[1]
    data = await fetch_json("https://api.jikan.moe/v4/manga", {"q": query, "limit": 1})
    results = data.get("data") or []
    if not results:
        return await message.reply_text("<b>Manga tidak ditemukan.</b>")
    manga = results[0]
    caption = (
        f"<b>{manga.get('title')}</b>\n"
        f"Score: <code>{_safe_text(manga.get('score'))}</code>\n"
        f"Chapters: <code>{_safe_text(manga.get('chapters'))}</code>\n"
        f"Status: <code>{_safe_text(manga.get('status'))}</code>\n"
        f"Genres: <code>{_safe_text([x['name'] for x in manga.get('genres', [])])}</code>\n\n"
        f"{_safe_text(manga.get('synopsis'))[:900]}"
    )
    await message.reply_photo(manga["images"]["jpg"]["image_url"], caption=caption)


@PY.UBOT("character|char")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Gunakan: <code>character nama</code></b>")
    query = message.text.split(None, 1)[1]
    data = await fetch_json("https://api.jikan.moe/v4/characters", {"q": query, "limit": 1})
    results = data.get("data") or []
    if not results:
        return await message.reply_text("<b>Karakter tidak ditemukan.</b>")
    char = results[0]
    nick = _safe_text(char.get("nicknames"))
    anime_refs = _safe_text([x["anime"]["title"] for x in char.get("anime", [])])
    caption = (
        f"<b>{char.get('name')}</b>\n"
        f"Nicknames: <code>{nick}</code>\n"
        f"Anime: <code>{anime_refs}</code>\n\n"
        f"{_safe_text(char.get('about'))[:900]}"
    )
    await message.reply_photo(char["images"]["jpg"]["image_url"], caption=caption)


@PY.UBOT("seiyuu|person")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Gunakan: <code>seiyuu nama</code></b>")
    query = message.text.split(None, 1)[1]
    data = await fetch_json("https://api.jikan.moe/v4/people", {"q": query, "limit": 1})
    results = data.get("data") or []
    if not results:
        return await message.reply_text("<b>Seiyuu tidak ditemukan.</b>")
    person = results[0]
    voices = _safe_text([x["character"]["name"] for x in person.get("voices", [])])
    caption = (
        f"<b>{person.get('name')}</b>\n"
        f"Favorites: <code>{_safe_text(person.get('favorites'))}</code>\n"
        f"Voices: <code>{voices}</code>\n\n"
        f"{_safe_text(person.get('about'))[:900]}"
    )
    await message.reply_photo(person["images"]["jpg"]["image_url"], caption=caption)


@PY.UBOT("topanime")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    data = await fetch_json("https://api.jikan.moe/v4/top/anime", {"limit": 10})
    lines = []
    for index, item in enumerate(data.get("data", [])[:10], start=1):
        lines.append(f"{index}. {item['title']} | score {item.get('score', '-')}")
    await message.reply_text("<b>Top Anime:</b>\n\n" + "\n".join(lines))


@PY.UBOT("topmanga")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    data = await fetch_json("https://api.jikan.moe/v4/top/manga", {"limit": 10})
    lines = []
    for index, item in enumerate(data.get("data", [])[:10], start=1):
        lines.append(f"{index}. {item['title']} | score {item.get('score', '-')}")
    await message.reply_text("<b>Top Manga:</b>\n\n" + "\n".join(lines))


@PY.UBOT("randomanime")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    data = await fetch_json("https://api.jikan.moe/v4/random/anime")
    anime = data.get("data") or {}
    caption = (
        f"<b>{anime.get('title')}</b>\n"
        f"Score: <code>{_safe_text(anime.get('score'))}</code>\n"
        f"Genres: <code>{_safe_text([x['name'] for x in anime.get('genres', [])])}</code>\n\n"
        f"{_safe_text(anime.get('synopsis'))[:900]}"
    )
    await message.reply_photo(anime["images"]["jpg"]["image_url"], caption=caption)


@PY.UBOT("randommanga")
@PY.TOP_CMD
@PY.COOLDOWN(3)
async def _(client, message):
    data = await fetch_json("https://api.jikan.moe/v4/random/manga")
    manga = data.get("data") or {}
    caption = (
        f"<b>{manga.get('title')}</b>\n"
        f"Score: <code>{_safe_text(manga.get('score'))}</code>\n"
        f"Chapters: <code>{_safe_text(manga.get('chapters'))}</code>\n\n"
        f"{_safe_text(manga.get('synopsis'))[:900]}"
    )
    await message.reply_photo(manga["images"]["jpg"]["image_url"], caption=caption)


for command, endpoint in WAIFU_COMMANDS.items():
    @PY.UBOT(command)
    @PY.TOP_CMD
    @PY.COOLDOWN(2)
    async def _reaction(client, message, endpoint=endpoint, command=command):
        data = await fetch_json(f"https://api.waifu.pics/sfw/{endpoint}")
        await message.reply_photo(
            data["url"],
            caption=f"<b>{command.title()} by AunuHostv</b>",
        )
