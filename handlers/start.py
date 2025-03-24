from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import app

@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("Auction Channel", url="https://t.me/God_Auction")],
        [InlineKeyboardButton("Trade Group", url="https://t.me/Trainers_union")],
        [InlineKeyboardButton("Add Items For Auction", callback_data="add_item")]
    ]
    welcome_text = """
**Hello Sir! Welcome to God Auction Bot**

I am a bot that manages auctions in God Auction.

For using me, join our channels and groups:
★ Auction Channel ➤ @God_Auction
★ Auction Trade Group ➤ @Trainers_union

Use /add to add your items for auction.
"""
    await message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("help"))
async def help(client, message):
    help_text = """
**Available Commands:**
/start - Start the bot
/add - Add an item for auction
/list - View auction items
/close - Close an auction (Admin only)
/help - Display this help message
/rules - View auction rules
/info - Get auction information
/bid - Place a bid on an item
/remove - Remove an auction item (Admin only)
/mybids - View your active bids
/contact - Contact support
/start_auction - Start the auction (Admin only)
/end_auction - End the auction (Admin only)
/broadcast - Send a message to all users (Admin only)
"""
    await message.reply_text(help_text)
