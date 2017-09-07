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
        self.__is_recursive = __recursive
        if '__default' in d:
            __default = d['__default']
            del d['__default']
            self.__default = __default
            self.__has_default = True
        # keep the input as a reference. Destructuring breaks this reference.
        self.__d = d

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

    # def keys(self):
    #     print("****************************************")
    #     return self.__dict__.keys()

    def __getattr__(self, key):
        try:
            value = self.__d[key]
        except KeyError:
            if hasattr(self.__d, key):
                return getattr(self.__d, key)
            elif self.__has_default:
                factory = self.__default
                if callable(factory):
                    value = factory()
                else:
                    value = factory
            else:
                raise AttributeError("attribute {} does not exist".format(key))
        if type(value) == dict and self.__is_recursive:
            return Bear(**value)
        else:
            return value

    def __getattribute__(self, key):
        d = super().__getattribute__('__d')
        if key == "_Bear__d" or key == "__dict__":
            return d
        elif key in ["_Bear__is_recursive", "__is_recursive"]:
            return super().__getattribute__("__is_recursive")
        elif key in ["_Bear__default", "__default"]:
            return super().__getattribute__("__default")
        elif key in ["_Bear__has_default", "__has_default"]:
            return super().__getattribute__("__has_default")
        elif hasattr(d, key):
            return getattr(d, key)
        else:
            return super().__getattr__(key)

    def __setattr__(self, key, value):
        if key == "_Bear__d":
            super().__setattr__("__d", value)
        elif key == "_Bear__is_recursive":
            super().__setattr__("__is_recursive", value)
        elif key == "_Bear__default":
            super().__setattr__("__default", value)
        elif key == "_Bear__has_default":
            super().__setattr__("__has_default", value)
        else:
            self.__d[key] = value


class DefaultBear(Bear):
    def __init__(self, default, **d):
        super().__init__(__default=default, **d)
