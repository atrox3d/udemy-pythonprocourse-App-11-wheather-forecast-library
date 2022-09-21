import secret.openweathermap


class EndPoint:

    def __init__(self, base_url, docs):
        self.base_url = base_url
        self.docs = docs
        self.params = {}

    def get_url(self, **kwargs):
        self.params = kwargs                                                    # save params
        params = []
        for k, v in kwargs.items():
            params += [f"{k}={v}"]                                              # build list of params
        queryparams = "&".join(params)                                          # build query string

        url = f'{self.base_url}?{queryparams}'                                  # build url
        return url


class OpenWeatherMapEndPoint(EndPoint):

    api_key = secret.openweathermap.API_KEY

    def get_url(self, city, country_code=None, units=None, lang=None, **kwargs):
        params = {}

        params['q'] = f'{city},{country_code}' if country_code else f'{city}'   # add city and country code, if present
        if units:
            params['units'] = units                                             # add units, if present
        if lang:
            params['lang'] = lang                                               # add lang, if present
        params.update(kwargs)                                                   # add other params
        params['appid'] = self.api_key                                          # add api_key

        url = super().get_url(**params)                                         # build url
        return url


if __name__ == '__main__':
    owmep = OpenWeatherMapEndPoint('https://base.url', 'https://docs.url')
    print(owmep.base_url)
    print(owmep.get_url(city='turin', country_code='it', lang='it', test='CIAO'))
    print(owmep.params)
