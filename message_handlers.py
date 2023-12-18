import asyncio
import json
import requests
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from config import WEATHER_API_TOKEN

router = Router()

class States(StatesGroup):
    city = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Hello! I am Weather Bot')
    await message.answer('Please, enter your city name')
    await state.set_state(States.city)

@router.message(States.city)
async def get_weather(message: Message):
    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_API_TOKEN}&units=metric'
        )
        data = response.json()
        if data['cod'] == 200:
            city = data['name']
            temp = data['main']['temp']
            weather_description = data['weather'][0]['description']
            await message.reply(f"Weather in {city}: {weather_description}, temperature: {temp:.2f}°C")
        else:
            await message.reply("Sorry, I couldn't find the weather for that city.")
    except Exception as e:
        await message.reply("Sorry, an error occurred while fetching the weather data.")


