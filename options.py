import getopt
import sys


class Option:

    def __init__(self, name: str, default=None):
        """
        create an Option object from a tuple option name, option value
        like getopt return value,
        saving name and dash name to be used based on the situation

        :param name:
        :param value:
        """
        self.update(name, default)

    def update(self, name, value):
        if name.startswith('--'):                                               # save either normal and double dash
            self.name = name[2:]
            self.dashname = self.name
        else:
            self.name = name
            self.dashname = '--' + self.name
        self.value = value

    def dictitem(self, dash=False):
        return {self.dashname if dash else self.name: self.value}

    def tuple(self, dash=False):
        return self.dashname if dash else self.name, self.value

    def longopt(self):
        return f'{self.name}='


class Flag(Option):

    def __init__(self, name, default=False):
        super().__init__(name, default)

    def update(self, name, value=False):
        super().update(name, value if value is False else True)

    def longopt(self):
        return self.name


class Options:
    def __init__(self, options):
        self.options = {}
        if isinstance(options, str):
            options = options.split()

        for option in options:
            if option.endswith('='):                                            # build option
                name = option[:-1]
                self.options.update({name: Option(name)})
            else:
                self.options.update({option: Flag(option)})                     # build flag

    def longopts(self):
        return [option.longopt() for option in self.options.values()]

    def evaluate(self, opts, filter=None):
        for name, val in opts:
            if option := self.options.get(name[2:]):
                option.update(name, val)
        if filter:
            return self.filter(filter)
        else:
            return self.get_dict(True)

    def get_dict(self, notNone=False):
        if notNone:
            return {key: val for option in self.options.values() for key, val in option.dictitem().items() if val}
        else:
            return {key: val for option in self.options.values() for key, val in option.dictitem().items()}

    def filter(self, names, notNone=True):
        kwargs = {key: val for key, val in self.get_dict(notNone).items() if key + '=' in names or key in names}
        return kwargs


if __name__ == '__main__':
    longopts = 'city= debug'
    options = Options(longopts)
    print(f'options.options   : {options.options}')
    print(f'options.longopts(): {options.longopts()}')

    cmdlineparams = '--city nichelino --debug'.split()
    opts, args = getopt.getopt(cmdlineparams, None, options.longopts())
    print(f'opts: {opts}, args: {args}')                                        # [('--city', 'nichelino'), ('--debug', '')] []

    options.evaluate(opts)
    print(options.get_dict())