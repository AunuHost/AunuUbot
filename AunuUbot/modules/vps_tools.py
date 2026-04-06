from AunuUbot import *

__MODULE__ = "ᴠᴘs"
__HELP__ = """
<blockquote><b>Pack command VPS tambahan.

Contoh:
<code>{0}vpschecknginx</code>
<code>{0}vpsinstallpm2</code>
<code>{0}vpssecuressh</code>
<code>{0}vpsbackupmysql</code>
<code>{0}vpsmonitorcpu</code>

Modul ini menambahkan command bertema VPS, server, keamanan, monitoring, dan deployment.</b></blockquote>
"""

VPS_TOPICS = {
    "nginx": "Nginx",
    "apache": "Apache",
    "docker": "Docker",
    "pm2": "PM2",
    "nodejs": "Node.js",
    "python": "Python",
    "mysql": "MySQL",
    "postgres": "PostgreSQL",
    "redis": "Redis",
    "ufw": "UFW",
    "fail2ban": "Fail2Ban",
    "ssh": "SSH",
    "domain": "domain",
    "ssl": "SSL",
    "cron": "cron job",
    "swap": "swap",
    "disk": "disk",
    "ram": "RAM",
    "cpu": "CPU",
    "firewall": "firewall",
}

VPS_ACTIONS = {
    "check": "pengecekan",
    "install": "instalasi",
    "secure": "pengamanan",
    "backup": "backup",
    "monitor": "monitoring",
}


def build_vps_text(action_key, action_label, topic_key, topic_label):
    if action_key == "check":
        body = (
            f"Checklist {topic_label}:\n"
            f"- service status\n"
            f"- port aktif\n"
            f"- log error terakhir\n"
            f"- resource usage terkait\n"
        )
    elif action_key == "install":
        body = (
            f"Langkah instalasi {topic_label}:\n"
            f"1. update package\n"
            f"2. install service inti\n"
            f"3. enable service saat boot\n"
            f"4. cek status setelah instalasi\n"
        )
    elif action_key == "secure":
        body = (
            f"Hardening {topic_label}:\n"
            f"- ganti default config yang lemah\n"
            f"- batasi akses hanya port perlu\n"
            f"- aktifkan logging\n"
            f"- audit user dan permission\n"
        )
    elif action_key == "backup":
        body = (
            f"Strategi backup {topic_label}:\n"
            f"- tentukan file/data yang penting\n"
            f"- buat jadwal harian/mingguan\n"
            f"- simpan minimal 2 salinan\n"
            f"- lakukan restore test rutin\n"
        )
    else:
        body = (
            f"Monitoring {topic_label}:\n"
            f"- pantau uptime\n"
            f"- pantau log error\n"
            f"- pantau CPU/RAM/disk\n"
            f"- buat alert saat threshold lewat\n"
        )
    return (
        f"<blockquote><b>🖥️ {action_label.title()} {topic_label}</b>\n\n"
        f"{body}\n"
        f"Gunakan command ini sebagai catatan cepat saat kelola VPS atau server produksi.</blockquote>"
    )


def make_vps_handler(action_key, action_label, topic_key, topic_label):
    async def handler(client, message):
        await message.reply(
            build_vps_text(action_key, action_label, topic_key, topic_label),
            quote=True,
        )

    return handler


for _action_key, _action_label in VPS_ACTIONS.items():
    for _topic_key, _topic_label in VPS_TOPICS.items():
        _commands = (
            f"vps{_action_key}{_topic_key}"
            f"|server{_action_key}{_topic_key}"
            f"|host{_action_key}{_topic_key}"
        )
        _func = make_vps_handler(_action_key, _action_label, _topic_key, _topic_label)
        _func.__name__ = f"vps_{_action_key}_{_topic_key}"
        globals()[_func.__name__] = PY.UBOT(_commands)(_func)
