from typing import Union

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.__pool: Union[Pool, None] = None

    async def get_pool(self):
        await self.__create_connection()
        return self.__pool

    async def __create_connection(self):
        self.__pool = self.__pool or await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        pool = await self.get_pool()
        async with pool.acquire() as connection:
            # connection: Connection
            # async with connection.transaction():
            if fetch:
                result = await connection.fetch(command, *args)
            elif fetchval:
                result = await connection.fetchval(command, *args)
            elif fetchrow:
                result = await connection.fetchrow(command, *args)
            elif execute:
                result = await connection.execute(command, *args)
        return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())
    """
    ТАБЛИЦА Users
    """
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        discord_id BIGINT NOT NULL UNIQUE,
        count_games INT DEFAULT 0,
        score INT DEFAULT 0
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, discord_id):
        sql = """
        INSERT INTO users (discord_id) VALUES($1) ON CONFLICT DO NOTHING returning *
        """
        await self.execute(sql, discord_id, fetchrow=True)

    async def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = """
        SELECT * FROM users WHERE 
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_count_games(self, discord_id):
        sql = f"""
        UPDATE users SET count_games=count_games+1 WHERE discord_id={discord_id}
        """
        return await self.execute(sql, execute=True)

    async def update_score(self, point, discord_id):
        sql = f"""
        UPDATE users SET score=score+{point} WHERE discord_id={discord_id}
        """
        return await self.execute(sql, execute=True)

    async def get_top_10(self):
        sql = """
        SELECT * FROM users ORDER BY score DESC LIMIT 10
        """
        return await self.execute(sql, fetch=True)

    async def get_your_place(self, discord_id):
        sql = f"""
        SELECT 
        * 
        FROM (
        SELECT 
        *, row_number() OVER (ORDER BY score DESC NULLS LAST) AS idx 
        FROM 
        users 
        ORDER BY 
        score DESC
        ) as t 
        WHERE 
        t.discord_id={discord_id}
        """
        return await self.execute(sql, fetchrow=True)

    async def count_users(self):
        sql = """
        SELECT COUNT(*) FROM users
        """
        return await self.execute(sql, fetchval=True)

    async def cleaning_users(self):
        sql = """
        DELETE FROM users WHERE TRUE
        """
        return await self.execute(sql, execute=True)

    async def drop_table_users(self):
        sql = """
        DROP TABLE IF EXISTS users
        """
        return await self.execute(sql, execute=True)
    """
    ТАБЛИЦА lobbies
    """
    async def create_table_lobbies(self):
        sql = """
        CREATE TABLE IF NOT EXISTS lobbies(
        id SERIAL PRIMARY KEY,
        id_lobby INTEGER,
        server_id BIGINT NOT NULL,
        users INTEGER[],
        status INTEGER NOT NULL DEFAULT 0
        );
        """
        await self.execute(sql, execute=True)

    async def add_lobby(self, id_lobby, server_id):
        sql = """
        INSERT INTO lobbies (id_lobby, server_id) VALUES($1, $2) returning *
        """
        await self.execute(sql, id_lobby, server_id, fetchrow=True)

    async def select_all_lobbies(self):
        sql = """
        SELECT * FROM lobbies
        """
        return await self.execute(sql, fetch=True)

    async def select_lobby(self, **kwargs):
        sql = """
        SELECT * FROM lobbies WHERE 
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_lobbies(self):
        sql = """
        SELECT COUNT(*) FROM lobbies
        """
        return await self.execute(sql, fetchval=True)
    """
    ТАБЛИЦА lobbies
    """
    async def create_table_servers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS servers(
        id INTEGER PRIMARY KEY,
        server_id BIGINT NOT NULL,
        status INTEGER NOT NULL DEFAULT 1
        );
        """
        await self.execute(sql, execute=True)

    async def add_server(self, server_id):
        sql = """
        INSERT INTO servers (server_id) VALUES($1) returning *
        """
        await self.execute(sql, server_id, fetchrow=True)

    async def select_all_servers(self):
        sql = """
        SELECT * FROM servers
        """
        return await self.execute(sql, fetch=True)

    async def select_server(self, **kwargs):
        sql = """
        SELECT * FROM servers WHERE 
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_servers(self):
        sql = """
        SELECT COUNT(*) FROM servers
        """
        return await self.execute(sql, fetchval=True)
