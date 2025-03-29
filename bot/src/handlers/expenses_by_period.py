from datetime import datetime
import os

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
import requests

from utils.get_expenses import get_expenses

API_URL = os.getenv("API_URL", "http://backend:8000")

class PeriodExpenseForm(StatesGroup):
    start_date = State()
    end_date = State()
    
router = Router()

@router.message(F.text == 'Витрати за період')
async def start_period_expense(message: types.Message, state: FSMContext):
    await message.answer("Введіть початкову дату у форматі dd.mm.YYYY, наприклад 01.01.2025")
    await state.set_state(PeriodExpenseForm.start_date)
    
@router.message(PeriodExpenseForm.start_date)
async def get_start_date(message: types.Message, state: FSMContext):
    try:
        start_date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer("Невірний формат дати. Спробуйте ще раз.")
        return
    
    await state.update_data(start_date=start_date)
    
    await message.answer("Введіть кінцеву дату у форматі dd.mm.YYYY, наприклад 01.01.2025")
    await state.set_state(PeriodExpenseForm.end_date)
    
@router.message(PeriodExpenseForm.end_date)
async def get_end_date(message: types.Message, state: FSMContext):
    try:
        end_date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer("Невірний формат дати. Спробуйте ще раз.")
        return
    
    user_data = await state.get_data()
    start_date = user_data['start_date']
    
    if end_date < start_date:
        await message.answer("Кінцева дата не може бути раніше початкової. Спробуйте ще раз.")
        return
    
    await state.update_data(end_date=end_date)
    
    response = requests.get(f"{API_URL}/expenses?start_date={start_date.strftime('%d.%m.%Y')}&end_date={end_date.strftime('%d.%m.%Y')}")
    
    if response.status_code != 200:
        await message.answer("Не вдалося отримати витрати за вказаний період. Спробуйте ще раз.")
        return
    expenses = response.json()
    await get_expenses(message, expenses)
    
    await state.clear()
    