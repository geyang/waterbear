# waterbear, A utility that makes python dictionary accessible with the dot notation

## Usage
```python
from waterbear import Bear

waterbear = Bear(**{"key": 100})
assert waterbear.key == 100, 'now waterbear.key is accessible!'
```