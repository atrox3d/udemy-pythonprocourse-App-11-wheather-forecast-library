import getopt
import sys


class WeatherOptions:

    NAME = __qualname__
    
    WEATHER_OPTS_NAMES = [
        'city',
        'country_code',
        'lat',
        'lon',
        'lang',
    ]

    NEXT_OPTS_NAMES = [
        'hours',
    ]

    NEXT_OPTS_FLAGS = [
        'simplified',
        'from_cache'
    ]

    def __init__(self, params=sys.argv):
        self.params = params
        self.WEATHER_OPTS = []
        self.NEXT_OPTS = []
        self.opts, self.args = self.getopts(self.params)
        print(self.NAME, ' | ', 'self.params | ', self.params)
        print(self.NAME, ' | ', 'self.opts   | ', self.opts)
        print(self.NAME, ' | ', 'self.args   | ', self.args)

    def build_opts(self):
        self.WEATHER_OPTS = [f'{opt}=' for opt in self.WEATHER_OPTS_NAMES]
        print(self.NAME, ' | ', 'self.WEATHER_OPTS | ', self.WEATHER_OPTS)

        self.NEXT_OPTS = [f'{opt}=' for opt in self.NEXT_OPTS_NAMES]
        self.NEXT_OPTS += self.NEXT_OPTS_FLAGS
        print(self.NAME, ' | ', 'self.NEXT_OPTS | ', self.NEXT_OPTS)

        return self.WEATHER_OPTS + self.NEXT_OPTS

    def getopts(self, params):
        return getopt.getopt(
            params[1:],
            "",
            self.build_opts()
        )

    def parse_weather_opts(self):
        weather_opts = {
            item[0]: item[1] for item in                                        # build dict item
            [(opt[0].replace('--', ''), opt[1]) for opt in self.opts]           # nested list comprehension, remove -- from options in tuples
            if item[0] in self.WEATHER_OPTS_NAMES                               # filter only weather options
        }

        print(self.NAME, ' | ', 'weather_opts | ', weather_opts)
        print(self.NAME, ' | ', 'WEATHER_OPTS | ', self.WEATHER_OPTS)
        exit()
        return weather_opts

    def parse_next_opts(self):
        next_opts = {t[0].replace('--', ''): True if not t[1] else t[1] for t in self.opts if t[0].startswith('--') if
                     t[0] in self.NEXT_OPTS}
        print(self.NAME, ' | ', 'self.NEXT_OPTS | ', self.NEXT_OPTS)
        print(self.NAME, ' | ', 'next_opts | ', next_opts)
        if next_opts.get('hours'):
            next_opts['hours'] = int(next_opts['hours'])
        default_next_ops = {
            'hours': 12,
            'simplified': True,
            'from_cache': False
        }
        default_next_ops.update(next_opts)
        print(self.NAME, ' | ', 'default_next_opts | ', default_next_ops)
        return default_next_ops

    def parse(self):
        weather_opts = self.parse_weather_opts()
        next_opts = self.parse_next_opts()
        return weather_opts, next_opts


if __name__ == '__main__':
    # w = Weather(**weather_opts)
    # print(w.url)
    #
    # print(w.next_n_hours(**default_next_ops))
    wo = WeatherOptions(sys.argv)
    wo.parse()
