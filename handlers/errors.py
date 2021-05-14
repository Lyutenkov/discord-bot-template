from loader import bot


# Данный вариант не совсем информативный, но помогает избежать прекращение работы бота, игнорируя ошибки,
# Но предупреждая о них в консоли (На тестах бота лучше лучше отключить данную команду)
@bot.event
async def on_command_error(ctx, exception):
    print(f"ОШИБКА!\n"
          f"CTX: {ctx.message.content}\n"
          f"CTX_AUTHOR_NAME: {ctx.author.name}\n"
          f"CTX_AUTHOR_ID: {ctx.author.id}\n"
          f"EXCEPTION: {exception}\n"
          f"CHANNEL_NAME: {ctx.channel.name}\n"
          f"CHANNEL_ID: {ctx.channel.id}")
