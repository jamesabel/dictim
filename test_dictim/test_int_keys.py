from dictim import dictim


def test_int_keys():
    d = dictim({1: "one", 2: "two"})
    assert d[1] == "one"


def test_int_key_delete():
    d = dictim({1: "one", 2: "two"})
    del d[1]
    assert d == dictim({2: "two"})
