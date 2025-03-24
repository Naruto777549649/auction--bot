from pyrogram import Client

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

admins = [123456789, 987654321]  # Add Admin IDs

app = Client("auction_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

auction_active = False
auction_items = []
user_bids = {}
