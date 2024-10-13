class log_entry:
    def __init__(self, user_id, user_text, utc_date, bot_text):
        self.user_id = user_id
        self.user_text = user_text
        self.utc_date = utc_date
        self.bot_text = bot_text

class weather_info:
    def __init__(self, temperature, temp_feel, description, humidity, wind_speed, celsius=False):
        self.temperature = temperature if celsius else self.kelvin_to_celsius(temperature)
        self.temp_feel = temp_feel if celsius else self.kelvin_to_celsius(temp_feel)
        self.description = description
        self.humidity = humidity
        self.wind_speed = wind_speed

    def kelvin_to_celsius(self, degrees):
        KELVIN_DIFF = 273
        return degrees - KELVIN_DIFF
