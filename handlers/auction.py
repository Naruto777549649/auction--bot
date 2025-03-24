from pyrogram import filters
from config import app, auction_active, admins

@app.on_message(filters.command("start_auction") & filters.user(admins))
async def start_auction(client, message):
    global auction_active
    auction_active = True
    await message.reply_text("Auction started. Users can now place bids.")

@app.on_message(filters.command("end_auction") & filters.user(admins))
async def end_auction(client, message):
    global auction_active
    auction_active = False
    await message.reply_text("Auction ended. No further bids will be accepted.")
