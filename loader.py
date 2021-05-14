import discord
from discord.ext import commands
from utils.db_api.postgres import Database


db = Database()


from filters import default


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.add_check(default)
