from AunuUbot.core.database import dumps_data, loads_data, run_db


async def get_pref(user_id: int):
    row = await run_db(
        "SELECT prefixesi FROM prefixes WHERE user_id = ?",
        (user_id,),
        fetchone=True,
    )
    if not row:
        return ["."]
    prefixes = loads_data(row["prefixesi"], ["."])
    if isinstance(prefixes, str):
        return [prefixes]
    return prefixes or ["."]


async def set_pref(user_id: int, prefix):
    if isinstance(prefix, str):
        prefix = [prefix]
    await run_db(
        """
        INSERT INTO prefixes (user_id, prefixesi)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET prefixesi = excluded.prefixesi
        """,
        (user_id, dumps_data(prefix)),
    )


async def rem_pref(user_id: int):
    await run_db("DELETE FROM prefixes WHERE user_id = ?", (user_id,))
