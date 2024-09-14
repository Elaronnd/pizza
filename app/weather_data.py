from aiocache import cached
from aiohttp.client import ClientSession
from app.debugs.change_logger import logger
from app.get_config.keys import time_live
from app.get_config.keys import weather_token as api_key


class Weather:
    # Повертає json з api погоди вказаного
    @cached(ttl=time_live)
    async def get_data_city(self, url: str = "https://api.openweathermap.org/data/2.5/weather", city: str = "Kyiv"):
        params = {
            "q": city,
            "lang": "ua",
            "units": "metric",
            "appid": api_key
        }
        async with ClientSession() as session:
            async with session.get(url, params=params) as response:
                status = response.status
                if status == 200:
                    data = await response.json()
                    return [status, data]
                else:
                    logger.error(f"Weather | An error occurred(from \"get_data_city\"): {status}")
                    return [status, None]

    async def get_weather(self, param: str, city: str = "Kyiv"):
        """
        :param param: can be: "coord", "weather", "base", "main", "visibility", "wind", "clouds", "dt", "sys", "timezone", "id", "name" and "cod"
        :param city:
        :return: [{status api}, {result}]
        """
        data = await self.get_data_city(city=city)
        if data[0] == 200:
            weather = data[1][param]
            return [data[0], weather]
        return data

    async def get_something_weather(self, param: str, city: str = "Kyiv"):
        """
        :param param: can be: "id" , "main", "description" and "icon"
        :param city:
        :return:
        """
        data = await self.get_weather(city=city, param="weather")
        if data[0] == 200:
            something_weather = dict(data[1][0]).get(param)
            return [data[0], something_weather]
        return data

    async def get_something_main(self, param: str, city: str = "Kyiv"):
        """
        :param param: can be: "temp", "feels_like", "temp_min", "temp_max", "pressure", "humidity", "sea_level" and "grnd_level"
        :param city:
        :return:
        """
        data = await self.get_weather(city=city, param="main")
        if data[0] == 200:
            something_main = dict(data[1]).get(param)
            return [data[0], round(something_main)]
        return data
