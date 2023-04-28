# Vidimera

![PyPI](https://img.shields.io/pypi/v/vidimera)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vidimera)
![PyPI - Status](https://img.shields.io/pypi/status/vidimera)
![PyPI - License](https://img.shields.io/pypi/l/vidimera)
[![Python package](https://github.com/DevL/vidimera/actions/workflows/python-package.yml/badge.svg)](https://github.com/DevL/vidimera/actions/workflows/python-package.yml)

_Python signature and behaviour checker inspired by Elixir._

In Swedish, _vidimera_ means _to attest_ or _to certify_. It is commonly used to attest that a copy of a document is accurate compared to the original.

## Installation

Install the package `vidimera` version `1.0+` from PyPI.
The recommended `requirements.txt` line is `vidimera~=1.0`.

## Current Functionality

### `Behaviour(object)`
- Creates a new `Behaviour` instance.
- If `object` already is an instance of `Behaviour`, it is returned unchanged.

### `behaviour.implemented_by(other)`
- Verifies that `other` at least has the same public and dunderscore callables with the same signatures as the `behaviour`.
- Creats a `Behaviour` from `other` before making the comparison.

### `behaviour.implements(other)`
- Verifies that the `behaviour` at least has the same public and dunderscore callables with the same signatures as `other`.
- Creats a `Behaviour` from `other` before making the comparison.

### `behaviour.signatures(scope=Behaviour.PUBLIC_AND_SPECIAL)`
- Returns a `set` of tuples that represent the name and the callable selected based on the `scope`.
- Possible scopes include `PUBLIC`, `PRIVATE`, `SPECIAL`, and `PUBLIC_AND_SPECIAL`.
