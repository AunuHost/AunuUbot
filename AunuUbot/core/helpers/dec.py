import asyncio
from pyrogram.enums import ChatType
from AunuUbot import *

chat_type = {
    "group": [ChatType.GROUP, ChatType.SUPERGROUP],
    "users": [ChatType.PRIVATE],
}

async def get_private_and_group_chats(client):
    pm_chats = []
    gc_chats = []

    async for dialog in client.get_dialogs(limit=None):
        try:
            if dialog.chat.type in chat_type.get("users"):
                pm_chats.append(dialog.chat.id)
            elif dialog.chat.type in chat_type.get("group"):
                gc_chats.append(dialog.chat.id)
        except Exception as e:
            print(f"[INFO]: {e}")

    return pm_chats, gc_chats


async def install_my_peer(client):
    pm_chats, gc_chats = await get_private_and_group_chats(client)
    client_id = client.me.id
    client._get_my_peer[client_id] = {"pm": pm_chats, "gc": gc_chats}


async def installPeer():
    tasks = [install_my_peer(client) for client in ubot._ubot]
    await asyncio.gather(*tasks, return_exceptions=True)



