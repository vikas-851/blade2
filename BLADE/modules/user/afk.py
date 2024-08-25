import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import CMD_HANDLER
from BLADE import BOTLOG_CHATID
from BLADE.helpers.msg_types import Types, get_message_type
from BLADE.helpers.parser import escape_markdown, mention_markdown
from BLADE.helpers.SQL.afk_db import get_afk, set_afk

# Set priority to 11 and 12
MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 3  # seconds

@Client.on_message(filters.me & filters.command("afk", CMD_HANDLER))
async def afk(client: Client, message: Message):
    if len(message.text.split()) >= 2:
        reason = message.text.split(None, 1)[1]
        set_afk(True, reason)
        await message.edit(
            f"❏ {mention_markdown(message.from_user.id, message.from_user.first_name)} "
            f"<b>is now AFK!</b>\n└ <b>Reason:</b> <code>{reason}</code>"
        )
    else:
        set_afk(True, "")
        await message.edit(
            f"✘ {mention_markdown(message.from_user.id, message.from_user.first_name)} <b>is now AFK</b> ✘"
        )
    await message.stop_propagation()

@Client.on_message(
    (filters.mentioned | filters.private) & filters.incoming & ~filters.bot, group=11
)
async def afk_mentioned(client: Client, message: Message):
    global MENTIONED
    afk_status = get_afk()
    if afk_status and afk_status["afk"]:
        cid = str(message.chat.id)[4:] if "-" in str(message.chat.id) else str(message.chat.id)

        if cid in AFK_RESTIRECT and int(AFK_RESTIRECT[cid]) >= int(time.time()):
            return
        
        AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME

        # Determine the message text
        if afk_status["reason"]:
            afk_reply = (
                f"❏ {client.me.mention} <b>is currently AFK!</b>\n└ <b>Reason:</b> <code>{afk_status['reason']}</code>"
            )
        else:
            afk_reply = f"<b>Sorry</b>, {client.me.first_name} <b>is currently AFK!</b>"

        await message.reply(afk_reply)

        _, message_type = get_message_type(message)
        
        # Determine text from different message types
        if message_type == Types.TEXT:
            text = message.text or message.caption
        elif message_type in [Types.PHOTO, Types.VIDEO, Types.ANIMATION]:
            text = message.caption or f"{message_type.name} received"
        else:
            text = message_type.name

        MENTIONED.append({
            "user": message.from_user.first_name,
            "user_id": message.from_user.id,
            "chat": message.chat.title,
            "chat_id": cid,
            "text": text,
            "message_id": message.id,
        })

        try:
            await client.send_message(
                BOTLOG_CHATID,
                f"<b>#MENTION\n • From:</b> {message.from_user.mention}\n"
                f"• <b>Group:</b> <code>{message.chat.title}</code>\n"
                f"• <b>Message:</b> <code>{text[:3500]}</code>"
            )
        except Exception as e:
            print(f"Error sending log message: {e}")

@Client.on_message(filters.me & filters.group, group=12)
async def no_longer_afk(client: Client, message: Message):
    global MENTIONED
    afk_status = get_afk()
    if afk_status and afk_status["afk"]:
        set_afk(False, "")
        try:
            await client.send_message(BOTLOG_CHATID, "You are no longer AFK!")
        except Exception as e:
            print(f"Error sending log message: {e}")

        text = f"<b>Total {len(MENTIONED)} mentions while AFK:</b>\n"
        for mention in MENTIONED:
            msg_text = (mention["text"][:11] + "...") if len(mention["text"]) >= 11 else mention["text"]
            text += (
                f"- [{escape_markdown(mention['user'])}](https://t.me/c/"
                f"{mention['chat_id']}/{mention['message_id']}) ({mention['chat']}): {msg_text}\n"
            )

        try:
            await client.send_message(BOTLOG_CHATID, text)
        except Exception as e:
            print(f"Error sending log message: {e}")

        MENTIONED.clear()
