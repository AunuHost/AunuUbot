import base64
import binascii
import hashlib
import html
import re
import urllib.parse

from AunuUbot import *

__MODULE__ = "TextLab"
__HELP__ = """
<blockquote><b>TextLab

Text:
<code>{0}upper</code> <code>{0}lower</code> <code>{0}titlecase</code> <code>{0}swapcase</code>
<code>{0}reverse</code> <code>{0}rot13</code> <code>{0}slug</code> <code>{0}trim</code>
<code>{0}dedupwords</code> <code>{0}sortwords</code> <code>{0}palindrome</code> <code>{0}counttext</code>

Encode:
<code>{0}b64e</code> <code>{0}b64d</code> <code>{0}hexe</code> <code>{0}hexd</code>
<code>{0}binenc</code> <code>{0}bindec</code> <code>{0}urlenc</code> <code>{0}urldec</code>
<code>{0}htmle</code> <code>{0}htmld</code>

Hash:
<code>{0}md5</code> <code>{0}sha1</code> <code>{0}sha224</code> <code>{0}sha256</code>
<code>{0}sha384</code> <code>{0}sha512</code></b></blockquote>
"""


def _extract_text(message):
    text = get_text(message)
    return text.strip() if text else ""


def _need_text(text):
    if not text:
        raise ValueError("Balas pesan atau beri teks setelah command.")
    return text


def _bin_encode(text):
    return " ".join(format(ord(ch), "08b") for ch in text)


def _bin_decode(text):
    parts = text.split()
    return "".join(chr(int(part, 2)) for part in parts)


def _slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


TEXT_FUNCS = {
    "upper": lambda text: text.upper(),
    "lower": lambda text: text.lower(),
    "titlecase": lambda text: text.title(),
    "swapcase": lambda text: text.swapcase(),
    "reverse": lambda text: text[::-1],
    "rot13": lambda text: text.translate(
        str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
        )
    ),
    "slug": _slugify,
    "trim": lambda text: " ".join(text.split()),
    "dedupwords": lambda text: " ".join(dict.fromkeys(text.split())),
    "sortwords": lambda text: " ".join(sorted(text.split(), key=str.lower)),
    "palindrome": lambda text: "ya" if re.sub(r"\W+", "", text.lower()) == re.sub(r"\W+", "", text.lower())[::-1] else "tidak",
    "counttext": lambda text: (
        f"Karakter: {len(text)}\n"
        f"Tanpa spasi: {len(text.replace(' ', ''))}\n"
        f"Kata: {len(text.split())}\n"
        f"Baris: {len(text.splitlines()) or 1}"
    ),
    "b64e": lambda text: base64.b64encode(text.encode()).decode(),
    "b64d": lambda text: base64.b64decode(text.encode()).decode(),
    "hexe": lambda text: text.encode().hex(),
    "hexd": lambda text: bytes.fromhex(text).decode(),
    "binenc": _bin_encode,
    "bindec": _bin_decode,
    "urlenc": lambda text: urllib.parse.quote(text),
    "urldec": lambda text: urllib.parse.unquote(text),
    "htmle": lambda text: html.escape(text),
    "htmld": lambda text: html.unescape(text),
    "md5": lambda text: hashlib.md5(text.encode()).hexdigest(),
    "sha1": lambda text: hashlib.sha1(text.encode()).hexdigest(),
    "sha224": lambda text: hashlib.sha224(text.encode()).hexdigest(),
    "sha256": lambda text: hashlib.sha256(text.encode()).hexdigest(),
    "sha384": lambda text: hashlib.sha384(text.encode()).hexdigest(),
    "sha512": lambda text: hashlib.sha512(text.encode()).hexdigest(),
}


def _register_text_command(command, func):
    @PY.UBOT(command)
    @PY.TOP_CMD
    @PY.COOLDOWN(2)
    async def _handler(client, message, command=command, func=func):
        text = _extract_text(message)
        try:
            result = func(_need_text(text))
        except (ValueError, binascii.Error, UnicodeDecodeError) as error:
            return await message.reply_text(f"<b>{error}</b>")
        await message.reply_text(f"<code>{result}</code>")

    return _handler


for _command, _func in TEXT_FUNCS.items():
    _register_text_command(_command, _func)
