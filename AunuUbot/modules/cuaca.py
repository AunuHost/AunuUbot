import requests

from AunuUbot import *

sc = Fonts.smallcap

__MODULE__ = sc("cuaca")
__HELP__ = f"""
<blockquote><b>⁹ 〔 {sc("cuaca board")} 〕</b>

<code>{{0}}cuaca kota</code>
{sc("cek cuaca kota dengan tampilan ringkas, rapi, dan dekoratif")}</blockquote>
"""


def weather_icon(code):
    if code in {0}:
        return "☀️"
    if code in {1, 2, 3}:
        return "⛅"
    if code in {45, 48}:
        return "🌫"
    if code in {51, 53, 55, 61, 63, 65, 80, 81, 82}:
        return "🌧"
    if code in {71, 73, 75, 77, 85, 86}:
        return "❄️"
    if code in {95, 96, 99}:
        return "⛈"
    return "🌍"


@PY.UBOT("cuaca")
@PY.TOP_CMD
async def cuaca(client, message):
    city = get_arg(message)
    if not city:
        return await message.reply_text(
            f"<blockquote><b>⁹ 〔 {sc('gunakan')} 〕</b>\n<code>{message.command[0]} jakarta</code></blockquote>"
        )
    wait = await message.reply_text(f"<blockquote><b>{sc('mencari data cuaca')}...</b></blockquote>")
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "id", "format": "json"},
            timeout=30,
        ).json()
        results = geo.get("results") or []
        if not results:
            return await wait.edit(f"<blockquote><b>{sc('kota tidak ditemukan')}.</b></blockquote>")
        loc = results[0]
        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": loc["latitude"],
                "longitude": loc["longitude"],
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                "timezone": "Asia/Jakarta",
            },
            timeout=30,
        ).json()
        current = weather.get("current", {})
        icon = weather_icon(current.get("weather_code", -1))
        text = (
            f"<blockquote><b>⁹ 〔 {sc('weather report')} 〕</b></blockquote>\n"
            f"<blockquote>{icon} {sc('lokasi')}: <code>{loc.get('name')}</code>\n"
            f"🗺 {sc('wilayah')}: <code>{loc.get('admin1') or '-'}, {loc.get('country') or '-'}</code>\n"
            f"🌡 {sc('suhu')}: <code>{current.get('temperature_2m', '-')}°C</code>\n"
            f"💧 {sc('kelembapan')}: <code>{current.get('relative_humidity_2m', '-')}%</code>\n"
            f"🍃 {sc('angin')}: <code>{current.get('wind_speed_10m', '-')} km/h</code>\n"
            f"🧭 {sc('kode cuaca')}: <code>{current.get('weather_code', '-')}</code></blockquote>\n"
            f"<blockquote><b>⁹ 〔 {sc('live weather snapshot')} 〕</b></blockquote>"
        )
        await wait.edit(text)
    except Exception as error:
        await wait.edit(f"<blockquote><b>{sc('gagal mengambil data cuaca')}.</b>\n<code>{error}</code></blockquote>")
