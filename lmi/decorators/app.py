from lmi.app import App


def app(*a, **kw):
    def wrapper(func):
        return App(*a, func=func, **kw)

    return wrapper
