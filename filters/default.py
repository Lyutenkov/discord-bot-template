from data.config import ADMINS


async def default(ctx):
    """
    Этот фильтр создан в ознакомительных целях и не несет никакой смысловой нагрузки
    """
    if ctx.message.content != "stop.bot":
        return True
    else:
        if ctx.message.author.id in ADMINS:
            print("Админ хочет остановить бота!")
            return False
        else:
            return True
