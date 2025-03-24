from pyrogram import Client

def is_admin(user_id):
    from config import admins
    return user_id in admins
