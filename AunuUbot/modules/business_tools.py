from AunuUbot import *

__MODULE__ = "ʙɪsɴɪs"
__HELP__ = """
<blockquote><b>Pack command bisnis tambahan.

Contoh:
<code>{0}bizplanreseller</code>
<code>{0}biztipsclosing</code>
<code>{0}biztemplateinvoice</code>
<code>{0}bizcheckstok</code>
<code>{0}bizcalcomzet</code>

command bertema bisnis, jualan, marketing, invoice, reseller, dan operasional toko.</b></blockquote>
"""

BUSINESS_TOPICS = {
    "reseller": "reseller",
    "affiliate": "affiliate",
    "invoice": "invoice",
    "promo": "promo",
    "branding": "branding",
    "leads": "leads",
    "closing": "closing",
    "cs": "customer service",
    "toko": "toko online",
    "marketplace": "marketplace",
    "katalog": "katalog",
    "copy": "copywriting",
    "caption": "caption jualan",
    "konten": "konten marketing",
    "harga": "strategi harga",
    "diskon": "strategi diskon",
    "stok": "manajemen stok",
    "omzet": "target omzet",
    "roi": "ROI bisnis",
    "target": "target penjualan",
}

BUSINESS_ACTIONS = {
    "plan": "rencana",
    "tips": "tips",
    "template": "template",
    "check": "checklist",
    "calc": "perhitungan",
}


def build_business_text(action_key, action_label, topic_key, topic_label):
    if action_key == "plan":
        body = (
            f"1. Tentukan objective utama untuk {topic_label}.\n"
            f"2. Susun target mingguan, PIC, dan KPI.\n"
            f"3. Buat alur kerja sederhana dari traffic sampai closing.\n"
            f"4. Evaluasi hasil {topic_label} tiap 7 hari.\n"
        )
    elif action_key == "tips":
        body = (
            f"1. Fokus pada 1 masalah utama pelanggan di area {topic_label}.\n"
            f"2. Gunakan bahasa singkat, angka, dan bukti hasil.\n"
            f"3. Simpan template yang paling sering dipakai.\n"
            f"4. Catat apa yang menaikkan respon, closing, atau repeat order.\n"
        )
    elif action_key == "template":
        body = (
            f"Template {topic_label}:\n"
            f"- Halo kak, aku bantu info {topic_label} ya.\n"
            f"- Kebutuhan utama kakak apa dan targetnya kapan?\n"
            f"- Setelah itu aku kirim opsi, estimasi, dan langkah berikutnya.\n"
        )
    elif action_key == "check":
        body = (
            f"Checklist {topic_label}:\n"
            f"- target jelas\n"
            f"- data pelanggan/produk siap\n"
            f"- template follow up siap\n"
            f"- evaluasi harian dibuat\n"
        )
    else:
        body = (
            f"Rumus dasar {topic_label}:\n"
            f"- omzet = jumlah order x rata-rata transaksi\n"
            f"- laba = omzet - biaya\n"
            f"- ROI = (laba / biaya) x 100%\n"
        )
    return (
        f"<blockquote><b>📊 {action_label.title()} {topic_label.title()}</b>\n\n"
        f"{body}\n"
        f"Gunakan command ini sebagai template cepat untuk operasional bisnis harian.</blockquote>"
    )


def make_business_handler(action_key, action_label, topic_key, topic_label):
    async def handler(client, message):
        await message.reply(
            build_business_text(action_key, action_label, topic_key, topic_label),
            quote=True,
        )

    return handler


for _action_key, _action_label in BUSINESS_ACTIONS.items():
    for _topic_key, _topic_label in BUSINESS_TOPICS.items():
        _commands = (
            f"biz{_action_key}{_topic_key}"
            f"|usaha{_action_key}{_topic_key}"
            f"|jualan{_action_key}{_topic_key}"
        )
        _func = make_business_handler(
            _action_key, _action_label, _topic_key, _topic_label
        )
        _func.__name__ = f"business_{_action_key}_{_topic_key}"
        globals()[_func.__name__] = PY.UBOT(_commands)(_func)
