if __name__ == "__main__":
    # bear = Bear()
    # bear.npts = 10
    # print(vars(bear))

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
            print('END: __init__')

        def __getattribute__(self, item):
            print("__getattribute__({})".format(item))
            return object.__getattribute__(self, item)

        @property
        def __dict__(self):
            print("__dict__()")
            return self.__d

        def __getattr__(self, item):
            print("__getattr__({})".format(item))
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
            print("__setattr__({}, {})".format(key, value))
            if key[:7] == '_Bear__':
                super().__setattr__(key, value)
            elif key[:2] == '__':
                super().__setattr__(key, value)
            else:
                self.__d[key] = value


    bear = Bear()
    print(bear.__dict__)
    bear.npts = 10
    bear.__hidden_method__ = lambda: 'hey'
    print(bear.__hidden_method__())

    bear = Bear(__default=None)
    assert bear.npts is None
    bear.npts = 10
    assert bear.npts == 10


    class ExtendBear(Bear):
        def __init__(self, debug_dict=True, **d):
            super().__init__(**d)
            self._debug_dict = debug_dict

        def __some_method__(self):
            return '.__some_method__'

        @property
        def __dict__(self):
            if self._debug_dict:
                return ".__dict__"
            else:
                return super().__dict__


    e = ExtendBear()
    assert e.__some_method__() == ".__some_method__"
    assert e.__dict__ == ".__dict__"
    e = ExtendBear(debug_dict=False)
    assert e.__dict__ == {'_debug_dict': False}

    raised_error = False
    try:
        print(e.does_not_exist)
    except AttributeError:
        raised_error = True
    assert raised_error



