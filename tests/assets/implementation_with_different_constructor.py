class ImplementationWithDifferentConstructor:
    def __init__(self, arg, keyword="different", another=True):
        pass

    def method(self, a, b):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name}"
