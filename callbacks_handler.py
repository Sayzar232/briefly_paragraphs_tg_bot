from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import BufferedInputFile
from parser import get_paragraphs
from config import book_numbers
from keyboards import get_paragraphs_keyboard
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data.startswith("book_"))
async def handle_book_callback(callback: CallbackQuery, state: FSMContext):
    book_number = callback.data.split("_")[1]

    await state.update_data(book_number=book_number)

    url = book_numbers[book_number]

    await callback.message.answer("Теперь выбери нужный параграф", reply_markup=get_paragraphs_keyboard(url))

    await callback.answer()  # Acknowledge the callback to remove the loading state


@router.callback_query(F.data.startswith("paragraph_"))
async def handle_paragraph_callback(callback: CallbackQuery, state: FSMContext):
    paragraph_text = callback.data

    data = await state.get_data()
    book_number = data.get("book_number")

    image_bytes = get_paragraphs(paragraph_text.split("_")[1], book_number)
    
    if image_bytes:
        await callback.message.answer_photo(BufferedInputFile(image_bytes, "paragraph.jpg"), caption=f"Вот краткое содержание параграфа {paragraph_text.split('_')[1]}")
    else:
        await callback.message.answer("Sorry, could not retrieve the content for this paragraph.")
    
    await callback.answer()  # Acknowledge the callback to remove the loading state