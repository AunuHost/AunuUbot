import asyncio
import json
import os
import sqlite3
from contextlib import closing

from AunuUbot.config import LOCAL_DB_PATH


def _resolve_db_path() -> str:
    if os.path.isabs(LOCAL_DB_PATH):
        return LOCAL_DB_PATH
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    return os.path.abspath(os.path.join(base_dir, LOCAL_DB_PATH))


DB_PATH = _resolve_db_path()
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    with closing(_connect()) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS prefixes (
                user_id INTEGER PRIMARY KEY,
                prefixesi TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS userbots (
                user_id INTEGER PRIMARY KEY,
                api_id INTEGER NOT NULL,
                api_hash TEXT NOT NULL,
                session_string TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS vars_store (
                user_id INTEGER NOT NULL,
                query_name TEXT NOT NULL,
                data TEXT NOT NULL,
                PRIMARY KEY (user_id, query_name)
            );

            CREATE TABLE IF NOT EXISTS expired_users (
                user_id INTEGER PRIMARY KEY,
                expire_date TEXT
            );

            CREATE TABLE IF NOT EXISTS antigcast_users (
                client_id INTEGER PRIMARY KEY,
                user_ids TEXT NOT NULL
            );
            """
        )
        conn.commit()


_init_db()


async def run_db(query: str, params=(), fetchone: bool = False, fetchall: bool = False):
    def _runner():
        with closing(_connect()) as conn:
            cursor = conn.execute(query, params)
            result = None
            if fetchone:
                row = cursor.fetchone()
                result = dict(row) if row else None
            elif fetchall:
                result = [dict(row) for row in cursor.fetchall()]
            conn.commit()
            return result

    return await asyncio.to_thread(_runner)


def dumps_data(value):
    return json.dumps(value, ensure_ascii=True)


def loads_data(value, default=None):
    if value is None:
        return default
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return default


from AunuUbot.core.database.expired import *
from AunuUbot.core.database.userbot import *
from AunuUbot.core.database.pref import *
from AunuUbot.core.database.variabel import *
from AunuUbot.core.database.antigcast import *
