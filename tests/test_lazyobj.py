from lazy import LazyObject


class MyObject():
    zero = 0

    def __init__(self, first, second=2, third='three'):
        self.first = first
        self.second = second
        self.third = third


def test_lazy_object():
    obj = LazyObject(MyObject, 'x')
    assert obj.__class__ == MyObject
    assert isinstance(obj, MyObject)
    assert isinstance(obj, LazyObject)
    assert obj.zero == 0
    assert obj.first == 'x'
    assert obj.second == 2
    assert obj.third == 'three'


def test_lazy_object_with_args():
    obj = LazyObject(MyObject, None, third=3)
    assert obj.__class__ == MyObject
    assert isinstance(obj, MyObject)
    assert isinstance(obj, LazyObject)
    assert obj.zero == 0
    assert obj.first is None
    assert obj.second == 2
    assert obj.third == 3
