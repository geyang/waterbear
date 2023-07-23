import logging

from copy import deepcopy


class Bear:
    """
    Bear automatically injects the key value pairs into the class at construction.

    Note: Bear does NOT automatically inject attributes of the current name space
        into the dictionary. This ia  good thing. To use the object as a namespace,
        use params-proto's ParamsProto or PrefixProto instead.

    - Ge
    """
    def __init_subclass__(cls, **kwargs):
        # intercept the kwargs in the init_subclass call
        super().__init_subclass__()

    def __init__(self, **d):
        """
        Features:

        0. Take in a list of keyword arguments in constructor, and assign them as attributes
        1. Correctly handles `dir` command, so shows correct auto-completion in editors.
        2. Correctly handles `vars` command, and returns a dictionary version of self.

        default: if d['new_key'] is queried, the default value is inserted into the dictionary.

        # todo: finish this documentation
        When recursive is set to False,

        :param __recursive
        :param __default
        :param __idempotent_get
        """
        # double underscore variables are mangled by python, so we use keyword argument dictionary instead.
        # Otherwise you will have to use __Bear_recursive = False instead.
        if '__recursive' in d:
            __recursive = d['__recursive']
            del d['__recursive']
        else:
            __recursive = True
        self.__is_recursive = __recursive
        if '__default' in d:
            self.__default = d['__default']
            del d['__default']
            self.__has_default = True
        else:
            self.__has_default = False
        if '__idempotent_get' in d:
            self.__idempotent_get = d['__idempotent_get']
            del d['__idempotent_get']
        else:
            self.__idempotent_get = False  # the default value of idempotent_get is False.
        # keep the input as a reference. Destructuring breaks this reference.
        self.__d = d

    def __getattribute__(self, item):
        """
        Waterbear get attribute method. Deligate to system default if
        the attribute is not found in the local dictionary.

        Child classes need to escape things like static methods, properties etc.
        in the Bear constructor, so that they are not returned as is.

        1. First try to detect if method is private
        2. then tries to retrieve it from the local dict
        3. If that fails, try using super method again.

        note-1: Because we make a `__d` call, we need to filter for recursion.
        note-2: Always check the dictionary first.
        """
        if item.startswith("__") or item.startswith("_Bear"):
            return super(Bear, self).__getattribute__(item)
        try:
            value = self.__d[item]
            if type(value) == dict and self.__is_recursive:
                bear = Bear()
                bear.__d = value
                return bear
            else:
                return value
        except:
            return super(Bear, self).__getattribute__(item)

    def __copy__(self):
        if self.__has_default:
            return Bear(__default=self.__default, __recursive=self.__is_recursive, **vars(self))
        else:
            return Bear(__recursive=self.__is_recursive, **vars(self))

    copy = __copy__

    def __deepcopy__(self, memodict=None):
        # if memodict is None:
        #     memodict = dict()
        if self.__has_default:
            return Bear(__default=self.__default, __recursive=self.__is_recursive, **deepcopy(dict(self)))
        else:
            return Bear(__recursive=self.__is_recursive, **deepcopy(dict(self)))
        # todo: use memodict to avoid infinite recursion.
        # not_there = []
        # existing = memo.get(self, not_there)
        # if existing is not not_there:
        #     print
        #     '  ALREADY COPIED TO', repr(existing)
        #     return existing
        # pprint.pprint(memo, indent=4, width=40)
        # dup = Graph(copy.deepcopy(self.name, memo), [])
        # print
        # '  COPYING TO', repr(dup)
        # memo[self] = dup
        # for c in self.connections:
        #     dup.addConnection(copy.deepcopy(c, memo))
        # return dup

    @property
    def __dict__(self):
        # logging.debug("__dict__()")
        return self.__d

    def __setstate__(self, state):
        self.__d = state['__dict__']
        self.__is_recursive = state["__is_recursive"]
        self.__has_default = state["__has_default"]
        self.__idempotent_get = state["__idempotent_get"]
        if state['__has_default']:
            self.__default = state["__default"]

    def __getstate__(self):
        state_dict = {
            "__dict__": self.__dict__,
            "__is_recursive": self.__is_recursive,
            "__has_default": self.__has_default,
            "__idempotent_get": self.__idempotent_get,
        }
        if state_dict['__has_default']:
            state_dict["__default"] = self.__default
        return state_dict

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
        # logging.debug("__getattr__({})".format(item))
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
                # implement "get" method to get around  
                if not self.__idempotent_get:
                    self[item] = value
            else:
                raise AttributeError("attribute {} does not exist on {}".format(item, __d))
        if type(value) == dict and self.__is_recursive:
            bear = Bear()
            bear.__d = value
            return bear
        else:
            return value

    def __setattr__(self, key, value):
        if key[:7] == '_Bear__':
            object.__setattr__(self, key, value)
        elif key[:2] == '__':
            object.__setattr__(self, key, value)
        else:
            self.__d[key] = value

    def __delattr__(self, item):
        if item[:7] == '_Bear__':
            object.__delattr__(self, item)
        elif item[:2] == '__':
            object.__delattr__(self, item)
        else:
            del self.__d[item]


class DefaultBear(Bear):
    def __init__(self, _default, _idempotent_get=False, **d):
        """

        :param _default:
        :param _idempotent_get:
            make the getattribute calls idempotent, which means it does NOT insert new values when queried.
        :param d: key-value pairs.
        """
        super().__init__(__default=_default, __idempotent_get=_idempotent_get, **d)


from types import SimpleNamespace


class OrderedBear(SimpleNamespace):
    __RESERVED_KEYS = 'items', 'values', 'keys'

    def items(self):
        return [(k, getattr(self, k)) for k in self.__class__.__dict__.keys() if
                not k.startswith('_') and k not in self.__RESERVED_KEYS]

    def values(self):
        return [getattr(self, k) for k in self.__class__.__dict__.keys() if
                not k.startswith('_') and k not in self.__RESERVED_KEYS]

    def keys(self):
        return [k for k in self.__class__.__dict__.keys() if not k.startswith('_') and k not in self.__RESERVED_KEYS]
