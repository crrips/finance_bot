import os

from aiogram import Bot, Dispatcher
import asyncio

TOKEN = os.getenv("TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    from handlers import start, all_expenses, expenses_by_period, add_expense, delete_expense, update_expense
    dp.include_router(start.router)
    dp.include_router(all_expenses.router)
    dp.include_router(expenses_by_period.router)
    dp.include_router(add_expense.router)
    dp.include_router(delete_expense.router)
    dp.include_router(update_expense.router)
    
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())