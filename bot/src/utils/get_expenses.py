import os

from aiogram.types.input_file import FSInputFile
from aiogram import types

from utils.xlsx import create_xlsx

API_URL = os.getenv("API_URL", "http://backend:8000")

async def get_expenses(message: types.Message, expenses):
    if not expenses:
        await message.answer("❌ Витрат не знайдено.")
        return
    
    file = create_xlsx(expenses)
    
    document = FSInputFile(file)
    await message.answer_document(document)
    
    os.remove(file)