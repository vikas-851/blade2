import random
from BLADE import app
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from config import OWNER_ID as owner 

@app.on_callback_query()
def pmowner(client, callback_query):
    user_id = owner
    message = "A Pᴏᴡᴇʀғᴜʟ Assɪᴛᴀɴᴛ blade has been started!!!!"
    client.send_message(user_id, message)
    client.answer_callback_query(callback_query.id, text="Message sent")

logoX = [
    "https://telegra.ph/file/c8e18f003f896048ce12d.jpg"
]

alive_logo = random.choice(logoX)

@app.on_message(filters.command("start") & filters.private)
async def start(app, message):
    chat_id = message.chat.id
    file_id = alive_logo
    caption = "Hello, Mʏ Mᴀsᴛᴇʀ!!\nNice To Meet You 🤗 !!\nI guess, that you know me, Uhh you don't, np..\nWell.\n\nA Pᴏᴡᴇʀғᴜʟ Assɪᴛᴀɴᴛ \n\n Pᴏᴡᴇʀᴇᴅ Bʏ [BLADES](t.me/blade_x_community)\n\nYᴏᴜ Cᴀɴ Cʜᴀᴛ Wɪᴛʜ Mʏ Mᴀsᴛᴇʀ Tʜʀᴏᴜɢʜ Tʜɪs Bᴏᴛ.\nIғ Yᴏᴜ Wᴀɴᴛ Yᴏᴜʀ Oᴡɴ Assɪᴛᴀɴᴛ Yᴏᴜ Cᴀɴ Dᴇᴘʟᴏʏ Fʀᴏᴍ Bᴜᴛᴛᴏɴ Bᴇʟᴏᴡ."
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/BLADE_X_SUPPORT"),
            InlineKeyboardButton("𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url="https://t.me/BLADE_x_community"),
            InlineKeyboardButton("𝐎𝐰𝐧𝐞𝐫", url="https://t.me/alone_x_hater"),
        ],
    ])

    await app.send_photo(chat_id, file_id, caption=caption, reply_markup=reply_markup)
