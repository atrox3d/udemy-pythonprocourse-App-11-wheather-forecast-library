from endpoint import OpenWeatherMapEndPoint

current_weather = OpenWeatherMapEndPoint(
    base_url='https://api.openweathermap.org/data/2.5/weather',
    docs='https://openweathermap.org/current',
)

forecast = OpenWeatherMapEndPoint(
    base_url='https://api.openweathermap.org/data/2.5/forecast',
    docs='https://openweathermap.org/forecast5',
)


print(current_weather.get_url('turin', country_code='it', units='metric'))
print(forecast.get_url('turin', country_code='it', units='metric'))
