from loader import bot
from data.config import ADMINS


@bot.command(pass_context=True)
async def database(ctx):
    if str(ctx.author.id) in ADMINS:
        await ctx.channel.send("Это команда для администраторов!")
