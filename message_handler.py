from aiogram import Router, types
from aiogram.filters import CommandStart
from database import add_user

from keyboards import books_keyboard

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    await add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)

    await message.answer("Привет, я бот для краткого изложения абзацев! Выбери нужную книгу", reply_markup=books_keyboard)