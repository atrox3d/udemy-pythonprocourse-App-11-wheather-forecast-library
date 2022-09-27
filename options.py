import getopt
import sys


class Option:

    def __init__(self, name: str, value=None):
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
        self.value = value

    def dictitem(self, dash=False):
        return {self.dashname if dash else self.name: self.value}

    def tuple(self, dash=False):
        return self.dashname if dash else self.name, self.value


class Flag(Option):

    def __init__(self, name, value=True):
        super().__init__(name, value)


class Options:
    def __init__(self, options):
        self.options = []
        for option in options:
            if not isinstance(option, tuple):
                raise TypeError
            if len(option) != 2:
                raise ValueError
            if option[1]:
                self.options.append(Option(*option))
            else:
                self.options.append(Flag(option[0]))
    #
    # def dictitems(self):
    #     return list(map(lambda x: x.dictitem(), self.options))

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
    params = ['--city', 'nichelino']
    opts, args = getopt.getopt(params, '', 'city=')
    print(opts, args)                                       # [('--city', 'nichelino')] []

    options = Options(opts)
    print(f'options  : {options.tuples()} | {options.dict()}')
    print(f'options  : {options.tuples()} | {options.dict()}')
