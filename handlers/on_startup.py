from loader import bot


@bot.event
async def on_ready():
    print("Бот успешно залогинился!")
