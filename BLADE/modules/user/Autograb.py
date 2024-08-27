from BLADE import bot1 as app
from pyrogram import filters
from pyrogram.types import Message
from pymongo import MongoClient
import asyncio
from config import CMD_HANDLER
# MongoDB Setup
from BLADE.Mongo import users_collection, settings_collection

# Command to add allowed user
@app.on_message(filters.me & filters.command("adduser", cmd))
async def add_user(client, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: .add_user <user_id>")
        return

    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply("Invalid user ID. It must be a number.")
        return

    users_collection.update_one({"user_id": user_id}, {"$set": {"allowed": True}}, upsert=True)
    await message.reply(f"User {user_id} added to allowed users.")

# Command to remove allowed user
@app.on_message(filters.me & filters.command("deluser", cmd))
async def del_user(client, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: .del_user <user_id>")
        return

    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply("Invalid user ID. It must be a number.")
        return

    users_collection.update_one({"user_id": user_id}, {"$set": {"allowed": False}})
    await message.reply(f"User {user_id} removed from allowed users.")

# Command to turn photo processing on or off
@app.on_message(filters.me & filters.command("autograb", cmd))
async def photo_processing(client, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: .photo_processing <on|off>")
        return

    state = message.command[1].lower()
    if state == "on":
        settings_collection.update_one({}, {"$set": {"photo_processing": True}}, upsert=True)
        await message.reply("Photo processing enabled.")
    elif state == "off":
        settings_collection.update_one({}, {"$set": {"photo_processing": False}}, upsert=True)
        await message.reply("Photo processing disabled.")
    else:
        await message.reply("Invalid option. Use 'on' or 'off'.")

# Process incoming photos from allowed users if photo_processing_enabled is True
@app.on_message(filters.incoming & filters.photo)
async def process_photo(client, message: Message):
    photo_processing_enabled = settings_collection.find_one({}, {"photo_processing": True})
    if not photo_processing_enabled or not photo_processing_enabled.get("photo_processing", False):
        return

    user = users_collection.find_one({"user_id": message.from_user.id})
    if not user or not user.get("allowed", False):
        return

    caption = message.caption or ""
    if caption.startswith("/"):
        forwarded = await message.forward("@grabbers_cheat_bot")
        
        @app.on_message(filters.chat("@grabbers_cheat_bot") & filters.reply)
        async def handle_reply(client, reply_message: Message):
            if reply_message.reply_to_message.message_id == forwarded.message_id:
                if "Copy String:" in reply_message.text.lower():
                    text_to_copy = reply_message.text.split("Copy String:")[1].strip()
                    await message.reply(text_to_copy)
        
        # Ensure the listener for the reply is set up
        await asyncio.sleep(5)  # Wait for the reply to be received
        app.remove_handler(handle_reply)

