from AunuUbot.core.database import dumps_data, loads_data, run_db


async def get_user_ids(client_id: int):
    row = await run_db(
        "SELECT user_ids FROM antigcast_users WHERE client_id = ?",
        (client_id,),
        fetchone=True,
    )
    if not row:
        return []
    return loads_data(row["user_ids"], [])


async def add_user_id(client_id: int, target_id: int):
    user_ids = await get_user_ids(client_id)
    if target_id not in user_ids:
        user_ids.append(target_id)
    await run_db(
        """
        INSERT INTO antigcast_users (client_id, user_ids)
        VALUES (?, ?)
        ON CONFLICT(client_id) DO UPDATE SET user_ids = excluded.user_ids
        """,
        (client_id, dumps_data(user_ids)),
    )


async def remove_user_id(client_id: int, target_id: int):
    user_ids = await get_user_ids(client_id)
    if target_id in user_ids:
        user_ids.remove(target_id)
    await run_db(
        """
        INSERT INTO antigcast_users (client_id, user_ids)
        VALUES (?, ?)
        ON CONFLICT(client_id) DO UPDATE SET user_ids = excluded.user_ids
        """,
        (client_id, dumps_data(user_ids)),
    )


async def remove_all_user_ids(client_id: int):
    await run_db("DELETE FROM antigcast_users WHERE client_id = ?", (client_id,))
