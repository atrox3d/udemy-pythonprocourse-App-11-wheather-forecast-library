import secret


class EndPoint:

    api_key = secret.openweathermap.API_KEY

    def __init__(self, base_url, docs):
        self.base_url = base_url
        self.docs = docs

    def get_url(self, city, country_code=None, units=None, **kwargs):
        params = []
        params += [f'q={city},{country_code}'] if country_code else [f'q={city}']
        params += [f'units={units}'] if units else []

        for k, v in kwargs.items():
            params += [f"{k}={v}"]

        params += [f'appid={self.api_key}']
        queryparams = "&".join(params)

        url = f'{self.base_url}?{queryparams}'
        return url
