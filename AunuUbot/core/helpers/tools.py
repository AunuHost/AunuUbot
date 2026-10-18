import base64
import asyncio
import math
import os
import re
import shlex
import string
import textwrap

from io import BytesIO
from time import time
from base64 import urlsafe_b64decode
from struct import unpack
from attrify import Attrify as Atr

from gc import get_objects
from pyrogram import enums
from PIL import Image, ImageDraw, ImageFont
from pymediainfo import MediaInfo
from pyrogram.enums import ChatType
from pyrogram.errors import *


def unpackInlineMessage(inline_message_id: str):
    dc_id, message_id, chat_id, query_id = unpack(
        "<iiiq",
        urlsafe_b64decode(
            inline_message_id + "=" * (len(inline_message_id) % 4),
        ),
    )
    temp = {
        "dc_id": dc_id,
        "message_id": message_id,
        "chat_id": int(str(chat_id).replace("-1", "-1001")),
        "query_id": query_id,
        "inline_message_id": inline_message_id,
    }
    return Atr(temp)


async def extract_userid(message, text):
    def is_int(text):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()
    text = re.sub(r"^(?:https?://)?t\.me/", "", text, flags=re.IGNORECASE)
    text = text.lstrip("@").split("/", 1)[0]

    if is_int(text):
        return int(text)

    entities = message.entities or message.caption_entities
    app = message._client

    if entities is not None and len(entities) > 0:
        raw_text = message.text or message.caption or ""
        first_is_slash = raw_text.startswith("/")
        entity = entities[1 if first_is_slash else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            try:
                user = await app.get_users(text)
            except (UsernameInvalid, PeerIdInvalid, UsernameNotOccupied):
                return None
            if user is not None:
                return user.id
        elif entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id

    try:
        user = await app.get_users(text)
    except (UsernameInvalid, PeerIdInvalid, UsernameNotOccupied):
        return None
    if user is not None:
        return user.id

    return None


async def extract_user_and_reason(message, sender_chat=False):
    raw_text = message.text or message.caption or ""
    args = raw_text.strip().split()
    user = None
    reason = None

    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user and (reply.sender_chat and reply.sender_chat != message.chat.id and sender_chat):
            id_ = reply.sender_chat.id
        elif reply.from_user:
            id_ = reply.from_user.id
        else:
            return None, None

        reason = ' '.join(args[1:]) if len(args) > 1 else None
        return id_, reason

    if len(args) >= 2:
        user = ' '.join(args[1:])
        return await extract_userid(message, user), None

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


admins_in_chat = {}


async def list_admins(message):
    global admins_in_chat
    if message.chat.id in admins_in_chat:
        interval = time() - admins_in_chat[message.chat.id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[message.chat.id]["data"]

    admins_in_chat[message.chat.id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in message._client.get_chat_members(
                message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[message.chat.id]["data"]
