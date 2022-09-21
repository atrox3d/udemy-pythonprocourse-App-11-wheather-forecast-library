import json


class CacheException(Exception):
    pass


class CacheDataMissingException(CacheException):
    pass


class Cache:
    def __init__(
            self,
            cachepath='files/cache.json',                                       # default path
    ):
        self.url = None
        self.cachepath = cachepath
        self.data = None

    def get(self):
        return self.data                                                        # get data

    # TODO: cache should load a dict for each url but today's date changes
    def load(self):
        """
        loads json dict
        :return: dict
        """
        print(f"Cache | load | using cache: {self.cachepath} | loading...")
        with open(self.cachepath) as fp:                # load data
            self.data = json.load(fp)
        return self.data                                # return data

    # TODO: cache should save a dict for each url but today's date changes
    def save(self, url, data):
        self.url = url
        self.data = {}                                  # create dict
        self.data.update(data)

        if self.data:
            print(f"Cache | save | using cache: {self.cachepath} | saving...")
            with open(self.cachepath, 'w') as fp:       # save json to file news-cache.json

                # TODO: url should be the key to the item containing the dict but today's date changes
                # https://www.geeksforgeeks.org/python-append-items-at-beginning-of-dictionary/
                url_first = dict(url=self.url)          # try to save url on top of json
                url_first.update(self.data)

                self.data = url_first
                json.dump(
                    self.data,                          # dict
                    fp,                                 # file pointer
                    indent=4                            # pretty print
                )
        else:
            raise CacheDataMissingException             # cannot be empty
