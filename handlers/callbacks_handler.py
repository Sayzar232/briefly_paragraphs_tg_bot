import html

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from utils import get_subjects_keyboard, get_books_keyboard, get_paragraphs_keyboard
from database import db

router = Router()

# Лимит сообщения в Telegram — 4096 символов, оставляем запас
MESSAGE_CHUNK_LIMIT = 4000


async def _safe_edit(callback: CallbackQuery, text: str, reply_markup=None):
    """Редактирует сообщение, игнорируя 'message is not modified'."""
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest:
        pass


def _split_text(text: str, limit: int = MESSAGE_CHUNK_LIMIT) -> list[str]:
    """Разбивает длинный текст на части не длиннее limit по границам строк."""
    chunks: list[str] = []

    while len(text) > limit:
        cut = text.rfind("\n", 0, limit)
        if cut <= 0:
            cut = limit

        chunks.append(text[:cut])
        text = text[cut:].lstrip("\n")

    if text:
        chunks.append(text)

    return chunks


@router.callback_query(F.data.startswith("grade_"))
async def handle_grade_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    grade = int(callback.data.split("_", 1)[1])

    await state.update_data(grade=grade)

    await _safe_edit(
        callback,
        "Теперь выбери предмет",
        reply_markup=await get_subjects_keyboard(grade),
    )


@router.callback_query(F.data.startswith("subject_"))
async def handle_subject_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    state_data = await state.get_data()

    subject = callback.data.split("_", 1)[1]
    grade = state_data["grade"]

    await state.update_data(subject=subject)

    await _safe_edit(
        callback,
        "Выбери Авторов",
        reply_markup=await get_books_keyboard(grade, subject),
    )


@router.callback_query(F.data.startswith("book_"))
async def handle_book_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    book_id = int(callback.data.split("_", 1)[1])

    await state.update_data(book_id=book_id)

    await _safe_edit(
        callback,
        "Теперь выбери параграф",
        reply_markup=await get_paragraphs_keyboard(book_id),
    )


@router.callback_query(F.data.startswith("paragraph_"))
async def handle_paragraph_callback(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    book_id = state_data.get("book_id")

    if book_id is None:
        await callback.answer("Сначала выбери книгу", show_alert=True)
        return

    paragraph_number = int(callback.data.split("_", 1)[1])

    paragraph = await db.get_paragraph(book_id, paragraph_number)

    if paragraph is None:
        await callback.answer("Параграф не найден", show_alert=True)
        return

    await callback.answer()

    header_parts = [f"Параграф {paragraph['paragraph_number']}"]

    if paragraph.get("title"):
        header_parts.append(paragraph["title"])

    header = html.escape(". ".join(header_parts))

    pages = paragraph.get("pages")
    if pages:
        header += f"\n<i>Страницы: {html.escape(str(pages))}</i>"

    # Эскейпим после разбиения, чтобы не разорвать HTML-сущности
    chunks = _split_text(paragraph["text"])

    await callback.message.answer(f"<b>{header}</b>")

    for chunk in chunks:
        await callback.message.answer(html.escape(chunk))


@router.callback_query(F.data == "back_books")
async def handle_back_to_books_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    state_data = await state.get_data()

    grade = state_data.get("grade")
    subject = state_data.get("subject")

    if grade is None or subject is None:
        await _safe_edit(
            callback,
            "Привет, я бот для краткого изложения абзацев! Выбери свой класс",
        )
        return

    await _safe_edit(
        callback,
        "Выбери Авторов",
        reply_markup=await get_books_keyboard(grade, subject),
    )

    await state.clear()