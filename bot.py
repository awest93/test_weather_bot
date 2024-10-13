
from datetime import datetime, timezone
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from models import log_entry, weather_info
from db import log_event, create_table
from weather_api import get_weather_for_city, WeatherServiceException
import yaml

config = yaml.safe_load(open("config.yml"))
DB_NAME = config["DB_NAME"]
BOT_TOKEN = config["BOT_TOKEN"]
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
MESSAGES = config["bot_messages"]

async def log_handler(message, bot_text):
    current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    await log_event(DB_NAME, log_entry(user_id = message.from_user.id, 
                                       user_text = message.text, 
                                       utc_date = current_date, 
                                       bot_text = bot_text))

@dp.message(Command("start"))
@dp.message(Command("help"))
async def start(message: types.Message):
    await log_handler(message, MESSAGES["help"])
    await message.answer(MESSAGES["help"])

@dp.message(Command("weather"))
async def get_weather_in_city(message: types.Message):
    city = " ".join(message.text.split(" ")[1:])
    response = ""
    try:
        weather: weather_info = await get_weather_for_city(city)
        response = MESSAGES["weather_in_city_message"].format(city,
                                                                 weather.description,
                                                                 weather.temperature,
                                                                 weather.temp_feel,
                                                                 weather.humidity,
                                                                 weather.wind_speed)
    except WeatherServiceException:
        response = MESSAGES["weather_for_location_retrieval_failed"]
    await log_handler(message, response)
    await message.answer(response)

@dp.message()
async def default_response(message: types.Message):
    await log_handler(message, MESSAGES["general_failure"])
    await message.answer(MESSAGES["general_failure"])

async def start_bot():
    await create_table(DB_NAME)
    await dp.start_polling(bot)
