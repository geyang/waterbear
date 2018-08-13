![waterbear_is_a_bear](./figures/waterbear.jpg)

# `waterbear`, A Base Classs That Makes Python Dictionary Accessible With The Dot Notation, Recursively and with Default Values

Now introducing the smallest bear! **Waterbear**.

Waterbear makes it easy to use python dictionaries with dot notation!

## What does `Waterbear`:bear: do?

`Waterbear` is like `defaultdict` + `SimpleNameSpace` + `namedtuples`.

`Waterbear` is similar in usage to `namedtuples` or `recordtypes`, but it is not a tuple or array type but a dictionary. The distinction
is that `Waterbear` attributes are accessible via `key` strings instead of index numbers.

`Waterbear` is more similar to `types.SimpleNamespace`. However, a major difference is that `Waterbear` enables:

- setting default values via a `default_factory` during instantiation
- all attributes are recognized by IDE's static type-checking so they have auto-completion without having to be used first.
- work recursively

Now with all of these three, there isn't an alternative solution available. libraries like `Munch`
has bad support for pythonic idioms. In this case `Waterbear` allows you to:

- use `vars(bear)` to convert the bear object into a dictionary.
- use `dict(bear)` for the same purpose
- use `print(bear)` and get a dictionary string
- ... all methods that are available in a python `dict` object

## TODOs

- [ ] fix class extension usage pattern
- [ ] ~~merge `python2.7` version with `python3`~~
- [ ] ~~make another package called `tardigrade `~~

## Installation 

```python
pip install waterbear
```

## Usage

For more usage examples, take a look at the [test.py](./waterbear/test_waterbear.py)!

There are two classes, the `Bear` and the `DefaultBear`. Default Bear allows you to pass in a
default factory as the first argument. `Bear` allows you do do so via a keyword argument `__default`

Example usage below:

```python
# Waterbear is a bear!
from waterbear import Bear

waterbear = Bear(**{"key": 100})
assert waterbear.key == 100, 'now waterbear.key is accessible!'
assert waterbear['key'] == 100, 'item access syntax is also supported!'
```

### Similar to `collection.defaultdict`, there is `DefaultBear`

```python
bear = DefaultBear(None, a=10, b=100)
assert vars(bear) == {'a': 10, 'b': 100}

assert bear.does_not_exist is None, "default value works"
```

### DefaultBear like `defaultdict`

You can use the `DefaultBear` class and pass in a default factor as the first parameter.

```python
bear = DefaultBear(tuple, a=10, b=100)
assert bear.does_not_exist is (), "default factory also works!"
```

### You can also use it with `vars`, `str`, `print(repr)`, `dict` etc.

```python
bear = Bear(a=10, b=100)
assert str(bear) == "{'a': 10, 'b': 100}"
assert dir(bear) == ['a', 'b']
assert list(iter(bear)) == ['a', 'b']
assert dict(bear) == {'a': 10, 'b': 100}
```

### As Bool in Condition Logic

When used in conditional logic, `Bear` and `DefaultBear` behaves exactly like an ordinary dictionary!

```python
def test_dict_comparison():
    bear = Bear()
    assert not {}, 'empty dictionary are treated as False value.'
    assert not bear, 'bear should be treated as False value too!'
```

### Using with Pickle

When using with default factories, only non-callables are picklable.

```python
def test_pickle_setstate_getstate():
    # create a default bear with a default factory
    bear = DefaultBear('hey', a=10, b=100)
    pickle_string = pickle.dumps(bear)
    bear_reborn = pickle.loads(pickle_string)
    assert type(bear_reborn) == DefaultBear
    assert vars(bear_reborn) == {'a': 10, 'b': 100}

    bear = DefaultBear(lambda: 'hey', a=10, b=100)
    function_fails = False
    try:
        pickle.dumps(bear)
    except AttributeError as e:
        function_fails = True
    assert function_fails
```

### Using deepcopy

You can just do `copy.deepcopy(bear)`!

```python
def test_deepcopy():
    from copy import deepcopy
    original = Bear(a=1, b={'ha': 0})
    copy = deepcopy(original)
    copy.b.ha += 1
    assert copy.b.ha == 1
    assert original.b.ha == 0
```

### As A Base Class

Waterbear is completely rewritten to play well with class extension!

```python
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
```

### Order Preserving SimpleNamespace

In tensorflow, you frequently need order preserving namespaces that you can use for `sess.run([tensors... `. 
We built `OrderedBear` exactly for this purpose. It is an extension of the `types.SimpleNamespace` class.

```
# First declare the typings (namespace) for your model
class Reporting:
    loss=None
    entropy=None
    mean_kl=None

# Now, you can instantiate this with new values

... inside model

    r = Reporting(entropy=-5, loss=1)
    # Notice that 1. we are putting values in out-of-order, and 2. We are missing `mean_kl` in our construction.

    tems = r.items()
    assert items[0] == ('loss', 1), 'order follows class declaration.'
    assert items[1] == ('entropy', -5), 'entropy goes after loss even though this is the second atrribute'
    assert items[2] == ('mean_kl', None), 'undefined falls back to the default'

    values = r.values()
    assert values[0] == 1, 'order follows class declaration.'
    assert values[1] == -5, 'entropy goes after loss even though this is the second atrribute'
    assert values[2] == None, 'undefined falls back to the default'

    keys = r.keys()
    assert keys[0] == 'loss', 'order follows class declaration.'
    assert keys[1] == 'entropy', 'entropy goes after loss even though this is the second atrribute'
    assert keys[2] == 'mean_kl', 'undefined falls back to the default'
```


### More Usages Could Be Found in The Tests!

For more usage examples, take a look at [test.py](./waterbear/test_waterbear.py).

```python
test_dict = {
    'a': 0,
    'b': 1
}

# Use spread operators to construct with a dictionary!
test_args = Bear(**test_dict)
assert test_args.a == 0
assert test_args.b == 1
# the value should now be accessible through the key name.
test_args.haha = 0
assert test_args.haha == 0


# You can also use a nested dictionary.
test_args.haha = {'a': 1}
assert test_args.haha != {'a': 1}
assert vars(test_args.haha) == {'a': 1}
assert test_args.haha.a == 1
assert test_args.__dict__['haha']['a'] == 1
assert vars(test_args)['haha']['a'] == 1
assert str(test_args) == "{'a': 0, 'b': 1, 'haha': {'a': 1}}", \
    'test_args should be this value "{\'a\': 0, \'b\': 1, \'haha\': {\'a\': 1}}"'

# To set recursion to false, use this `__recursive` parameter.
test_args = Bear(__recursive=False, **test_dict)
assert test_args.__is_recursive == False
assert test_args.a == 0
assert test_args.b == 1
test_args.haha = {'a': 1}
assert test_args.haha['a'] == 1
assert test_args.haha == {'a': 1}

# Some other usage patterns
test_args = Bear(**test_dict, **{'ha': 'ha', 'no': 'no'})
assert test_args.ha == 'ha', 'key ha should be ha'
```

## To Develop

```python
git clone https://github.com/episodeyang/waterbear.git
cd waterbear
make dev
```

This `make dev` command should build the wheel and install it in your current python environment. Take a look at the [./Makefile](./Makefile) for details.

**To publish**, first update the version number, then do:
```bash
make publish
```

\* image credit goes to BBC [waterbear: The Smallest Bear!](http://www.bbc.com/earth/story/20150313-the-toughest-animals-on-earth) 😛
![tardigrade](./figures/waterbear_2.jpg)
