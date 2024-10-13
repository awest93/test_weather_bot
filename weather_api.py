
import aiohttp.client
import urllib
from models import weather_info
import yaml

config = yaml.safe_load(open("config.yml"))
WEATHER_SERVICE_API_KEY = config["WEATHER_SERVICE_API_KEY"]

class WeatherServiceException(BaseException):
    pass

async def get_weather_for_city(city_name: str) -> weather_info:
    return await make_weather_service_query(get_city_query_url(city_name))

def get_city_query_url(city_name: str):
    return f'http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city_name)}&appid={WEATHER_SERVICE_API_KEY}&lang=ru'

async def make_weather_service_query(url: str) -> weather_info:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return get_weather_from_response(await resp.json())
    raise WeatherServiceException()

def get_weather_from_response(json):
    return weather_info(json['main']['temp'], json['main']['feels_like'], json['weather'][0]['description'], json['main']['humidity'], json['wind']['speed'])
