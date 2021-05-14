from loader import bot


@bot.command(pass_context=True)
async def info(ctx):
    text = [
        "Это сообщение служит для информации о боте в команде .info",
        "Напишите тут, что вы захотите.",
        "Команду нельзя назвать help, т.к. она будет граничить с зарезервированной командой из библиотеки discord"
    ]
    await ctx.channel.send("\n".join(text))
