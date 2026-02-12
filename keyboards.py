from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from parser import extract_paragraphs

def get_paragraphs_keyboard(url):
    """Return keyboard with paragraphs"""
    paragraphs = extract_paragraphs(url)
    builder = InlineKeyboardBuilder()
    for paragraph in paragraphs:
        builder.add(InlineKeyboardButton(text=paragraph, callback_data=f"paragraph_{paragraph}"))

    builder.adjust(1)  # one button per row-

    return builder.as_markup()


books_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="История", callback_data="book_3345")],
    [InlineKeyboardButton(text="Биология", callback_data="book_3367")],
    [InlineKeyboardButton(text="Физика", callback_data="book_3355")],
    [InlineKeyboardButton(text="Обществознание", callback_data="book_3327")],
])
