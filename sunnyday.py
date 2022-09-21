import requests as requests

from endpoint import OpenWeatherMapEndPoint


class Weather:

    def __init__(self, city, country_code=None, lat=None, lon=None):
        self.city = city
        self.country_code = country_code
        self.lat = lat
        self.lon = lon
        self.data = {}
        self.endpoint = OpenWeatherMapEndPoint(
            base_url='https://api.openweathermap.org/data/2.5/forecast',
            docs='https://openweathermap.org/forecast5',
        )
        self.url = self.endpoint.get_url(self.city, country_code=self.country_code, lat=self.lat, lon=self.lon)

    def _update(self):
        self.url = self.endpoint.get_url(self.city, country_code=self.country_code, lat=self.lat, lon=self.lon)
        response = requests.get(self.url)
        response.raise_for_status()
        self.data = response.json()

    def next12h(self):
        self._update()
        return self.data


w = Weather('Turin')
print(w.url)
print(w.next12h())
