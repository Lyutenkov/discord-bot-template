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
        discord_id BIGINT NOT NULL UNIQUE
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
