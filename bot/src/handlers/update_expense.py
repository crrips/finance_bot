from datetime import datetime
import os


from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
import requests

from utils.get_expenses import get_expenses
from utils.api import fetch_expenses
from keyboards import confirm

API_URL = os.getenv("API_URL", "http://backend:8000")

class UpdateExpenseForm(StatesGroup):
    expense_id = State()
    expense_name = State()
    expense_amount = State()
    expense_confirmation = State()

router = Router()

@router.message(F.text == 'Редагувати витрату')
async def start(message: types.Message, state: FSMContext):
    expenses = fetch_expenses()
    await get_expenses(message, expenses)
    await message.answer("Введіть ID витрати, яку потрібно редагувати.")
    await state.set_state(UpdateExpenseForm.expense_id)
    
@router.message(UpdateExpenseForm.expense_id)
async def get_expense_id(message: types.Message, state: FSMContext):
    try:
        expense_id = int(message.text)
    except ValueError:
        await message.answer("Невірний формат ID. Перевірте ID витрати та спробуйте ще раз.")
        return
    
    await state.update_data(expense_id=expense_id)
    
    response = requests.get(f"{API_URL}/expenses/{expense_id}")
    
    if response.status_code != 200:
        await message.answer("Витрата з таким ID не знайдена. Спробуйте ще раз.")
        return
    
    expense = response.json()
    
    date = expense['date']
    date_obj = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
    formatted_date = date_obj.strftime("%d.%m.%Y")
    
    await message.answer(f"Витрата з ID {expense_id}:\n\n"
                         f"Назва витрати: {expense['name']}\n"
                         f"Сума витрати: {expense['amount_uah']} UAH\n"
                         f"Сума витрати в USD: {expense['amount_usd']} USD\n"
                         f"Дата витрати: {formatted_date}\n"
    )
    await message.answer("Введіть нову назву витрати.")
    await state.set_state(UpdateExpenseForm.expense_name)

@router.message(UpdateExpenseForm.expense_name)
async def get_expense_name(message: types.Message, state: FSMContext):
    expense_name = message.text
    await state.update_data(expense_name=expense_name)
    
    await message.answer("Тепер введи нову суму витрат у вигляді числа (наприклад, 150.75 або 100).")
    await state.set_state(UpdateExpenseForm.expense_amount)

@router.message(UpdateExpenseForm.expense_amount)
async def get_expense_amount(message: types.Message, state: FSMContext):
    try:
        expense_amount = float(message.text)
    except ValueError:
        await message.answer("Невірна сума витрат. Введіть число.")
        return
    
    await state.update_data(expense_amount=expense_amount)

    user_data = await state.get_data()
    expense_name = user_data['expense_name']
    expense_amount = user_data['expense_amount']

    await message.answer(f"Ось ваші дані:\n\n"
                         f"Назва витрати: {expense_name}\n"
                         f"Сума витрати: {expense_amount} UAH")
    
    await message.answer("Ви впевнені, що хочете редагувати витрату?", reply_markup=confirm())
    await state.set_state(UpdateExpenseForm.expense_confirmation)
    
@router.callback_query(UpdateExpenseForm.expense_confirmation, F.data == "confirm_yes")
async def confirm_update_expense(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    expense_id = user_data['expense_id']
    expense_name = user_data['expense_name']
    expense_amount = user_data['expense_amount']

    response = requests.put(f"{API_URL}/expenses/{expense_id}", json={
        "name": expense_name,
        "amount_uah": expense_amount
    })

    if response.status_code == 200:
        await callback.message.answer("✅ Витрату успішно відредаговано!")
    else:
        await callback.message.answer("❌ Помилка при редагуванні витрати. Спробуйте ще раз.")

    await state.clear()
    
@router.callback_query(UpdateExpenseForm.expense_confirmation, F.data == "confirm_no")
async def cancel_update_expense(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Редагування витрати скасовано.")
    await state.clear()
    