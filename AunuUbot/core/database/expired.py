from datetime import datetime

from AunuUbot.core.database import run_db


async def get_expired_date(user_id: int):
    row = await run_db(
        "SELECT expire_date FROM expired_users WHERE user_id = ?",
        (user_id,),
        fetchone=True,
    )
    if not row or not row["expire_date"]:
        return None
    try:
        return datetime.fromisoformat(row["expire_date"])
    except ValueError:
        return None


async def set_expired_date(user_id: int, expire_date):
    value = expire_date.isoformat() if hasattr(expire_date, "isoformat") else str(expire_date)
    await run_db(
        """
        INSERT INTO expired_users (user_id, expire_date)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET expire_date = excluded.expire_date
        """,
        (user_id, value),
    )


async def rem_expired_date(user_id: int):
    await run_db("DELETE FROM expired_users WHERE user_id = ?", (user_id,))
