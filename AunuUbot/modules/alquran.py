import requests

from AunuUbot import *

sc = Fonts.smallcap

__MODULE__ = sc("alquran")
__HELP__ = f"""
<blockquote><b>⁹ 〔 {sc("alquran board")} 〕</b>

<code>{{0}}alquran nomor_surah</code>
<code>{{0}}alquran nomor_surah:ayat</code>
<code>{{0}}surah nama</code>
{sc("membuka surah atau ayat alquran dengan tampilan yang lebih elegan")}</blockquote>
"""


def quran_header(title, subtitle):
    return (
        f"<blockquote><b>⁹ 〔 {sc('alquran center')} 〕</b></blockquote>\n"
        f"<blockquote>📖 {sc('surah')}: <code>{title}</code>\n"
        f"🪶 {sc('detail')}: <code>{subtitle}</code></blockquote>"
    )


@PY.UBOT("alquran|surah")
@PY.TOP_CMD
async def alquran(client, message):
    arg = get_arg(message)
    if not arg:
        return await message.reply_text(
            f"<blockquote><b>⁹ 〔 {sc('gunakan')} 〕</b>\n"
            f"<code>{message.command[0]} 1</code>\n"
            f"<code>{message.command[0]} 1:5</code></blockquote>"
        )
    wait = await message.reply_text(f"<blockquote><b>{sc('mencari data alquran')}...</b></blockquote>")
    try:
        if ":" in arg and message.command[0].lower() == "alquran":
            surah_no, ayat_no = [x.strip() for x in arg.split(":", 1)]
            data = requests.get(f"https://equran.id/api/v2/surat/{surah_no}", timeout=30).json()
            surat = data.get("data") or {}
            ayat = next((x for x in surat.get("ayat", []) if str(x.get("nomorAyat")) == ayat_no), None)
            if not ayat:
                return await wait.edit(f"<blockquote><b>{sc('ayat tidak ditemukan')}.</b></blockquote>")
            text = (
                quran_header(surat.get("namaLatin", "-"), f"ayat {ayat_no}")
                + "\n"
                + f"<blockquote><b>{ayat.get('teksArab', '-')}</b>\n\n"
                + f"{ayat.get('teksLatin', '-')}\n\n"
                + f"{ayat.get('teksIndonesia', '-')}</blockquote>\n"
                + f"<blockquote><b>⁹ 〔 {sc('ayat spotlight')} 〕</b></blockquote>"
            )
            return await wait.edit(text)

        if message.command[0].lower() == "surah" and not arg.replace(" ", "").isdigit():
            all_surah = requests.get("https://equran.id/api/v2/surat", timeout=30).json()
            found = None
            for item in all_surah.get("data", []):
                if arg.lower() in str(item.get("namaLatin", "")).lower():
                    found = item
                    break
            if not found:
                return await wait.edit(f"<blockquote><b>{sc('surah tidak ditemukan')}.</b></blockquote>")
            arg = str(found.get("nomor"))

        data = requests.get(f"https://equran.id/api/v2/surat/{arg.strip()}", timeout=30).json()
        surat = data.get("data") or {}
        if not surat:
            return await wait.edit(f"<blockquote><b>{sc('surah tidak ditemukan')}.</b></blockquote>")
        ayat_preview = surat.get("ayat", [])[:5]
        ayat_lines = []
        for ayat in ayat_preview:
            ayat_lines.append(
                f"<b>{ayat.get('nomorAyat')}.</b> {ayat.get('teksArab', '-')}\n"
                f"<i>{ayat.get('teksIndonesia', '-')}</i>"
            )
        text = (
            quran_header(
                surat.get("namaLatin", "-"),
                f"{surat.get('arti', '-')} • {surat.get('jumlahAyat', '-')} ayat",
            )
            + "\n"
            + f"<blockquote>🕌 {sc('tempat turun')}: <code>{surat.get('tempatTurun', '-')}</code>\n"
            + f"🎙 {sc('audio')}: <a href='{surat.get('audioFull', {}).get('05', '')}'>{sc('putar murattal')}</a></blockquote>\n"
            + "<blockquote>"
            + "\n\n".join(ayat_lines)
            + "</blockquote>\n"
            + f"<blockquote><b>⁹ 〔 {sc('preview 5 ayat pertama')} 〕</b></blockquote>"
        )
        await wait.edit(text, disable_web_page_preview=True)
    except Exception as error:
        await wait.edit(f"<blockquote><b>{sc('gagal mengambil data alquran')}.</b>\n<code>{error}</code></blockquote>")
