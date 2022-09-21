import secret.openweathermap


class EndPoint:

    def __init__(self, base_url, docs):
        self.base_url = base_url
        self.docs = docs

    def get_url(self, **kwargs):
        params = []
        for k, v in kwargs.items():
            params += [f"{k}={v}"]
        queryparams = "&".join(params)

        url = f'{self.base_url}?{queryparams}'
        return url


class OpenWeatherMapEndPoint(EndPoint):

    api_key = secret.openweathermap.API_KEY

    def get_url(self, city, country_code=None, units=None, lang=None, **kwargs):
        params = {}

        params['q'] = f'{city},{country_code}' if country_code else f'{city}'
        if units:
            params['units'] = units
        if lang:
            params['lang'] = lang
        params.update(kwargs)

        url = f'{super().get_url(**params)}&appid={self.api_key}'
        return url


if __name__ == '__main__':
    owmep = OpenWeatherMapEndPoint('https://base.url', 'https://docs.url')
    print(owmep.base_url)
    print(owmep.get_url(city='turin', country_code='it', lang='it', test='CIAO'))