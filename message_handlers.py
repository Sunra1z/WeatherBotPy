# Description: This file contains all message handlers for bot
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import buttons
from config import WEATHER_API_TOKEN
from Weather_parser import get_weather_data, weather_translate, weather_emojis
from datetime import datetime

router = Router()

class States(StatesGroup):
    city = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Hello! I am Weather Bot')
    await message.answer('Please, enter your city name')
    await state.set_state(States.city)
@router.message(States.city)
async def get_weather(message: Message, state: FSMContext):
    data = get_weather_data(message.text, WEATHER_API_TOKEN)
    if data and data['cod'] == 200:
        await state.update_data(city=message.text)
        await message.answer(weather_translate(data))
        await message.answer('You can look for more info or enter other city', reply_markup=await buttons.more_info_keyboard())
    else:
        await message.answer('Something went wrong, please try again')

@router.callback_query(F.data.startswith('humidity'))
async def show_humidity(call: F.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    city = user_data.get('city')
    if city:
        data = get_weather_data(city, WEATHER_API_TOKEN)
        if data:
            await call.message.answer(f"Current humidity: {data['main']['humidity']}%")
        else:
            await call.message.answer('Something went wrong, please try again')
    else:
        await call.message.answer('No city name was found, please enter again')

@router.callback_query(F.data.startswith('pressure'))
async def show_pressure(call: F.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    city = user_data.get('city')
    if city:
        data = get_weather_data(city, WEATHER_API_TOKEN)
        if data:
            await call.message.answer(f"Current pressure: {data['main']['pressure']} hPa")
        else:
            await call.message.answer('Something went wrong, please try again')
    else:
        await call.message.answer('No city name was found, please enter again')

@router.callback_query(F.data.startswith('wind'))
async def show_wind(call: F.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    city = user_data.get('city')
    if city:
        data = get_weather_data(city, WEATHER_API_TOKEN)
        if data:
            await call.message.answer(f"Current wind speed: {data['wind']['speed']} m/s")
        else:
            await call.message.answer('Something went wrong, please try again')
    else:
        await call.message.answer('No city name was found, please enter again')

@router.callback_query(F.data.startswith('sun'))
async def show_sun(call: F.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    city = user_data.get('city')
    if city:
        data = get_weather_data(city, WEATHER_API_TOKEN)
        if data:
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
            await call.message.answer(f"Sunrise: {sunrise} Sunset: {sunset}")
        else:
            await call.message.answer('Something went wrong, please try again')
    else:
        await call.message.answer('No city name was found, please enter again')

