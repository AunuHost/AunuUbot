import ast
import math
import random
import statistics
import time
import uuid
from datetime import datetime, timedelta

from AunuUbot import *

__MODULE__ = "UtilsLab"
__HELP__ = """
<blockquote><b>UtilsLab

Math:
<code>{0}calc</code> <code>{0}persen</code> <code>{0}diskon</code> <code>{0}bmi</code>
<code>{0}mean</code> <code>{0}median</code> <code>{0}mode</code> <code>{0}gcd</code>
<code>{0}lcm</code> <code>{0}fibo</code> <code>{0}factorial</code> <code>{0}prime</code>

Random:
<code>{0}coin</code> <code>{0}dice</code> <code>{0}rand</code> <code>{0}pick</code>

Utility:
<code>{0}uuid</code> <code>{0}unix</code> <code>{0}fromunix</code> <code>{0}now</code>
<code>{0}countdown</code></b></blockquote>
"""


SAFE_NAMES = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "pow": pow,
    "ceil": math.ceil,
    "floor": math.floor,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "pi": math.pi,
    "e": math.e,
}


def _extract_text(message):
    text = get_text(message)
    return text.strip() if text else ""


def _split_numbers(text):
    return [float(x) for x in text.replace(",", " ").split()]


def _safe_eval(expr):
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(
            node,
            (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,
                ast.Constant,
                ast.Load,
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.FloorDiv,
                ast.Mod,
                ast.Pow,
                ast.USub,
                ast.UAdd,
                ast.Call,
                ast.Name,
                ast.Tuple,
                ast.List,
            ),
        ):
            raise ValueError("Ekspresi tidak aman.")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in SAFE_NAMES:
                raise ValueError("Fungsi tidak diizinkan.")
    return eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, SAFE_NAMES)


@PY.UBOT("calc")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    expr = _extract_text(message)
    if not expr:
        return await message.reply_text("<b>Gunakan: <code>calc 2+2*5</code></b>")
    try:
        result = _safe_eval(expr)
    except Exception as error:
        return await message.reply_text(f"<b>{error}</b>")
    await message.reply_text(f"<code>{result}</code>")


@PY.UBOT("persen")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    parts = _extract_text(message).split()
    if len(parts) != 2:
        return await message.reply_text("<b>Gunakan: <code>persen 25 400</code></b>")
    persen, total = map(float, parts)
    await message.reply_text(f"<code>{(persen / 100) * total}</code>")


@PY.UBOT("diskon")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    parts = _extract_text(message).split()
    if len(parts) != 2:
        return await message.reply_text("<b>Gunakan: <code>diskon 100000 15</code></b>")
    harga, persen = map(float, parts)
    akhir = harga - ((persen / 100) * harga)
    await message.reply_text(f"<code>{akhir}</code>")


@PY.UBOT("bmi")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    parts = _extract_text(message).split()
    if len(parts) != 2:
        return await message.reply_text("<b>Gunakan: <code>bmi 70 170</code></b>")
    berat, tinggi_cm = map(float, parts)
    tinggi_m = tinggi_cm / 100
    bmi = berat / (tinggi_m ** 2)
    await message.reply_text(f"<b>BMI:</b> <code>{bmi:.2f}</code>")


def _register_numbers_command(command, func):
    @PY.UBOT(command)
    @PY.TOP_CMD
    @PY.COOLDOWN(2)
    async def _handler(client, message, func=func):
        text = _extract_text(message)
        if not text:
            return await message.reply_text("<b>Masukkan angka dipisah spasi.</b>")
        try:
            numbers = _split_numbers(text)
            result = func(numbers)
        except Exception as error:
            return await message.reply_text(f"<b>{error}</b>")
        await message.reply_text(f"<code>{result}</code>")

    return _handler


_register_numbers_command("mean", lambda nums: statistics.mean(nums))
_register_numbers_command("median", lambda nums: statistics.median(nums))
_register_numbers_command("mode", lambda nums: statistics.mode(nums))
_register_numbers_command("gcd", lambda nums: math.gcd(*(int(x) for x in nums)))
_register_numbers_command("lcm", lambda nums: math.lcm(*(int(x) for x in nums)))


@PY.UBOT("fibo")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    text = _extract_text(message)
    if not text:
        return await message.reply_text("<b>Gunakan: <code>fibo 10</code></b>")
    n = int(text)
    if n > 50:
        return await message.reply_text("<b>Maksimal 50 angka fibonacci.</b>")
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(str(a))
        a, b = b, a + b
    await message.reply_text("<code>{}</code>".format(" ".join(seq)))


@PY.UBOT("factorial")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    text = _extract_text(message)
    if not text:
        return await message.reply_text("<b>Gunakan: <code>factorial 6</code></b>")
    n = int(text)
    await message.reply_text(f"<code>{math.factorial(n)}</code>")


@PY.UBOT("prime")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    text = _extract_text(message)
    if not text:
        return await message.reply_text("<b>Gunakan: <code>prime 17</code></b>")
    n = int(text)
    if n < 2:
        return await message.reply_text("<b>Bukan bilangan prima.</b>")
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return await message.reply_text("<b>Bukan bilangan prima.</b>")
    await message.reply_text("<b>Bilangan prima.</b>")


@PY.UBOT("coin")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    await message.reply_text(f"<b>{random.choice(['Heads', 'Tails'])}</b>")


@PY.UBOT("dice")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    await message.reply_text(f"<b>{random.randint(1, 6)}</b>")


@PY.UBOT("rand")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    parts = _extract_text(message).split()
    if len(parts) != 2:
        return await message.reply_text("<b>Gunakan: <code>rand 1 100</code></b>")
    start, end = map(int, parts)
    await message.reply_text(f"<b>{random.randint(start, end)}</b>")


@PY.UBOT("pick")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    text = _extract_text(message)
    items = [x.strip() for x in text.split("|") if x.strip()]
    if len(items) < 2:
        return await message.reply_text("<b>Gunakan: <code>pick merah | biru | hijau</code></b>")
    await message.reply_text(f"<b>{random.choice(items)}</b>")


@PY.UBOT("uuid")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    await message.reply_text(f"<code>{uuid.uuid4()}</code>")


@PY.UBOT("unix")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    await message.reply_text(f"<code>{int(time.time())}</code>")


@PY.UBOT("fromunix")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    text = _extract_text(message)
    if not text:
        return await message.reply_text("<b>Gunakan: <code>fromunix 1700000000</code></b>")
    ts = int(text)
    await message.reply_text(f"<code>{datetime.fromtimestamp(ts)}</code>")


@PY.UBOT("now")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    await message.reply_text(f"<code>{datetime.now()}</code>")


@PY.UBOT("countdown")
@PY.TOP_CMD
@PY.COOLDOWN(2)
async def _(client, message):
    text = _extract_text(message)
    if not text:
        return await message.reply_text("<b>Gunakan: <code>countdown 2026-12-31 23:59</code></b>")
    try:
        target = datetime.strptime(text, "%Y-%m-%d %H:%M")
    except ValueError:
        return await message.reply_text("<b>Format: YYYY-MM-DD HH:MM</b>")
    delta = target - datetime.now()
    await message.reply_text(f"<code>{delta}</code>")
