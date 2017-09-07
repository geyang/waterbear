import logging


class Bear():
    def __init__(self, **d):
        """Features:
        0. Take in a list of keyword arguments in constructor, and assign them as attributes
        1. Correctly handles `dir` command, so shows correct auto-completion in editors.
        2. Correctly handles `vars` command, and returns a dictionary version of self.

        When recursive is set to False,
        """
        # double underscore variables are mangled by python, so we use keyword argument dictionary instead.
        # Otherwise you will have to use __Bear_recursive = False instead.
        if '__recursive' in d:
            __recursive = d['__recursive']
            del d['__recursive']
        else:
            __recursive = True
        if '__default' in d:
            __default = d['__default']
            del d['__default']
            self.__default = __default
            self.__has_default = True
        else:
            self.__has_default = False
        # keep the input as a reference. Destructuring breaks this reference.
        self.__is_recursive = __recursive
        self.__d = d

    def __getattribute__(self, item):
        logging.debug("__getattribute__({})".format(item))
        return object.__getattribute__(self, item)

    def __deepcopy__(self, memodict={}):
        raise NotImplementedError('todo: need to implement deepcopy')

    @property
    def __dict__(self):
        logging.debug("__dict__()")
        return self.__d

    def __bool__(self):
        return bool(self.__dict__)

    def __dir__(self):
        return self.__dict__.keys()

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self):
        # Not called during dict(bear)
        return self.__dict__.__iter__()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delitem__(self, key):
        del self.__d[key]

    def __getattr__(self, item):
        logging.debug("__getattr__({})".format(item))
        try:
            value = self.__d[item]
        except KeyError:
            __d = self.__d
            if hasattr(__d, item):
                return getattr(__d, item)
            elif self.__has_default:
                factory = self.__default
                if callable(factory):
                    value = factory()
                else:
                    value = factory
            else:
                raise AttributeError("attribute {} does not exist on {}".format(item, __d))
        if type(value) == dict and self.__is_recursive:
            return Bear(**value)
        else:
            return value

    def __setattr__(self, key, value):
        logging.debug("__setattr__({}, {})".format(key, value))
        if key[:7] == '_Bear__':
            super().__setattr__(key, value)
        elif key[:2] == '__':
            super().__setattr__(key, value)
        else:
            self.__d[key] = value


class DefaultBear(Bear):
    def __init__(self, default, **d):
        super().__init__(__default=default, **d)
