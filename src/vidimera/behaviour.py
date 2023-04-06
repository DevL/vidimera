from inspect import signature


class Behaviour:
    NO_SIGNATURE = object()

    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return f"<Behaviour of {repr(self.obj)}>"

    def signatures(self):
        contents = dir(self.obj)
        included = filter(_included, contents)
        candidates = map(self._name_and_attribute, included)
        callables = filter(_callable, candidates)
        return {(name, _safe_signature(func)) for name, func in callables}

    def _name_and_attribute(self, name):
        return name, getattr(self.obj, name)


def _callable(name_and_attribute):
    return callable(name_and_attribute[1])


def _included(name):
    return _public(name) or _special_method(name)


def _public(name):
    return not _private(name)


def _private(name):
    return name.startswith("_")


def _special_method(name):
    return name.startswith("__") and name.endswith("__")


def _safe_signature(func):
    try:
        return signature(func)
    except ValueError:
        return Behaviour.NO_SIGNATURE
