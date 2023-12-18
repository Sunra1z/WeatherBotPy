from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def more_info_keyboard():
    more_kb = InlineKeyboardBuilder()
    more_kb.add(InlineKeyboardButton(text='💧 Humidity', callback_data='humidity'))
    more_kb.add(InlineKeyboardButton(text='🌫️ Pressure', callback_data='pressure'))
    more_kb.add(InlineKeyboardButton(text='🌬️ Wind', callback_data='wind'))
    more_kb.add(InlineKeyboardButton(text='☀️ Sunset & Sunrise', callback_data='sun'))
    return more_kb.adjust(2).as_markup()