# Vidimera

![PyPI](https://img.shields.io/pypi/v/vidimera)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vidimera)
![PyPI - Status](https://img.shields.io/pypi/status/vidimera)
![PyPI - License](https://img.shields.io/pypi/l/vidimera)
[![Python package](https://github.com/DevL/vidimera/actions/workflows/python-package.yml/badge.svg)](https://github.com/DevL/vidimera/actions/workflows/python-package.yml)

_Python signature and behaviour checker inspired by Elixir._

In Swedish, _vidimera_ means _to attest_ or _to certify_. It is commonly used to attest that a copy of a document is accurate compared to the original.  

## Installation

Install the package `oh_behave` version `1.0+` from PyPI.
The recommended `requirements.txt` line is `oh_behave~=1.0`.

## Planned Functionality

### `Behaviour(object)
- a new behaviour instance
- If object already is an instance of Behaviour, it is returned unchanged.

### `behaviour.implemented_by(other)`
- verifies that other has the same public and dunderscore callables with the same signatures as the behaviour.

### `behaviour.implements(other_behaviour)`
- Convenience alias for other_behaviour.implemented_by(behaviour)
- If other_behaviour is not an instance of Behaviour, it will be turned into one. 


### Comparison operators
`__ge__` and `__le__` could be added, but `__gt__` and `__lt__` would not make much sense semantically. Using `__eq__` as an alias for `implements` would lead to nice tests, though it wouldn’t actually be semantically correct AND it wouldn’t be transitive. Implementing `in` could be an alternative.

```python
assert Behaviour(a) == Behaviour(b)
assert Behaviour(a) <= Behaviour(b)
assert Behaviour(b) in Behaviour(a)
```

Expected Behaviour
- public functions/methods (callables)
- dunderscore callables
- NOT private callables
- NOT callables that inspect.signature fails on (ValueError/TypeError)
    - Should these be checked for existence, but not signature?
    - Should these be listed as unchecked?
