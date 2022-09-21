import requests as requests
import json

from endpoint import OpenWeatherMapEndPoint
from cache import Cache


class Weather:

    def __init__(self, city=None, country_code=None, lat=None, lon=None, units='metric', **kwargs):
        self.city = city
        self.country_code = country_code
        self.lat = lat
        self.lon = lon
        self.units = units
        self.kwargs = kwargs
        self.data = {}
        self.cache = Cache()
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
            units=self.units,
            **self.kwargs
        )

    def _update(self):
        self._buildurl()
        response = requests.get(self.url)
        response.raise_for_status()
        self.data = response.json()
        self.cache.save(self.url, self.data)

    def _load(self):
        self.data = self.cache.load()

    def next24h(self, from_cache=False):
        if from_cache:
            self._load()
        else:
            self._update()
        return self.data['list'][:8]

    def next24hsimplified(self, from_cache=False):
        if from_cache:
            self._load()
        else:
            self._update()
        lines = []
        for item in self.data['list'][:8]:
            # line = ''
            elements = []
            elements.append(item['dt_txt'])
            elements.append(item['main']['temp'])
            elements.append(item['weather'][0]['description'])
            elements = map(str, elements)
            line = ' | '.join(elements)
            lines += [line]

        return '\n'.join(lines)


w = Weather(city='Nichelino', country_code='it', lang='it')
print(w.url)
# print(json.dumps(w.next12h(from_cache=True), indent=4))
print(w.next24hsimplified(from_cache=True))