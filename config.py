import os
from pyrogram import Client

api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

admins = list(map(int, os.environ.get("ADMINS", "").split(",")))

app = Client("auction_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

auction_active = False
auction_items = []
user_bids = {}