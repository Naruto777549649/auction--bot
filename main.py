from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

app = Client("auction_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Admins List (Add Admin IDs Here)
admins = [123456789, 987654321]

auction_active = False
auction_items = []
user_bids = []

# Start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("Auction Channel", url="https://t.me/God_Auction")],
        [InlineKeyboardButton("Trade Group", url="https://t.me/Trainers_union")],
        [InlineKeyboardButton("Add Items For Auction", callback_data="add_item")]
    ]
    await message.reply_text(
        "**Hello Sir! Welcome to God Auction Bot**\n\n"
        "I am a bot that manages auctions in God Auction.\n\n"
        "For using me, join our channels and groups:\n"
        "★ Auction Channel ➤ @God_Auction\n"
        "★ Auction Trade Group ➤ @Trainers_union\n\n"
        "Use /add to add your items for auction.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Add Command
@app.on_message(filters.command("add"))
async def add_item(client, message):
    if message.from_user.id not in admins:
        buttons = [
            [InlineKeyboardButton("Legendary", callback_data="legendary")],
            [InlineKeyboardButton("Non-Legendary", callback_data="non_legendary")],
            [InlineKeyboardButton("Shiny", callback_data="shiny")],
            [InlineKeyboardButton("Item", callback_data="item")]
        ]
        await message.reply_text("Select the category of the auction item:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^(legendary|non_legendary|shiny|item)$"))
async def category_selected(client, callback_query):
    await callback_query.message.reply_text("Please forward Pokémon IVs page from @HeXamonbot")
    category = callback_query.data
    app.set_user_data(callback_query.from_user.id, "category", category)

@app.on_message(filters.forwarded & filters.private)
async def handle_forwarded_message(client, message):
    category = app.get_user_data(message.from_user.id, "category")
    if category:
        buttons = [
            [InlineKeyboardButton("Yes", callback_data="confirm_item")],
            [InlineKeyboardButton("No", callback_data="cancel_item")]
        ]
        await message.reply_text(f"Confirm this {category} for auction?", reply_markup=InlineKeyboardMarkup(buttons))
        app.set_user_data(message.from_user.id, "forwarded_message", message)

@app.on_callback_query(filters.regex("^(confirm_item|cancel_item)$"))
async def confirm_item(client, callback_query):
    if callback_query.data == "confirm_item":
        message = app.get_user_data(callback_query.from_user.id, "forwarded_message")
        category = app.get_user_data(callback_query.from_user.id, "category")

        # Notify Admins for Approval
        for admin in admins:
            buttons = [
                [InlineKeyboardButton("Approve", callback_data=f"approve_{message.message_id}")],
                [InlineKeyboardButton("Reject", callback_data=f"reject_{message.message_id}")]
            ]
            await app.send_message(admin, f"New {category} for Auction by @{callback_query.from_user.username}:", reply_markup=InlineKeyboardMarkup(buttons))
        
        await callback_query.message.reply_text("Item sent for admin approval!")
    else:
        await callback_query.message.reply_text("Item addition canceled.")

@app.on_callback_query(filters.regex("^approve_"))
async def approve_item(client, callback_query):
    message_id = int(callback_query.data.split("_")[1])
    message = await app.get_messages(callback_query.message.chat.id, message_id)

    auction_items.append(message)
    await callback_query.message.reply_text("Item approved and posted to the auction channel.")
    await app.send_message("@God_Auction", f"Auction Item:\n{message.text}")

@app.on_callback_query(filters.regex("^reject_"))
async def reject_item(client, callback_query):
    await callback_query.message.reply_text("Item rejected successfully.")

# List Command
@app.on_message(filters.command("list"))
async def list_items(client, message):
    if not auction_items:
        await message.reply_text("No items available for auction.")
        return
    
    text = "\n".join([f"{i+1}. {item.text}" for i, item in enumerate(auction_items)])
    await message.reply_text(f"Current Auction Items:\n{text}")

# Start Auction Command
@app.on_message(filters.command("start_auction"))
async def start_auction(client, message):
    if message.from_user.id in admins:
        global auction_active
        auction_active = True
        await message.reply_text("Auction started! Users can now place bids.")

# End Auction Command
@app.on_message(filters.command("end_auction"))
async def end_auction(client, message):
    if message.from_user.id in admins:
        global auction_active
        auction_active = False
        await message.reply_text("Auction ended! No more bids are allowed.")

# Bid Command
@app.on_message(filters.command("bid"))
async def place_bid(client, message):
    global auction_active
    if not auction_active:
        await message.reply_text("Auction is not active right now.")
        return
    bid_amount = message.text.split(" ", 1)[1]
    user_bids.append((message.from_user.id, bid_amount))
    await message.reply_text(f"Your bid of {bid_amount} has been placed!")

# Broadcast Command
@app.on_message(filters.command("broadcast"))
async def broadcast(client, message):
    if message.from_user.id not in admins:
        return
    
    broadcast_text = message.text.split(" ", 1)[1]
    sent, failed, blocked, deleted = 0, 0, 0, 0
    
    async for user in app.get_users():
        try:
            await app.send_message(user.id, broadcast_text)
            sent += 1
        except Exception as e:
            if "blocked" in str(e):
                blocked += 1
            elif "deleted" in str(e):
                deleted += 1
            failed += 1

    await message.reply_text(
        f"Broadcast completed\n"
        f"◇ Total Users: {sent + failed}\n"
        f"◇ Successful: {sent}\n"
        f"◇ Blocked Users: {blocked}\n"
        f"◇ Deleted Accounts: {deleted}\n"
        f"◇ Unsuccessful: {failed}"
    )

# Run the Bot
print("Auction Bot is running...")
app.run()
