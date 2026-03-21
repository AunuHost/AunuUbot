import os
from dotenv import load_dotenv

load_dotenv(".env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAX_BOT = int(os.getenv("MAX_BOT", "10"))

DEVS = list(map(int, os.getenv("DEVS", "8565893997").split()))

API_ID = int(os.getenv("API_ID", "29289753"))

API_HASH = os.getenv("API_HASH", "3f209b867db1920f5246bf523246fd74")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

OWNER_ID = int(os.getenv("OWNER_ID", "8565893997"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "").split()))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

LOCAL_DB_PATH = os.getenv(
    "LOCAL_DB_PATH",
    os.path.join(BASE_DIR, "storage", "aunuhost_local.db"),
)

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-3867220417"))

USER_GROUP = os.getenv("USER_GROUP", "https://t.me/AunuHostv")
