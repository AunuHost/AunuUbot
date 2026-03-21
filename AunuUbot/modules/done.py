import asyncio
import datetime

from AunuUbot import *

__MODULE__ = "Done"
__HELP__ = """
<blockquote><b>Bantuan Untuk Done</b>

� <b>Perintah</b> : <code>{0}done</code> <b>[nama item],[harga],[pembayaran]</b>
� <b>Penjelasan</b> : konfirmasi pembayaran.</blockquote>
"""


@PY.UBOT("done")
async def done_command(client, message):
    izzy_ganteng = await message.reply("<blockquote>memproses...</blockquote>")
    await asyncio.sleep(5)
    try:
        args = message.text.split(" ", 1)
        if len(args) < 2 or "," not in args[1]:
            await message.reply_text(
                "<blockquote>Penggunaan: .done nama item,harga,payment</blockquote>"
            )
            return

        parts = args[1].split(",", 2)
        if len(parts) < 2:
            await message.reply_text(
                "<blockquote>Penggunaan: .done nama item,harga,payment</blockquote>"
            )
            return

        name_item = parts[0].strip()
        price = parts[1].strip()
        payment = parts[2].strip() if len(parts) > 2 else "Lainnya"
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = (
            "『 TRANSAKSI BERHASIL 』\n\n"
            f"📦 <b>Barang:</b> {name_item}\n"
            f"💸 <b>Nominal:</b> {price}\n"
            f"🕰️ <b>Waktu:</b> {time}\n"
            f"💬 <b>Payment:</b> {payment}\n\n"
            "Thanks for buying at AunuXdev Markets\n"
            "Contact: https://t.me/AunuHostv"
        )
        await izzy_ganteng.edit(response)

    except Exception as e:
        await izzy_ganteng.edit(f"error: {e}")
