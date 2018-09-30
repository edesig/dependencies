class dynamicdict(dict):
    """
        dynamicdict(factory[, ...]) --> dict with factory

        The factory is called with one argument to produce
        a new value when a key is not present, in __getitem__ only.
        A defaultdict compares equal to a dict with the same items.
        All remaining arguments are treated the same as if they were
        passed to the dict constructor, including keyword arguments.
        """

    def __init__(self, factory=None, seq=None, **kwargs):
        if seq:
            super(dynamicdict, self).__init__(seq, **kwargs)
        else:
            super(dynamicdict, self).__init__(**kwargs)
        self.factory = factory

    def __missing__(self, key):
        self.__setitem__(key, self.factory(key))
        return self[key]


class idset(set):
    """
        idset([iterable]) --> set with id

        The id represents the order of getting into set,
        therefore this class should not support the operators
        union, intersection and difference, but appending a set to an
        idset makes sense.
    """

    def __init__(self, seq=()):
        super(idset, self).__init__()  # INEFFICIENT WORKAROUND
        self._d = dict()
        self.id = self.__getitem__
        self._lastid = -1
        for item in seq:
            self.add(item)

    def __contains__(self, item):
        return item in self._d

    def __getitem__(self, element):
        return self._d[element]

    def add(self, element):
        super(idset, self).add(element)  # INEFFICIENT WORKAROUND
        if not element in self._d:
            self._lastid += 1
            self._d[element] = self._lastid

    def append(self, iterable):
        for item in iterable:
            self.add(item)
