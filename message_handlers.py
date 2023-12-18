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
from database import async_session, User
from sqlalchemy.exc import IntegrityError

router = Router()

class States(StatesGroup): # States for FSM
    city = State()

@router.message(CommandStart()) # Handler for /start command
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Hello! I am Weather Bot')
    await message.answer('Please, enter your city name')
    await state.set_state(States.city)
@router.message(States.city) # Handler for city's weather display
async def get_weather(message: Message, state: FSMContext):
    data = get_weather_data(message.text, WEATHER_API_TOKEN)
    if data and data['cod'] == 200:
        async with async_session() as session:
            user = await session.get(User, message.from_user.id) # Get user from database
            if user is None: #
                # If the user does not exist in the database, create a new User object
                user = User(tg_id=message.from_user.id)
                try:
                    session.add(user)
                    await session.commit()
                except IntegrityError: # If the user already exists in the database, rollback the session
                    await session.rollback()
            user.city = message.text  # Update the user's city
            await session.commit()
        await state.update_data(city=message.text) # Update state data
        await message.answer(weather_translate(data)) # Send weather data
        await message.answer('You can look for more info or enter other city', reply_markup=await buttons.more_info_keyboard())
    else:
        await message.answer('Something went wrong, please try again')

@router.callback_query(F.data.startswith('humidity')) # Handler for humidity
async def show_humidity(call: F.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    city = user_data.get('city') # Get city from state data
    if city: # If city exists
        data = get_weather_data(city, WEATHER_API_TOKEN) # Get weather data
        if data:
            await call.message.answer(f"Current humidity: {data['main']['humidity']}%") # Send humidity
        else:
            await call.message.answer('Something went wrong, please try again')
    else:
        await call.message.answer('No city name was found, please enter again')

@router.callback_query(F.data.startswith('pressure')) # Handler for pressure
async def show_pressure(call: F.CallbackQuery, state: FSMContext):
    user_data = await state.get_data() # Get state data
    city = user_data.get('city') # Get city from state data
    if city:
        data = get_weather_data(city, WEATHER_API_TOKEN) # Get weather data
        if data:
            await call.message.answer(f"Current pressure: {data['main']['pressure']} hPa") # Send pressure
        else:
            await call.message.answer('Something went wrong, please try again')
    else:
        await call.message.answer('No city name was found, please enter again')

@router.callback_query(F.data.startswith('wind')) # Handler for wind
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

@router.callback_query(F.data.startswith('sun')) # Handler for sunset and sunrise
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

