import sys
import getopt

import requests as requests

from endpoint import OpenWeatherMapEndPoint
from cache import Cache
from longoptions import LongOptions

class Weather:
    """
    Creates a Weather object using as input either a city name (and optional contry code) or latitude and
    longitude coordinates
    """
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
        # response.raise_for_status()
        self.data = response.json()
        if self.data['cod'] == '200':
            self.cache.save(self.url, self.data)

    def _load(self):
        self.data = self.cache.load()

    def next_n_hours(self, hours=12, simplified=False, from_cache=False):
        if from_cache:
            self._load()
        else:
            self._update()

        if self.data['cod'] != '200':
            raise ValueError(self.data['message'])

        data = self.data['list'][:round(int(hours)/3)]

        if simplified:
            lines = []
            for item in data:
                elements = []
                elements.append(item['dt_txt'])
                elements.append(item['main']['temp'])
                elements.append(item['weather'][0]['description'])
                elements = map(str, elements)
                line = ' | '.join(elements)
                lines += [line]

            return '\n'.join(lines)
        else:
            return data

    def next12h(self, from_cache=False):
        return self.next_n_hours(12, simplified=False, from_cache=from_cache)

    def next12hsimplified(self, from_cache=False):
        return self.next_n_hours(12, simplified=True, from_cache=from_cache)


if __name__ == '__main__':
    weather_options = [                                                         # options for weather class
        'city=',
        'country_code=',
        'lat=',
        'lon=',
        'lang=',
    ]
    next_options = [                                                            # options for next_n_hours()
        'hours=',
        'simplified',
        'from_cache'
    ]
    long_options = weather_options + next_options                               # all options

    options = LongOptions(long_options)                                         # create Options object
    opts, args = getopt.getopt(sys.argv[1:], None, options.longopts())          # use object with getopt

    weather_kwargs = options.evaluate(opts, filter=weather_options)             # get kwargs for weather class
    next_kwargs = options.evaluate(opts, filter=next_options)                   # get kwargs for next_n_hours()

    w = Weather(**weather_kwargs)
    print(w.next_n_hours(**next_kwargs))
