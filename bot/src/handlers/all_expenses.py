import os

from aiogram import Router, types, F

from utils.get_expenses import get_expenses
from utils.api import fetch_expenses

API_URL = os.getenv("API_URL", "http://backend:8000")

router = Router()

@router.message(F.text == 'Усі витрати')
async def all_expenses(message: types.Message):
    expenses = fetch_expenses()
    await get_expenses(message, expenses)
