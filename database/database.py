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

            await conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    subject VARCHAR(255) NOT NULL,
                    grade INT NOT NULL,
                    authors VARCHAR(255) NOT NULL,
                    publisher VARCHAR(255),
                    edition VARCHAR(255) NOT NULL,
                    pages INT NOT NULL,
                    url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                '''
            )

            await conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS paragraphs (
                    id SERIAL PRIMARY KEY,
                    book_id INT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
                    paragraph_number INT NOT NULL,
                    title VARCHAR(255),
                    pages VARCHAR(255) NOT NULL,
                    text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                '''
            )

            await conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS summaries (
                    id SERIAL PRIMARY KEY,
                    paragraph_id INT NOT NULL REFERENCES paragraphs(id) ON DELETE CASCADE,
                    summary TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    questions TEXT
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

    async def ensure_book(
        self,
        subject: str,
        grade: int,
        authors: str,
        publisher: str,
        edition: str,
        pages: int,
        url: str
    ):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id FROM books
                WHERE subject = $1 AND grade = $2 AND authors = $3 AND publisher = $4 AND edition = $5;
                """,
                subject, grade, authors, publisher, edition
            )

            if row is None:
                row = await conn.fetchrow(
                    """
                    INSERT INTO books (subject, grade, authors, publisher, edition, pages, url)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    RETURNING id;
                    """,
                    subject, grade, authors, publisher, edition, pages, url
                )

            return row['id']

    async def add_paragraph(
            self,
            book_id: int,
            paragraph_number: int,
            title: str,
            pages: str,
            text: str
        ):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id FROM paragraphs
                WHERE book_id = $1 AND paragraph_number = $2;
                """,
                book_id, paragraph_number
            )
            if row is None:
                await conn.execute(
                    """
                    INSERT INTO paragraphs (book_id, paragraph_number, title, pages, text)
                    VALUES ($1, $2, $3, $4, $5);
                    """,
                    book_id, paragraph_number, title, pages, text
                )

    async def get_books(self, grade: int, subject: str):
        async with self.pool.acquire() as conn:
            books = await conn.fetch(
                "SELECT id, authors, edition FROM books WHERE grade = $1 AND subject = $2;",
                grade, subject
            )

            return [dict(row) for row in books]

    async def get_subjects(self, grade: int):
        async with self.pool.acquire() as conn:
            subjects = await conn.fetch(
                "SELECT DISTINCT subject FROM books WHERE grade = $1;",
                grade
            )

            return [row["subject"] for row in subjects]

    async def get_paragraphs(self, book_id):
        async with self.pool.acquire() as conn:
            paragraphs = await conn.fetch(
                "SELECT paragraph_number, title FROM paragraphs WHERE book_id = $1 ORDER BY paragraph_number;",
                book_id
            )

            return [dict(row) for row in paragraphs]

    async def get_paragraph(self, book_id: int, paragraph_number: int):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, paragraph_number, title, pages, text
                FROM paragraphs
                WHERE book_id = $1 AND paragraph_number = $2;
                """,
                book_id, paragraph_number
            )

            return dict(row) if row else None

db = Database()