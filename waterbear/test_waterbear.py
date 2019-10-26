import pickle

from .waterbear import Bear, DefaultBear, OrderedBear


def test():
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
    assert str(test_args) == "{'a': 0, 'b': 1, 'haha': {'a': 1}}", \
        'test_args should be this value "{\'a\': 0, \'b\': 1, \'haha\': {\'a\': 1}}"'
    assert dir(test_args) == ['a', 'b', 'haha']

    test_args = Bear(__recursive=False, **test_dict)
    assert test_args._Bear__is_recursive == False
    assert test_args.a == 0
    assert test_args.b == 1
    test_args.haha = {'a': 1}
    assert test_args.haha['a'] == 1
    assert test_args.haha == {'a': 1}

    # Some other usage patterns
    test_args = Bear(**test_dict, **{'ha': 'ha', 'no': 'no'})
    assert test_args.ha == 'ha', 'key ha should be ha'


def test_default_bear():
    bear = DefaultBear(None, a=10, b=100)
    assert vars(bear) == {'a': 10, 'b': 100}

    assert bear.does_not_exist is None

    bear = DefaultBear(tuple, a=10, b=100)
    assert bear.does_not_exist is ()

    bear = DefaultBear(list)
    assert bear.not_idempotent == [], 'query attribute adds a new value.'
    bear.not_idempotent.append('ha')
    assert bear.not_idempotent == ['ha']

    bear = DefaultBear(list)
    bear.not_idempotent.append('ha')  # directly append to it also works.
    assert bear.not_idempotent == ['ha'], 'calling attribute adds a new value too.'

    # Idempotent Case
    bear = DefaultBear(list, _idempotent_get=True)
    bear.not_idempotent.append('ha')
    assert bear.not_idempotent == [], 'calling attribute does NOT add new values in idempotent mode.'


def test_dict_methods():
    bear = Bear(a=10, b=100)
    assert str(bear) == "{'a': 10, 'b': 100}"
    assert dir(bear) == ['a', 'b']


def test_dict_comparison():
    bear = Bear()
    assert not {}, 'empty dictionary are treated as False value.'
    assert not bear, 'bear should be treated as False value too!'


def test_default_dict_methods():
    bear = DefaultBear(None, a=10, b=100)
    assert list(iter(bear)) == ['a', 'b']
    assert dict(bear) == {'a': 10, 'b': 100}


def test_pickle_basic():
    # create a default bear with a default factory
    bear = DefaultBear('hey', a=10, b=100)
    pickle_string = pickle.dumps(bear)
    bear_reborn = pickle.loads(pickle_string)
    assert type(bear_reborn) == DefaultBear
    assert vars(bear_reborn) == {'a': 10, 'b': 100}


def test_pickle_callable():
    bear = DefaultBear(lambda: 'hey', a=10, b=100)
    function_fails = False
    try:
        pickle.dumps(bear)
    except AttributeError as e:
        function_fails = True
    assert function_fails


def test_pickle_non_default():
    bear = Bear(a=10, b=100)
    pickle_string = pickle.dumps(bear)
    bear_reborn = pickle.loads(pickle_string)
    assert type(bear_reborn) == Bear
    assert vars(bear_reborn) == {'a': 10, 'b': 100}


def test_deepcopy():
    from copy import deepcopy
    original = Bear(a=1, b={'ha': 0})
    original.a = 5
    assert original.a == 5
    original.b.ha = 1
    assert original.b.ha == 1
    original['b']['ha'] = 1
    assert original.b.ha == 1
    copy = deepcopy(original)
    copy.b.ha += 1
    assert copy.b.ha == 2
    assert original.b.ha == 1


def test_copy():
    from copy import copy
    original = Bear(a=1, b={'ha': 0})
    original.b.ha += 1
    assert original.b.ha == 1, 'original works.'
    new = copy(original)
    new.b.ha = 5
    assert new.b.ha == 5, "copy works"
    assert original.b.ha == 5, 'original is linked because this is a shallow copy.'


def test_as_dict_items():
    bear = DefaultBear(None, a=10, b=100)
    assert bear['a'] == 10
    bear['a'] = 11
    assert bear['a'] == 11
    del bear['a']
    assert bear['a'] is None

    bear.update(b=101)
    assert bear['b'] == 101


def test_as_object():
    bear = Bear(a=10, b=100)
    assert bear.a == 10
    bear.a = 11
    assert bear.a == 11

    del bear.a
    assert not hasattr(bear, 'a'), "the attribute `a` should not exist"

    delattr(bear, 'b')
    assert not hasattr(bear, 'b'), "the attribute `b` should not exist"

    bear = DefaultBear(None, a=10, b=100)
    assert bear.a == 10
    bear.a = 11
    assert bear.a == 11

    del bear.a
    assert hasattr(bear, 'a'), "DefaultBear always has the attribute"
    assert bear['a'] is None

    delattr(bear, 'b')
    assert hasattr(bear, 'b'), "DefaultBear always has the attribute"
    assert bear['b'] is None



def test_dict_update():
    bear = DefaultBear(None, a=10, b=100)
    bear.update(a=11)
    bear['a'] = 11


def test_simple_class_extension():
    class ExtendBear(Bear):
        @property
        def _hidden_stuff(self):
            return "._hidden_stuff"

        @property
        def __mangled_stuff(self):
            return ".__mangled_stuff"

        @property
        def __dict__(self):
            return ".__dict__"

    e = ExtendBear()
    assert e.__dict__ == ".__dict__"
    assert e._hidden_stuff == '._hidden_stuff'
    assert e._ExtendBear__mangled_stuff == ".__mangled_stuff"


def test_class_extension():
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


def test_order_bear():
    class Reports(OrderedBear):
        loss = None
        entropy = None
        mean_kl = None

    r = Reports(entropy=0, loss=1)

    items = r.items()
    assert items[0] == ('loss', 1), 'order follows class declaration.'
    assert items[1] == ('entropy', 0), 'entropy goes after loss even though this is the second atrribute'
    assert items[2] == ('mean_kl', None), 'undefined falls back to the default'

    values = r.values()
    assert values[0] == 1, 'order follows class declaration.'
    assert values[1] == 0, 'entropy goes after loss even though this is the second atrribute'
    assert values[2] == None, 'undefined falls back to the default'

    keys = r.keys()
    assert keys[0] == 'loss', 'order follows class declaration.'
    assert keys[1] == 'entropy', 'entropy goes after loss even though this is the second atrribute'
    assert keys[2] == 'mean_kl', 'undefined falls back to the default'
