from aiogram import Router, types
from aiogram.filters import CommandStart
from database import db

from utils import get_grades_keyboard

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    await db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)

    await message.answer("Привет, я бот для краткого изложения абзацев! Выбери свой класс", reply_markup=get_grades_keyboard())