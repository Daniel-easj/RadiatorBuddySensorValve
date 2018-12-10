class WeatherData:
    def __init__(self, temperature, dt_txt, cloud_percentage):
        self.temperature = temperature
        self.dt_txt = dt_txt
        self.cloud_percentage = cloud_percentage

# Function to initialize WeatherData objects


def create_weatherdata(temperature, dt_txt, cloud_percentage):
    weather_data = WeatherData(temperature, dt_txt, cloud_percentage)
    return weather_data

# Function to display data from WeatherData object in string format


def __str__(self):
    return (f"Temperature : {self.temperature}, time : {self.dt_txt}, cloud coverage : {self.cloud_percentage}%")
