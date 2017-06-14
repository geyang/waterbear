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
        # keep the input as a reference. Destructuring breaks this reference.
        self.__d = d

    def __dir__(self):
        return self.__dict__.keys()

    def __str__(self):
        return str(self.__dict__)

    def __getattr__(self, key):
        value = self.__d[key]
        if type(value) == type({}) and self.__is_recursive:
            return Bear(**value)
        else:
            return value

    def __getattribute__(self, key):
        if key == "_Bear__d" or key == "__dict__":
            return super().__getattribute__("__d")
        elif key in ["_Bear__is_recursive", "__is_recursive"]:
            return super().__getattribute__("__is_recursive")
        else:
            return super().__getattr__(key)

    def __setattr__(self, key, value):
        if key == "_Bear__d":
            super().__setattr__("__d", value)
        elif key == "_Bear__is_recursive":
            super().__setattr__("__is_recursive", value)
        else:
            self.__d[key] = value


if __name__ == "__main__":
    # test dictionary to object
    test_dict = {
        'a': 0,
        'b': 1
    }

    test_args = Bear(**test_dict)
    assert test_args.a == 0
    assert test_args.b == 1
    test_args.haha = 0
    assert test_args.haha == 0
    test_args.haha = {'a': 1}
    assert test_args.haha != {'a': 1}
    assert vars(test_args.haha) == {'a': 1}
    assert test_args.haha.a == 1
    assert test_args.__dict__['haha']['a'] == 1
    assert vars(test_args)['haha']['a'] == 1
    print(test_args)

    test_args = Bear(__recursive=False, **test_dict)
    assert test_args.__is_recursive == False
    assert test_args.a == 0
    assert test_args.b == 1
    test_args.haha = {'a': 1}
    assert test_args.haha['a'] == 1
    assert test_args.haha == {'a': 1}


    # Some other usage patterns
    test_args = Bear(**test_dict, **{'ha': 'ha', 'no': 'no'})
    print(test_args.ha)
