from AunuUbot.core.database import run_db


async def add_ubot(user_id: int, api_id: int, api_hash: str, session_string: str):
    await run_db(
        """
        INSERT INTO userbots (user_id, api_id, api_hash, session_string)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            api_id = excluded.api_id,
            api_hash = excluded.api_hash,
            session_string = excluded.session_string
        """,
        (user_id, api_id, api_hash, session_string),
    )


async def remove_ubot(user_id: int):
    await run_db("DELETE FROM userbots WHERE user_id = ?", (user_id,))


async def get_userbots():
    rows = await run_db(
        "SELECT user_id, api_id, api_hash, session_string FROM userbots",
        fetchall=True,
    ) or []
    return [
        {
            "name": str(row["user_id"]),
            "api_id": row["api_id"],
            "api_hash": row["api_hash"],
            "session_string": row["session_string"],
        }
        for row in rows
    ]
