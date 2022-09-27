import secret.openweathermap


class EndPoint:
    """
    represents a generic API endpoint with query parameters
    """
    def __init__(self, base_url, docs):
        self.base_url = base_url
        self.docs = docs
        self.params = {}

    def get_url(self, **kwargs):
        self.params = kwargs                                                    # save params
        params = []
        for k, v in kwargs.items():
            if v is not None:
                params += [f"{k}={v}"]                                          # build list of params
        queryparams = "&".join(params)                                          # build query string

        url = f'{self.base_url}?{queryparams}'                                  # build url
        return url


class OpenWeatherMapEndPoint(EndPoint):
    """
    represents an OpenWeatherMap endpoint
    subclass of EndPoint

    API KEY is in secret.openweathermap module, not tracked in git
    """
    api_key = secret.openweathermap.API_KEY

    def get_url(self, city=None, country_code=None, lat=None, lon=None, units=None, lang=None, **kwargs):
        params = {}

        if city:
            if country_code:
                params['q'] = f'{city},{country_code}'                          # add city and country code, if present
            else:
                params['q'] = f'{city}'                                         # or just the city
        elif lat and lon:
            params['lat'] = lat                                                 # alternatively add lat and lon
            params['lon'] = lon
        else:
            raise TypeError('Provide either a city or lat and lon argument')
        if units:
            params['units'] = units                                             # add units, if present
        if lang:
            params['lang'] = lang                                               # add lang, if present
        params.update(kwargs)                                                   # add other params
        params['appid'] = self.api_key                                          # add api_key

        url = super().get_url(**params)                                         # build url
        return url


if __name__ == '__main__':
    current_weather = OpenWeatherMapEndPoint(
        base_url='https://api.openweathermap.org/data/2.5/weather',
        docs='https://openweathermap.org/current',
    )

    forecast = OpenWeatherMapEndPoint(
        base_url='https://api.openweathermap.org/data/2.5/forecast',
        docs='https://openweathermap.org/forecast5',
    )

    print(current_weather.get_url('turin', country_code='it', units='metric'))
    print(current_weather.params)
    print(forecast.get_url('turin', country_code='it', units='metric'))
    print(forecast.params)