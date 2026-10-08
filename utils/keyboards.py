from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import db


def get_grades_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="5 Класс", callback_data="grade_5"))
    builder.add(InlineKeyboardButton(text="6 Класс", callback_data="grade_6"))
    builder.add(InlineKeyboardButton(text="7 Класс", callback_data="grade_7"))
    builder.add(InlineKeyboardButton(text="8 Класс", callback_data="grade_8"))
    builder.add(InlineKeyboardButton(text="9 Класс", callback_data="grade_9"))
    builder.add(InlineKeyboardButton(text="10 Класс", callback_data="grade_10"))
    builder.add(InlineKeyboardButton(text="11 Класс", callback_data="grade_11"))

    builder.adjust(1)
    return builder.as_markup()


async def get_subjects_keyboard(grade: int):
    subjects = await db.get_subjects(grade)

    builder = InlineKeyboardBuilder()

    for subject in subjects:
        builder.add(InlineKeyboardButton(text=f"{subject}", callback_data=f"subject_{subject}"))

    builder.adjust(1)
    return builder.as_markup()


async def get_books_keyboard(grade: int, subject: str):
    builder = InlineKeyboardBuilder()

    books = await db.get_books(grade, subject)

    for book in books:
        book_id = book["id"]
        book_authors = book["authors"]

        builder.add(InlineKeyboardButton(text=f"{book_authors}", callback_data=f"book_{book_id}"))

    builder.adjust(1)
    return builder.as_markup()


async def get_paragraphs_keyboard(book_id: int):
    paragraphs = await db.get_paragraphs(book_id)

    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []

    for paragraph in paragraphs:
        number = paragraph["paragraph_number"]
        title = paragraph.get("title") or ""

        text = f"{number}. {title}" if title else f"§ {number}"

        # Telegram даёт не больше 64 символов на текст кнопки
        if len(text) > 64:
            text = text[:63].rstrip() + "…"

        row.append(InlineKeyboardButton(text=text, callback_data=f"paragraph_{number}"))

        if len(row) == 5:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    rows.append([InlineKeyboardButton(text="⬅️ Назад к книгам", callback_data="back_books")])

    return InlineKeyboardMarkup(inline_keyboard=rows)