from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Усі витрати")
            ],
            [
                KeyboardButton(text="Витрати за період")
            ],
            [
                KeyboardButton(text="Додати витрату"),
                KeyboardButton(text="Редагувати витрату"),
                KeyboardButton(text="Видалити витрату")
            ]
        ],
        resize_keyboard=True
    )

def confirm():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Так", callback_data="confirm_yes")
            ],
            [
                InlineKeyboardButton(text="Ні", callback_data="confirm_no")
            ]
        ]
    )
