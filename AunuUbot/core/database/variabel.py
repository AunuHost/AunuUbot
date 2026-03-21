from typing import List, Optional, Union

from AunuUbot.core.database import dumps_data, loads_data, run_db


async def _get_query_data(user_id: int, query: str = "vars") -> dict:
    row = await run_db(
        "SELECT data FROM vars_store WHERE user_id = ? AND query_name = ?",
        (user_id, query),
        fetchone=True,
    )
    return loads_data(row["data"], {}) if row else {}


async def _set_query_data(user_id: int, query: str, data: dict):
    await run_db(
        """
        INSERT INTO vars_store (user_id, query_name, data)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, query_name) DO UPDATE SET data = excluded.data
        """,
        (user_id, query, dumps_data(data)),
    )


async def set_vars(user_id: int, vars_name: str, value: Union[int, str], query: str = "vars"):
    data = await _get_query_data(user_id, query)
    data[vars_name] = value
    await _set_query_data(user_id, query, data)


async def get_vars(user_id: int, vars_name: str, query: str = "vars") -> Optional[Union[int, str]]:
    data = await _get_query_data(user_id, query)
    return data.get(vars_name)


async def remove_vars(user_id: int, vars_name: str, query: str = "vars"):
    data = await _get_query_data(user_id, query)
    if vars_name in data:
        del data[vars_name]
        if data:
            await _set_query_data(user_id, query, data)
        else:
            await run_db(
                "DELETE FROM vars_store WHERE user_id = ? AND query_name = ?",
                (user_id, query),
            )


async def all_vars(user_id: int, query: str = "vars") -> Optional[dict]:
    data = await _get_query_data(user_id, query)
    return data or None


async def remove_all_vars(user_id: int):
    await run_db("DELETE FROM vars_store WHERE user_id = ?", (user_id,))


async def get_list_from_vars(user_id: int, vars_name: str, query: str = "vars") -> List[int]:
    vars_data = await get_vars(user_id, vars_name, query)
    values = [int(x) for x in str(vars_data).split()] if vars_data else []
    if vars_name == "ADMIN_USERS":
        from AunuUbot.config import OWNER_ID

        if OWNER_ID not in values:
            values.append(OWNER_ID)
    return values


async def add_to_vars(user_id: int, vars_name: str, value: int, query: str = "vars"):
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    if value not in vars_list:
        vars_list.append(value)
    await set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)


async def remove_from_vars(user_id: int, vars_name: str, value: int, query: str = "vars"):
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    if value in vars_list:
        vars_list.remove(value)
        await set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)


async def get_pm_id(user_id: int) -> List[int]:
    pm_id = await get_vars(user_id, "PM_PERMIT")
    return [int(x) for x in str(pm_id).split()] if pm_id else []


async def add_pm_id(me_id: int, user_id: int):
    pm_id = await get_vars(me_id, "PM_PERMIT")
    if pm_id:
        user_id = f"{pm_id} {user_id}"
    await set_vars(me_id, "PM_PERMIT", user_id)


async def remove_pm_id(me_id: int, user_id: int):
    pm_id = await get_vars(me_id, "PM_PERMIT")
    if pm_id:
        list_id = [int(x) for x in str(pm_id).split() if x != str(user_id)]
        await set_vars(me_id, "PM_PERMIT", " ".join(map(str, list_id)))


async def set_status(user_id, status):
    await set_vars(user_id, "WORD_DETECTION_STATUS", status)


async def get_status(user_id):
    status = await get_vars(user_id, "WORD_DETECTION_STATUS")
    return status if status is not None else False
