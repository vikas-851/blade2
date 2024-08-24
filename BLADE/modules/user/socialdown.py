import asyncio
import os

from pyrogram import Client, enums, filters, raw
from pyrogram.types import Message

from config import CMD_HANDLER
from BLADE import *
from BLADE.helpers.basic import edit_or_reply
from BLADE.helpers.PyroHelpers import ReplyCheck
from BLADE.helpers.tools import get_arg
from BLADE.utils import s_paste

from .help import *

import requests


@Client.on_message(filters.command(["tt", "tiktok", "ig", "sosmed"], cmd) & filters.me)
async def sosmed(client: Client, message: Message):
    Man = await message.edit("`Processing Please Wait My Master✨ Give me only 5-10 Seconds Done Now Go to @MultiSaverXbot . . .`")
    link = get_arg(message)
    bot = "MultiSaverXbot"
    if link:
        try:
            xnxx = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await xnxx.delete()
        except YouBlockedUser:
            await client.unblock_user(bot)
            xnxx = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await xnxx.delete()
    async for sosmed in client.search_messages(
        bot, filter=enums.MessagesFilter.VIDEO, limit=1
    ):
        await asyncio.gather(
            Man.delete(),
            client.send_video(
                message.chat.id,
                sosmed,
                caption=f"**Upload by:** {client.me.mention}",
                reply_to_message_id=ReplyCheck(message),
            ),
        )
        await client.delete_messages(bot, 2)



add_command_help(
    "•─╼⃝𖠁 ꜱᴏꜱᴍᴇᴅ",
    [
        [
            f"sosmed <ʟɪɴᴋ>",
            "Tᴏ Dᴏᴡɴʟᴏᴀᴅ Mᴇᴅɪᴀ Fʀᴏᴍ Fᴀᴄᴇʙᴏᴏᴋ / Tɪᴋᴛᴏᴋ / Iɴꜱᴛᴀɢʀᴀᴍ / Tᴡɪᴛᴛᴇʀ / YᴏᴜTᴜʙᴇ.",
        ],
    ],
  ) 
