import asyncio

from handlers import bot
from data.config import BOT_TOKEN

if __name__ == "__main__":
    asyncio.run(bot.run(BOT_TOKEN))
