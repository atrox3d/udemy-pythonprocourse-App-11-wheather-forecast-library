import requests as requests
import json

from endpoint import OpenWeatherMapEndPoint


class Weather:

    def __init__(self, city=None, country_code=None, lat=None, lon=None, units='metric'):
        self.city = city
        self.country_code = country_code
        self.lat = lat
        self.lon = lon
        self.units = units
        self.data = {}
        self.endpoint = OpenWeatherMapEndPoint(
            base_url='https://api.openweathermap.org/data/2.5/forecast',
            docs='https://openweathermap.org/forecast5',
        )
        self._buildurl()

    def _buildurl(self):
        self.url = self.endpoint.get_url(
            city=self.city,
            country_code=self.country_code,
            lat=self.lat,
            lon=self.lon,
            units=self.units
        )

    def _update(self):
        self._buildurl()
        response = requests.get(self.url)
        response.raise_for_status()
        self.data = response.json()

    def next12h(self):
        self._update()
        return self.data['list'][:4]


w = Weather(city='Nichelino', country_code='it')
print(w.url)
print(
    json.dumps(
        w.next12h(), indent=4
    )
)
