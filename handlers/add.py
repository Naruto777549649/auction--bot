from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import app, admins, auction_items

@app.on_message(filters.command("add"))
async def add_item(client, message):
    buttons = [
        [InlineKeyboardButton("Legendary", callback_data="legendary"),
         InlineKeyboardButton("Non-Legendary", callback_data="nonlegendary")],
        [InlineKeyboardButton("Shiny", callback_data="shiny"),
         InlineKeyboardButton("Item", callback_data="item")]
    ]
    await message.reply_text("Choose item category:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^(legendary|nonlegendary|shiny|item)$"))
async def handle_category(client, callback_query):
    category = callback_query.data
    await callback_query.message.reply_text("Please forward Pokémon IVs page from @HeXamonbot.")
    app.set_parse_mode(category)

@app.on_message(filters.forwarded & filters.private)
async def confirm_item(client, message):
    category = app.get_parse_mode()
    auction_items.append({"user_id": message.from_user.id, "details": message.text, "category": category})
    
    for admin_id in admins:
        await client.send_message(admin_id, f"New item request:\nCategory: {category}\n{message.text}",
                                  reply_markup=InlineKeyboardMarkup([
                                      [InlineKeyboardButton("Approve", callback_data=f"approve_{len(auction_items) - 1}"),
                                       InlineKeyboardButton("Reject", callback_data=f"reject_{len(auction_items) - 1}")]
                                  ]))
    await message.reply_text("Your item has been sent for admin approval.")
