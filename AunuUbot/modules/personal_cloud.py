import asyncio
import os
import re

import requests

from AunuUbot import *

sc = Fonts.smallcap

__MODULE__ = sc("personal-cloud")
__HELP__ = f"""
<blockquote><b>{sc("bantuan personal cloud")}</b>

<b>{sc("digitalocean")}</b>
<code>{{0}}doaddapi &lt;token&gt;</code>
<code>{{0}}doaddapi none</code>
<code>{{0}}doaccount</code>
<code>{{0}}doregions</code>
<code>{{0}}dosizes</code>
<code>{{0}}doimages</code>
<code>{{0}}deployvps nama|region|size|image</code>
<code>{{0}}dovps</code>
<code>{{0}}dodelvps &lt;id&gt;</code>

<b>{sc("cloudflare")}</b>
<code>{{0}}cfaddapi &lt;token&gt;</code>
<code>{{0}}cfaddapi none</code>
<code>{{0}}cfaccount</code>
<code>{{0}}listdomain</code>
<code>{{0}}listsub domain.com</code>
<code>{{0}}addsub domain.com|sub|ip</code>
<code>{{0}}delsub domain.com|sub</code>

<b>{sc("payment")}</b>
<code>{{0}}adddana &lt;nomor&gt;</code>
<code>{{0}}addgopay &lt;nomor&gt;</code>
<code>{{0}}addovo &lt;nomor&gt;</code>
<code>{{0}}addshopeepay &lt;nomor&gt;</code>
<code>{{0}}addqris</code> {sc("reply foto atau link")}
<code>{{0}}delpay dana/gopay/ovo/shopeepay/qris</code>
<code>{{0}}paylist</code>
<code>{{0}}dana</code> <code>{{0}}gopay</code> <code>{{0}}ovo</code> <code>{{0}}shopeepay</code> <code>{{0}}qris</code>
"""

PAYMENT_METHODS = {
    "dana": sc("dana"),
    "gopay": sc("gopay"),
    "ovo": sc("ovo"),
    "shopeepay": sc("shopeepay"),
    "qris": sc("qris"),
}

def human_error(data, fallback="terjadi kesalahan"):
    if isinstance(data, dict):
        if data.get("message"):
            return str(data["message"])
        errors = data.get("errors")
        if isinstance(errors, list) and errors:
            first = errors[0]
            if isinstance(first, dict):
                return str(first.get("message") or first.get("error") or first)
            return str(first)
        if data.get("error"):
            return str(data["error"])
    return fallback


async def request_json(method, url, *, headers=None, params=None, json=None):
    def _run():
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json,
            timeout=45,
        )
        try:
            payload = response.json()
        except Exception:
            payload = {"message": response.text}
        return response.status_code, payload

    return await asyncio.to_thread(_run)


def do_headers(token: str):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def cf_headers(token: str):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


async def send_or_edit(message, text):
    if getattr(message, "outgoing", False):
        return await message.edit(text)
    return await message.reply(text)


async def media_source(client, message):
    if message.reply_to_message:
        replied = message.reply_to_message
        if replied.photo:
            return replied.photo.file_id
        if replied.text:
            return replied.text.strip()
        if replied.caption:
            return replied.caption.strip()
    if message.photo:
        return message.photo.file_id
    arg = get_arg(message)
    return arg.strip() if arg else None


async def text_source(message, skip_words=1):
    if message.reply_to_message:
        replied = message.reply_to_message
        if replied.text:
            return replied.text.strip()
        if replied.caption:
            return replied.caption.strip()
    parts = message.text.split(maxsplit=skip_words) if message.text else []
    if len(parts) > skip_words:
        return parts[skip_words].strip()
    return None


async def get_cf_zone(token: str, domain: str):
    status, data = await request_json(
        "GET",
        "https://api.cloudflare.com/client/v4/zones",
        headers=cf_headers(token),
        params={"name": domain, "per_page": 50},
    )
    if status >= 400 or not data.get("success"):
        raise ValueError(human_error(data, "gagal mengambil zone"))
    for zone in data.get("result") or []:
        if zone.get("name") == domain:
            return zone
    raise ValueError("domain tidak ditemukan")


@PY.UBOT("doaddapi|cfaddapi")
@PY.TOP_CMD
async def save_api_token(client, message):
    command = message.command[0].lower()
    arg = get_arg(message)
    if not arg:
        return await send_or_edit(message, f"<b>{sc('gunakan')}: <code>{command} token</code></b>")
    key = "DO_API_TOKEN" if command == "doaddapi" else "CF_API_TOKEN"
    label = sc("digitalocean") if command == "doaddapi" else sc("cloudflare")
    if arg.lower() == "none":
        await remove_vars(client.me.id, key)
        return await send_or_edit(message, f"<b>{label} {sc('api berhasil dihapus')}.</b>")
    await set_vars(client.me.id, key, arg.strip())
    return await send_or_edit(message, f"<b>{label} {sc('api berhasil disimpan')}.</b>")


@PY.UBOT("doregions|dosizes|doimages|dovps")
@PY.TOP_CMD
async def digitalocean_lookup(client, message):
    token = await get_vars(client.me.id, "DO_API_TOKEN")
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>doaddapi</code>.</b>")
    command = message.command[0].lower()
    mapping = {
        "doregions": ("https://api.digitalocean.com/v2/regions", "regions"),
        "dosizes": ("https://api.digitalocean.com/v2/sizes", "sizes"),
        "doimages": ("https://api.digitalocean.com/v2/images", "images"),
        "dovps": ("https://api.digitalocean.com/v2/droplets", "droplets"),
    }
    url, key = mapping[command]
    params = {"per_page": 20}
    if command == "doimages":
        params["type"] = "distribution"
    status, data = await request_json("GET", url, headers=do_headers(token), params=params)
    if status >= 400:
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    items = data.get(key) or []
    if not items:
        return await send_or_edit(message, f"<b>{sc('data tidak ditemukan')}.</b>")
    rows = []
    if command == "doregions":
        rows = [f"- <code>{x.get('slug')}</code> - {x.get('name')}" for x in items[:15]]
        title = sc("list region")
    elif command == "dosizes":
        rows = [f"- <code>{x.get('slug')}</code> - ${x.get('price_monthly')}/mo" for x in items[:15]]
        title = sc("list size")
    elif command == "doimages":
        rows = [f"- <code>{x.get('slug') or x.get('id')}</code> - {x.get('name')}" for x in items[:15]]
        title = sc("list image")
    else:
        title = sc("list vps")
        for item in items[:15]:
            ip = "-"
            for network in item.get("networks", {}).get("v4", []):
                if network.get("type") == "public":
                    ip = network.get("ip_address")
                    break
            rows.append(f"- <code>{item.get('id')}</code> - {item.get('name')} | {item.get('status')} | {ip}")
    return await send_or_edit(message, f"<blockquote><b>{title}</b>\n\n" + "\n".join(rows) + "</blockquote>")


@PY.UBOT("doaccount")
@PY.TOP_CMD
async def do_account(client, message):
    token = await get_vars(client.me.id, "DO_API_TOKEN")
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>doaddapi</code>.</b>")
    status, data = await request_json("GET", "https://api.digitalocean.com/v2/account", headers=do_headers(token))
    if status >= 400:
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    account = data.get("account") or {}
    return await send_or_edit(
        message,
        "<blockquote><b>{}</b>\n\nemail: <code>{}</code>\nstatus: <code>{}</code>\ndroplet_limit: <code>{}</code></blockquote>".format(
            sc("digitalocean account"),
            account.get("email", "-"),
            account.get("status", "-"),
            account.get("droplet_limit", "-"),
        ),
    )


@PY.UBOT("deployvps")
@PY.TOP_CMD
async def deploy_vps(client, message):
    token = await get_vars(client.me.id, "DO_API_TOKEN")
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>doaddapi</code>.</b>")
    arg = get_arg(message)
    if not arg:
        return await send_or_edit(
            message,
            "<b>{}</b> <code>deployvps nama|region|size|image</code>\n"
            "<b>{}</b> <code>deployvps web-1|sgp1|s-1vcpu-1gb|ubuntu-22-04-x64</code>".format(
                sc("gunakan:"), sc("contoh:")
            ),
        )
    parts = [x.strip() for x in arg.split("|")]
    if len(parts) < 3:
        return await send_or_edit(message, f"<b>{sc('format harus')}: nama|region|size|image</b>")
    name, region, size = parts[:3]
    image = parts[3] if len(parts) > 3 and parts[3] else "ubuntu-22-04-x64"
    wait = await send_or_edit(message, f"<b>{sc('membuat droplet')}...</b>")
    status, data = await request_json(
        "POST",
        "https://api.digitalocean.com/v2/droplets",
        headers=do_headers(token),
        json={
            "name": name,
            "region": region,
            "size": size,
            "image": image,
            "ipv6": True,
            "monitoring": True,
            "tags": ["aunu-ubot"],
        },
    )
    if status >= 400:
        return await wait.edit(f"<b>error: {human_error(data)}</b>")
    droplet = data.get("droplet") or {}
    return await wait.edit(
        "<blockquote><b>{}</b>\n\n"
        "id: <code>{}</code>\n"
        "nama: <code>{}</code>\n"
        "region: <code>{}</code>\n"
        "size: <code>{}</code>\n"
        "image: <code>{}</code></blockquote>".format(
            sc("droplet berhasil dibuat"),
            droplet.get("id"),
            droplet.get("name"),
            region,
            size,
            image,
        )
    )


@PY.UBOT("dodelvps")
@PY.TOP_CMD
async def delete_vps(client, message):
    token = await get_vars(client.me.id, "DO_API_TOKEN")
    droplet_id = get_arg(message)
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>doaddapi</code>.</b>")
    if not droplet_id:
        return await send_or_edit(message, f"<b>{sc('gunakan')}: <code>dodelvps id</code></b>")
    status, data = await request_json(
        "DELETE",
        f"https://api.digitalocean.com/v2/droplets/{droplet_id.strip()}",
        headers=do_headers(token),
    )
    if status >= 400:
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    return await send_or_edit(message, f"<b>{sc('droplet berhasil dihapus')}: <code>{droplet_id.strip()}</code></b>")


@PY.UBOT("listdomain")
@PY.TOP_CMD
async def list_domains(client, message):
    token = await get_vars(client.me.id, "CF_API_TOKEN")
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>cfaddapi</code>.</b>")
    status, data = await request_json(
        "GET",
        "https://api.cloudflare.com/client/v4/zones",
        headers=cf_headers(token),
        params={"per_page": 50},
    )
    if status >= 400 or not data.get("success"):
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    zones = data.get("result") or []
    if not zones:
        return await send_or_edit(message, f"<b>{sc('tidak ada domain di akun cloudflare')}.</b>")
    rows = [f"- <code>{zone.get('name')}</code>" for zone in zones[:50]]
    return await send_or_edit(message, f"<blockquote><b>{sc('list domain')}</b>\n\n" + "\n".join(rows) + "</blockquote>")


@PY.UBOT("cfaccount")
@PY.TOP_CMD
async def cf_account(client, message):
    token = await get_vars(client.me.id, "CF_API_TOKEN")
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>cfaddapi</code>.</b>")
    status, data = await request_json("GET", "https://api.cloudflare.com/client/v4/user/tokens/verify", headers=cf_headers(token))
    if status >= 400 or not data.get("success"):
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    result = data.get("result") or {}
    return await send_or_edit(
        message,
        "<blockquote><b>{}</b>\n\nstatus: <code>{}</code>\nid: <code>{}</code></blockquote>".format(
            sc("cloudflare token"),
            result.get("status", "-"),
            result.get("id", "-"),
        ),
    )


@PY.UBOT("listsub")
@PY.TOP_CMD
async def list_subdomains(client, message):
    token = await get_vars(client.me.id, "CF_API_TOKEN")
    domain = get_arg(message)
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>cfaddapi</code>.</b>")
    if not domain:
        return await send_or_edit(message, f"<b>{sc('gunakan')}: <code>listsub domain.com</code></b>")
    try:
        zone = await get_cf_zone(token, domain.strip())
    except Exception as error:
        return await send_or_edit(message, f"<b>error: {error}</b>")
    status, data = await request_json(
        "GET",
        f"https://api.cloudflare.com/client/v4/zones/{zone['id']}/dns_records",
        headers=cf_headers(token),
        params={"type": "A", "per_page": 100},
    )
    if status >= 400 or not data.get("success"):
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    records = data.get("result") or []
    if not records:
        return await send_or_edit(message, f"<b>{sc('tidak ada a record')}.</b>")
    rows = [f"- <code>{item.get('name')}</code> -> <code>{item.get('content')}</code>" for item in records[:50]]
    return await send_or_edit(message, f"<blockquote><b>{sc('list subdomain')}</b>\n\n" + "\n".join(rows) + "</blockquote>")


@PY.UBOT("addsub")
@PY.TOP_CMD
async def add_subdomain(client, message):
    token = await get_vars(client.me.id, "CF_API_TOKEN")
    arg = get_arg(message)
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>cfaddapi</code>.</b>")
    if not arg:
        return await send_or_edit(message, f"<b>{sc('gunakan')}: <code>addsub domain.com|sub|ip</code></b>")
    parts = [x.strip() for x in arg.split("|")]
    if len(parts) != 3:
        return await send_or_edit(message, f"<b>{sc('format harus')}: domain|sub|ip</b>")
    domain, sub, ip = parts
    try:
        zone = await get_cf_zone(token, domain)
    except Exception as error:
        return await send_or_edit(message, f"<b>error: {error}</b>")
    record_name = domain if sub in {"@", domain} else f"{sub}.{domain}"
    status, data = await request_json(
        "POST",
        f"https://api.cloudflare.com/client/v4/zones/{zone['id']}/dns_records",
        headers=cf_headers(token),
        json={"type": "A", "name": record_name, "content": ip, "ttl": 1, "proxied": False},
    )
    if status >= 400 or not data.get("success"):
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    return await send_or_edit(message, f"<b>{sc('subdomain berhasil dibuat')}</b>\n<code>{record_name}</code> -> <code>{ip}</code>")


@PY.UBOT("delsub")
@PY.TOP_CMD
async def delete_subdomain(client, message):
    token = await get_vars(client.me.id, "CF_API_TOKEN")
    arg = get_arg(message)
    if not token:
        return await send_or_edit(message, f"<b>{sc('silahkan set dulu')} <code>cfaddapi</code>.</b>")
    if not arg:
        return await send_or_edit(message, f"<b>{sc('gunakan')}: <code>delsub domain.com|sub</code></b>")
    parts = [x.strip() for x in arg.split("|")]
    if len(parts) != 2:
        return await send_or_edit(message, f"<b>{sc('format harus')}: domain|sub</b>")
    domain, sub = parts
    try:
        zone = await get_cf_zone(token, domain)
    except Exception as error:
        return await send_or_edit(message, f"<b>error: {error}</b>")
    record_name = domain if sub in {"@", domain} else f"{sub}.{domain}"
    status, data = await request_json(
        "GET",
        f"https://api.cloudflare.com/client/v4/zones/{zone['id']}/dns_records",
        headers=cf_headers(token),
        params={"name": record_name, "per_page": 100},
    )
    if status >= 400 or not data.get("success"):
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    records = data.get("result") or []
    if not records:
        return await send_or_edit(message, f"<b>{sc('dns record tidak ditemukan')}.</b>")
    record_id = records[0]["id"]
    status, data = await request_json(
        "DELETE",
        f"https://api.cloudflare.com/client/v4/zones/{zone['id']}/dns_records/{record_id}",
        headers=cf_headers(token),
    )
    if status >= 400 or not data.get("success"):
        return await send_or_edit(message, f"<b>error: {human_error(data)}</b>")
    return await send_or_edit(message, f"<b>{sc('subdomain berhasil dihapus')}: <code>{record_name}</code></b>")


@PY.UBOT("adddana|addgopay|addovo|addshopeepay|addqris")
@PY.TOP_CMD
async def add_payment(client, message):
    command = message.command[0].lower()
    method = command.replace("add", "", 1)
    key = f"PAY_{method.upper()}"
    if method == "qris":
        payload = await media_source(client, message)
        if not payload:
            return await send_or_edit(message, f"<b>{sc('reply foto atau kirim link qris')}.</b>")
        await set_vars(client.me.id, key, payload)
        return await send_or_edit(
            message,
            f"<blockquote><b>[9] {PAYMENT_METHODS[method]} {sc('berhasil disimpan')}</b>\n"
            f"{sc('payment ini sekarang aktif untuk userbot kamu')}</blockquote>",
        )
    payload = await text_source(message)
    if not payload:
        return await send_or_edit(message, f"<b>{sc('masukkan data untuk')} {PAYMENT_METHODS[method]}.</b>")
    await set_vars(client.me.id, key, payload)
    return await send_or_edit(
        message,
        f"<blockquote><b>[9] {PAYMENT_METHODS[method]} {sc('berhasil disimpan')}</b>\n"
        f"<code>{payload}</code></blockquote>",
    )


@PY.UBOT("dana|gopay|ovo|shopeepay|qris")
@PY.TOP_CMD
async def show_payment(client, message):
    method = message.command[0].lower()
    key = f"PAY_{method.upper()}"
    value = await get_vars(client.me.id, key)
    if not value:
        return await send_or_edit(message, f"<b>{PAYMENT_METHODS[method]} {sc('belum diset')}.</b>")
    if method == "qris":
        return await client.send_photo(
            message.chat.id,
            value,
            caption=(
                f"<blockquote><b>[9] {PAYMENT_METHODS[method]} {sc('milik')} {client.me.mention}</b></blockquote>\n"
                f"<blockquote>{sc('scan qris ini untuk melakukan pembayaran')}</blockquote>"
            ),
            reply_to_message_id=message.id,
        )
    return await send_or_edit(
        message,
        f"<blockquote><b>[9] {PAYMENT_METHODS[method]} {sc('milik')} {client.me.mention}</b>\n"
        f"<code>{value}</code></blockquote>",
    )


@PY.UBOT("delpay")
@PY.TOP_CMD
async def delete_payment(client, message):
    method = (get_arg(message) or "").strip().lower()
    if method not in PAYMENT_METHODS:
        return await send_or_edit(message, f"<b>{sc('gunakan')}: <code>delpay dana/gopay/ovo/shopeepay/qris</code></b>")
    await remove_vars(client.me.id, f"PAY_{method.upper()}")
    return await send_or_edit(message, f"<b>{PAYMENT_METHODS[method]} {sc('berhasil dihapus')}.</b>")


@PY.UBOT("paylist")
@PY.TOP_CMD
async def payment_list(client, message):
    rows = []
    for key, label in PAYMENT_METHODS.items():
        exists = await get_vars(client.me.id, f"PAY_{key.upper()}")
        rows.append(f"├ {label}: <code>{sc('aktif') if exists else sc('kosong')}</code>")
    if rows:
        rows[-1] = rows[-1].replace("├", "╰", 1)
    return await send_or_edit(
        message,
        f"<blockquote><b>[9] {sc('status payment')}</b>\n"
        f"owner: {client.me.mention}\n\n" + "\n".join(rows) + "</blockquote>",
    )
