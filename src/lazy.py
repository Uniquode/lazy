# -*- coding: utf-8 -*-
from functools import wraps
import operator

__all__ = (
    'LazyObject',
    'LazyWrapper'
)


empty = object()


class LazyObject:

    def __init__(self, factory: type, *args, **kwargs):
        self.__dict__['_wrapped'] = empty
        self.__dict__.update(
            __factory=factory,
            __args=args,
            __kwargs=kwargs
        )

    def _setup(self):
        factory = self.__dict__['__factory']
        args = self.__dict__['__args']
        kwargs = self.__dict__['__kwargs']
        self._wrapped = factory(*args, **kwargs)

    def new_method_proxy(func):
        """ routes functions to the nexted object """
        @wraps(func)
        def inner(self, *args, **kwargs):
            if self._wrapped is empty:
                self._setup()
            return func(self._wrapped, *args, **kwargs)
        return inner

    def __setattr__(self, name: str, value):
        """ handle special variables and redirect others to wrapped """
        if name in {'_wrapped'}:
            self.__dict__[name] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name != '_wrapped':
            if self._wrapped is empty:
                self._setup()
            delattr(self._wrapped, name)

    __getattr__ = new_method_proxy(getattr)
    __bytes__ = new_method_proxy(bytes)
    __str__ = new_method_proxy(str)
    __bool__ = new_method_proxy(bool)
    __dir__ = new_method_proxy(dir)
    __hash__ = new_method_proxy(hash)
    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __lt__ = new_method_proxy(operator.lt)
    __gt__ = new_method_proxy(operator.gt)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)


def LazyWrapper(cls, *args, **kwargs):

    ClassName = cls.__name__

    class LazyClass(LazyObject):

        __metaclass__ = cls

        def __init__(self, cls, *args, **kwargs):
            super().__init__(cls, *args, **kwargs)

    return LazyClass(cls, *args, **kwargs)
