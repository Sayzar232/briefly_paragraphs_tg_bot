from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services import extract_paragraphs
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


def get_books_keyboard(grade: int, subject: str):
    builder = InlineKeyboardBuilder()

    pass