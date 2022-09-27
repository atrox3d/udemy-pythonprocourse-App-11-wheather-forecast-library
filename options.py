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
        if name.startswith('--'):                                               # save either normal and double dash
            self.name = name[2:]
            self.dashname = self.name
        else:
            self.name = name
            self.dashname = '--' + self.name
        self.value = default

    def dictitem(self, dash=False):
        return {self.dashname if dash else self.name: self.value}

    def tuple(self, dash=False):
        return self.dashname if dash else self.name, self.value

    def longopt(self):
        return f'{self.name}='


class Flag(Option):

    def __init__(self, name, default=True):
        super().__init__(name, default)

    def longopt(self):
        return self.name


class Options:
    def __init__(self, options):
        self.options = []
        if isinstance(options, str):
            options = options.split()

        for option in options:
            if option.endswith('='):
                self.options.append(Option(option[:-1]))
            else:
                self.options.append(Flag(option))
    #
    # def dictitems(self):
    #     return list(map(lambda x: x.dictitem(), self.options))

    def longopts(self):
        return [option.longopt() for option in self.options]

    def dict(self):
        return dict(self.tuples())

    def tuples(self):
        return list(map(lambda x: x.tuple(), self.options))


def test():
    opt = Option('city', 'turin')
    print(f'option: {opt.dictitem()} | {opt.tuple()}')
    flag = Flag('debug')
    print(f'flag  : {flag.dictitem()} |  {flag.tuple()}')
    opt = Option('--contry', 'it')
    print(f'option: {opt.dictitem()} | {opt.tuple()}')
    flag = Flag('--simple')
    print(f'flag  : {flag.dictitem()} |  {flag.tuple()}')
    opts = Options(('city', 'nichelino'), ('debug', ''), ('--simple', ''))
    print(f'opts  : {opts.tuples()} | {opts.dict()}')


if __name__ == '__main__':
    # test()
    longopts = 'city= debug'
    options = Options(longopts)
    print(options.longopts())

    cmdlineparams = '--city nichelino --debug'.split()
    opts, args = getopt.getopt(cmdlineparams, None, options.longopts())
    print(opts, args)                                       # [('--city', 'nichelino')] []

