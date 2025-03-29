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

class DeleteExpenseForm(StatesGroup):
    delete_expense_id = State()
    delete_expense_confirmation = State()

router = Router()

@router.message(F.text == 'Видалити витрату')
async def delete_expense(message: types.Message, state: FSMContext):
    expenses = fetch_expenses()
    await get_expenses(message, expenses)
    await message.answer("Введіть ID витрати, яку потрібно видалити:")
    await state.set_state(DeleteExpenseForm.delete_expense_id)
    
@router.message(DeleteExpenseForm.delete_expense_id)
async def get_delete_expense_id(message: types.Message, state: FSMContext):
    try:
        expense_id = int(message.text)
    except ValueError:
        await message.answer("Невірний формат ID. Перевірте ID витрати та спробуйте ще раз.")
        return
    
    await state.update_data(delete_expense_id=expense_id)
    
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
    
    await message.answer(f"Ви впевнені, що хочете видалити витрату з ID {expense_id}?", reply_markup=confirm())
    await state.set_state(DeleteExpenseForm.delete_expense_confirmation)
    
@router.callback_query(DeleteExpenseForm.delete_expense_confirmation, F.data == "confirm_yes")
async def confirm_delete_expense(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    expense_id = user_data['delete_expense_id']
    
    response = requests.delete(f"{API_URL}/expenses/{expense_id}")
    
    if response.status_code == 200:
        await callback.message.answer(f"Витрата з ID {expense_id} була успішно видалена.")
    else:
        await callback.message.answer("Не вдалося видалити витрату. Спробуйте ще раз.")
    
    await state.clear()
    
@router.callback_query(DeleteExpenseForm.delete_expense_confirmation, F.data == "confirm_no")
async def cancel_delete_expense(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Видалення витрати скасовано.")
    await state.clear()
    