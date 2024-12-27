from dictim import dictim


def test_list():
    with_list = {"hi": [1, 2, 3]}
    my_dictim = dictim(with_list)
    d = my_dictim.as_dict()
    assert d == with_list
