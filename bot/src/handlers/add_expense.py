from datetime import datetime
import os

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
import requests

API_URL = os.getenv("API_URL", "http://backend:8000")

class AddExpenseForm(StatesGroup):
    expense_name = State()
    expense_date = State()
    expense_amount = State()

router = Router()

@router.message(F.text == 'Додати витрату')
async def start(message: types.Message, state: FSMContext):
    await message.answer("Введіть назву витрати.")
    await state.set_state(AddExpenseForm.expense_name)

@router.message(AddExpenseForm.expense_name)
async def get_expense_name(message: types.Message, state: FSMContext):
    expense_name = message.text
    await state.update_data(expense_name=expense_name)
    await message.answer("Тепер введи дату витрати у форматі dd.mm.YYYY (наприклад, 19.03.2025).")
    await state.set_state(AddExpenseForm.expense_date)

@router.message(AddExpenseForm.expense_date)
async def get_expense_date(message: types.Message, state: FSMContext):
    try:
        expense_date = datetime.strptime(message.text, '%d.%m.%Y')
    except ValueError:
        await message.answer("Невірний формат дати. Спробуй ще раз (dd.mm.YYYY).")
        return
    
    await state.update_data(expense_date=expense_date)
    await message.answer("Тепер введідть суму витрати в UAH у вигляді числа (наприклад, 150.75 або 100).")
    await state.set_state(AddExpenseForm.expense_amount)

@router.message(AddExpenseForm.expense_amount)
async def get_expense_amount(message: types.Message, state: FSMContext):
    try:
        expense_amount = float(message.text)
    except ValueError:
        await message.answer("Невірна сума витрати. Введіть число.")
        return
    
    await state.update_data(expense_amount=expense_amount)

    user_data = await state.get_data()
    expense_name = user_data['expense_name']
    expense_date = user_data['expense_date']
    expense_amount = user_data['expense_amount']

    await message.answer(f"Ось ваші дані:\n\n"
                         f"Назва витрати: {expense_name}\n"
                         f"Дата витрати: {expense_date.strftime('%d.%m.%Y')}\n"
                         f"Сума витрати: {expense_amount} UAH")
    
    await message.answer("Витрату буде додано. Зачекайте...")

    response = requests.post(f"{API_URL}/expenses/", json={
        "user_id": message.from_user.id,
        "name": expense_name,
        "date": expense_date.strftime('%d.%m.%Y'),
        "amount_uah": expense_amount
    })

    if response.status_code == 201:
        await message.answer("✅ Витрату успішно додано!")
    else:
        await message.answer("❌ Помилка при додаванні витрати. Спробуйте ще раз.")
    
    await state.clear()