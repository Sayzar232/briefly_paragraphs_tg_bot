import asyncpg
from config import DATABASE_URL


class Database:
    def __init__(
        self,
        dsn: str = None,
        min_size: int = 1,
        max_size: int = 10,
        command_timeout: int = 60,
    ):
        self.dsn = dsn if dsn is not None else DATABASE_URL
        self._min_size = min_size
        self._max_size = max_size
        self._command_timeout = command_timeout
        self.pool = None

    async def initialize(self):
        """Создаёт пул соединений и таблицы, если их ещё нет."""
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self._min_size,
            max_size=self._max_size,
            command_timeout=self._command_timeout,
        )

        await self._create_tables()

    async def _create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    registration_date TIMESTAMP DEFAULT NOW()
                );
                '''
            )

    async def add_user(self, user_id: int, username: str, full_name: str):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (id, username, full_name)
                VALUES ($1, $2, $3)
                ON CONFLICT (id) DO NOTHING;
                """,
                user_id, username, full_name,
            )

    async def get_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM users WHERE id = $1;", user_id)
            return row

    async def get_all_users(self):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM users;")
            return rows

    async def get_user_count(self) -> int:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT COUNT(*) FROM users;")
            return row[0] if row else 0


db = Database()