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
        """
        update Option with name, value regardless of prefix --

        :param name:
        :param value:
        :return:
        """
        if name.startswith('--'):                                               # save either normal and double dash
            self.name = name[2:]
            self.dashname = self.name
        else:
            self.name = name
            self.dashname = '--' + self.name
        self.value = value

    def dictitem(self, dash=False):                                             # return Option as Dictionary
        return {self.dashname if dash else self.name: self.value}

    def tuple(self, dash=False):                                                # return option as Tuple
        return self.dashname if dash else self.name, self.value

    def longopt(self):                                                          # return Option as long option string
        return f'{self.name}='


class Flag(Option):
    """
    create an Option sublclass object from a tuple option name, option value
    like getopt return value,
    saving name and dash name to be used based on the situation
    value is False by defautl, become true only if present on command line

    :param name:
    :param value:
    """
    def __init__(self, name, default=False):
        super().__init__(name, default)

    def update(self, name, value=False):
        super().update(name, value if value is False else True)                 # if getopt returns name, '' set to True

    def longopt(self):                                                          # return Flag as long option string
        return self.name


class LongOptions:
    """
    collection of Options and Flags based on array of strings in getopt format
    """
    def __init__(self, options):
        self.options = {}
        if isinstance(options, str):                                            # create list if string
            options = options.split()

        for option in options:
            if option.endswith('='):
                name = option[:-1]                                              # remove equal sign
                self.options.update({name: Option(name)})                       # build option
            else:
                self.options.update({option: Flag(option)})                     # build flag

    def longopts(self):
        """
        return list of long options strings
        """
        return [option.longopt() for option in self.options.values()]

    def evaluate(self, opts, filter=None):
        """
        evaluates getopt result and optionally filters a subset
        returns a dict for kwargs

        :param opts:
        :param filter:
        :return:
        """
        for name, val in opts:
            if option := self.options.get(name[2:]):                            # select only getopt results
                option.update(name, val)                                        # update value of Option/Flag
        if filter:
            return self.filter(filter)                                          # filter subset
        else:
            return self.get_dict(True)                                          # return only getopt results

    def get_dict(self, notNone=False):
        """
        return a dict of all options or just the assigned by getopt

        :param notNone:
        :return:
        """
        if notNone:
            return {key: val for option in self.options.values() for key, val in option.dictitem().items() if val}
        else:
            return {key: val for option in self.options.values() for key, val in option.dictitem().items()}

    def filter(self, names, notNone=True):
        """
        filters a subset of options, by default only those assigned by getopt

        :param names:
        :param notNone:
        :return:
        """
        kwargs = {key: val for key, val in self.get_dict(notNone).items() if key + '=' in names or key in names}
        return kwargs


if __name__ == '__main__':
    longopts = 'city= debug'
    options = LongOptions(longopts)
    print(f'options.options   : {options.options}')
    print(f'options.longopts(): {options.longopts()}')

    cmdlineparams = '--city nichelino --debug'.split()
    opts, args = getopt.getopt(cmdlineparams, None, options.longopts())
    print(f'opts: {opts}, args: {args}')                                        # [('--city', 'nichelino'), ('--debug', '')] []

    options.evaluate(opts)
    print(options.get_dict())