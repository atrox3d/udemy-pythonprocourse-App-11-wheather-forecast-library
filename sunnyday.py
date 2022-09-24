import getopt
import sys

import requests as requests

from endpoint import OpenWeatherMapEndPoint
from cache import Cache


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

        data = self.data['list'][:round(hours/3)]

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
    # w = Weather(city='Nichelino', country_code='it', lang='it')
    # print(w.url)
    # print(json.dumps(w.next12h(from_cache=True), indent=4))
    # print(w.next12hsimplified(from_cache=False))
    print(sys.argv[1:])
    opts, args = getopt.getopt(
        sys.argv[1:],
        "c:C:l:h:",
        [
            'city=',
            'country_code=',
            'lat=',
            'lon=',
            'lang=',
            'hours=',
            'simplified',
            'from_cache'
        ]
    )
    print('opts | ', opts)
    print('args | ', args)

    WEATHER_OPTS = [
            '--city',
            '--country_code',
            '--lat=',
            '--lon=',
            '--lang=',
    ]

    NEXT_OPTS = [
        '--hours',
        '--simplified',
        '--from_cache'
    ]

    weather_opts = {t[0].replace('--', ''): t[1] for t in opts if t[0].startswith('--') if t[0] in WEATHER_OPTS}
    print('weather_opts | ', weather_opts)
    print('WEATHER_OPTS | ', WEATHER_OPTS)
    w = Weather(**weather_opts)
    print(w.url)

    next_opts = {t[0].replace('--', ''): True if not t[1] else t[1] for t in opts if t[0].startswith('--') if t[0] in NEXT_OPTS}
    print('NEXT_OPTS | ', NEXT_OPTS)
    print('next_opts | ', next_opts)
    if next_opts.get('hours'):
        next_opts['hours'] = int(next_opts['hours'])
    default_next_ops = {
        'hours': 12,
        'simplified': True,
        'from_cache': False
    }
    default_next_ops.update(next_opts)
    print('default_next_opts | ', default_next_ops)
    print(w.next_n_hours(**default_next_ops))

