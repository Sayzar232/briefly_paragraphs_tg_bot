import aiosqlite
import datetime
from config import DATABASE_NAME

async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                registration_date TEXT
            )
        ''')
        await db.commit()

async def add_user(user_id: int, username: str, full_name: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        registration_date = datetime.datetime.now().isoformat()
        await db.execute(
            "INSERT OR IGNORE INTO users (id, username, full_name, registration_date) VALUES (?, ?, ?, ?)",
            (user_id, username, full_name, registration_date)
        )
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = await cursor.fetchone()
        return user

async def get_all_users():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        return users


async def get_user_count() -> int:
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        row = await cursor.fetchone()
        return row[0] if row else 0
