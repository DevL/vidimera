def identity(value):
    return value


class SimpleObject:
    A_CONSTANT = 1
    A_CALLABLE_CONTSTANT = identity
    A_LAMBDA = lambda x, y: x + y  # noqa

    def __init__(self, value):
        self.value = value

    def public_method(self, *args, **kwargs):
        pass

    def _private_method(self):
        pass

    def __call__(self, func):
        return func(self.value)

    def __eq__(self, other):
        return self.value == other
