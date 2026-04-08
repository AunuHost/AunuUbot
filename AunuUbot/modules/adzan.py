import requests

from AunuUbot import *

sc = Fonts.smallcap

__MODULE__ = sc("shalat")
__HELP__ = f"""
<blockquote><b>[9] {sc("shalat center")}</b>

<code>{{0}}adzan kota</code>
<code>{{0}}sholat kota</code>
{sc("melihat jadwal shalat harian dengan tampilan yang lebih rapi dan informatif")}</blockquote>
"""


def prayer_card(city_name, result):
    item = result["items"][0]
    return (
        f"<blockquote><b>[9] {sc('jadwal shalat')}</b></blockquote>\n"
        f"<blockquote>kota: <code>{city_name}</code>\n"
        f"negara: <code>{result.get('country', '-')}</code>\n"
        f"tanggal: <code>{item.get('date_for', '-')}</code></blockquote>\n"
        f"<blockquote>imsak: <code>{item.get('shurooq', '-')}</code>\n"
        f"subuh: <code>{item.get('fajr', '-')}</code>\n"
        f"zuhur: <code>{item.get('dhuhr', '-')}</code>\n"
        f"ashar: <code>{item.get('asr', '-')}</code>\n"
        f"maghrib: <code>{item.get('maghrib', '-')}</code>\n"
        f"isya: <code>{item.get('isha', '-')}</code></blockquote>\n"
        f"<blockquote><b>[9] {sc('aunu ubot prayer board')}</b></blockquote>"
    )


@PY.UBOT("adzan|sholat")
@PY.TOP_CMD
async def adzan(client, message):
    city = get_arg(message)
    if not city:
        return await message.reply_text(
            f"<blockquote><b>[9] {sc('gunakan')}</b>\n<code>{message.command[0]} jakarta</code></blockquote>"
        )
    wait = await message.reply_text(
        f"<blockquote><b>{sc('mencari jadwal shalat')}...</b></blockquote>"
    )
    url = f"http://muslimsalat.com/{city}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        result = response.json()
        if not result.get("items"):
            return await wait.edit(
                f"<blockquote><b>{sc('jadwal shalat tidak ditemukan')}.</b></blockquote>"
            )
        await wait.edit(prayer_card(result.get("query", city.title()), result))
    except Exception as error:
        await wait.edit(
            f"<blockquote><b>{sc('gagal mengambil jadwal shalat')}.</b>\n<code>{error}</code></blockquote>"
        )
