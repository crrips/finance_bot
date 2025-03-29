from aiogram.filters import Command
from aiogram import Router, types

from keyboards import main_menu
from database import conn_db

WELCOME_TEXT = """
📊 Привіт! Я бот для управління витратами. Використовуй меню, щоб додати, видалити, редагувати або переглянути витрати.
""" 

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    user_name = message.from_user.full_name
    
    conn = await conn_db()
    query = '''
        INSERT INTO users (telegram_id, username, name, created_at)
            VALUES ($1, $2, $3, NOW())
            ON CONFLICT (telegram_id) DO NOTHING
    '''
    await conn.execute(query, user_id, user_username, user_name)
    await conn.close()
    
    await message.answer(WELCOME_TEXT, reply_markup=main_menu())
