class WeatherData:
    def __init__(self, temperature, dt_txt, cloud_percentage):
        self.temperature = temperature
        self.dt_txt = dt_txt
        self.cloud_percentage = cloud_percentage


def create_weatherdata(temperature, dt_txt, cloud_percentage):
    weather_data = WeatherData(temperature, dt_txt, cloud_percentage)
    return weather_data
