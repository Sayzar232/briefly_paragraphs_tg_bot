from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils import get_subjects_keyboard, get_books_keyboard
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data.startswith("grade_"))
async def handle_book_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    grade = int(callback.data.split("_")[1])

    await state.update_data(grade=grade)

    await callback.message.edit_text(
        "Теперь выбери предмет",
        reply_markup=get_subjects_keyboard(grade)
    )


@router.callback_query(F.data.startswith("subject_"))
async def handle_book_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    state_data = state.get_data()

    subject = callback.data.split("_")[1]
    grade = state["grade"]

    await state.update_data(subject=subject)

    await callback.message.edit_text(
        "Выбери Авторов",
        reply_markup=get_books_keyboard(grade)
    )