from dictim import dictim


def test_deep_get_simple():
    a = dictim({"a": {"b": 1}})
    v = a.deep_get(["a", "b"])  # list
    assert v == 1


def test_deep_get():
    test_dict = dictim({"a": {"B": {"C": 1 + 2j}}})  # B and C are upper case, but it'll work since .deep_get converts all regular dict's to dictim
    value = test_dict.deep_get(("a", "b", "c"))  # tuple
    assert value == 1 + 2j


def test_deep_get_type_error():

    # attempt to get "c" from 3 (will raise a DictimError)
    test_dict = dictim({"a": {"b": 3}})

    value = test_dict.deep_get(["a", "b", "c"])
    assert value is None


def test_deep_get_key_error_simple():

    # Attempt to get value using key "b" (doesn't exist). Will return None.
    test_dict = dictim({"a": {"x": "y"}})

    value = test_dict.deep_get(["a", "b"])
    assert value is None


def test_deep_get_key_error_deep():

    # Attempt to get value using key "b" (doesn't exist). Will return None.
    test_dict = dictim({"a": {"x": {"y": "z"}}})

    value = test_dict.deep_get(["a", "b", "c"])
    assert value is None


def test_deep_get_default():
    test_dict = dictim({"a": {"x": "y"}})

    value = test_dict.deep_get(["a", "b"], 1)
    assert value is 1
