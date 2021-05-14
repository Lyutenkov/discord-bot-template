from loader import bot, db, lobbies_dict, players_dict
from data.config import ADMINS


@bot.command(pass_context=True)
async def database(ctx):
    if str(ctx.author.id) in ADMINS:
        db_list = await db.select_all_users()
        db_list = [str(i) for i in db_list]
        print(db_list)
        str_list = "; ".join(db_list)
        await ctx.author.send(str_list)


@bot.command(pass_context=True)
async def cleaning(ctx):
    if str(ctx.author.id) in ADMINS:
        await db.cleaning_users()
        print(await db.select_all_users())


@bot.command(pass_context=True)
async def add_user(ctx):
    if str(ctx.author.id) in ADMINS:
        await db.add_user(int(ctx.message.content[10:]))
        print(await db.select_all_users())


@bot.command(pass_context=True)
async def recreate(ctx):
    if str(ctx.author.id) in ADMINS:
        await db.drop_table_users()
        await db.create_table_users()


@bot.command(pass_context=True)
async def top_players(ctx):
    if str(ctx.author.id) in ADMINS:
        await db.get_top_10()


@bot.command(pass_context=True)
async def test(ctx):
    if str(ctx.author.id) in ADMINS:
        print(await db.get_your_place())


@bot.command(pass_context=True)
async def add_score(ctx):
    if str(ctx.author.id) in ADMINS:
        await db.update_score(1, ctx.message.content[12:])


@bot.command(pass_context=True)
async def add_all_in_database(ctx):
    if str(ctx.author.id) in ADMINS:
        for user in ctx.guild.members:
            await db.add_user(user.id)


@bot.command(pass_context=True)
async def check_(ctx):
    if str(ctx.author.id) in ADMINS:
        print(f"Лобби: {lobbies_dict}\n"
              f"Игроки: {players_dict}")


@bot.command(pass_context=True)
async def get_user(ctx):
    if str(ctx.author.id) in ADMINS:
        user_id = ctx.message.content[11:]
        user = players_dict.get(str(user_id))
        print(user.printer())


@bot.command(pass_context=True)
async def delete_lobby(ctx):
    if str(ctx.author.id) in ADMINS:
        lobby_name = ctx.message.content[15:20]
        lobby_object = lobbies_dict.get(lobby_name)

        for user_id in lobby_object.users.values():
            players_dict.pop(str(user_id))

        lobbies_dict.pop(str(lobby_name))

