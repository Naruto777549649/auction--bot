from config import app
from handlers import start, add, auction, broadcast, bids

if __name__ == "__main__":
    print("Bot is running...")
    app.run()