from pyrogram import filters
from config import app, admins

@app.on_message(filters.command("broadcast") & filters.user(admins))
async def broadcast(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /broadcast <message>")
        return

    broadcast_message = message.text.split(' ', 1)[1]
    total_users = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    async for user in app.iter_users():
        total_users += 1
        try:
            await app.send_message(user.id, broadcast_message)
            successful += 1
        except Exception as e:
            if "user is deactivated" in str(e):
                deleted += 1
            elif "bot was blocked" in str(e):
                blocked += 1
            else:
                unsuccessful += 1

    report = f"""
Broadcast completed

◇ Total Users: {total_users}
◇ Successful: {successful}
◇ Blocked Users: {blocked}
◇ Deleted Accounts: {deleted}
◇ Unsuccessful: {unsuccessful}
"""
    await message.reply_text(report)
