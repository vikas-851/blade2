from BLADE import bot1 as app
from pyrogram import filters
from pyrogram.types import Message
from pymongo import MongoClient
import asyncio

# MongoDB Setup
client = MongoClient("mongodb+srv://naruto:hinatababy@cluster0.rqyiyzx.mongodb.net/")
db = client["my_database"]
users_collection = db["users"]
settings_collection = db["settings"]

# 
