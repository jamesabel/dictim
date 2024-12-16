from dictim import dictim, as_dict

test_cases = [dictim({"A": 1, "B": 2}),
              dictim({"a": 1, "b": 2}),
              dictim({"A": 1, "B": [2, 3, None]}),
              dictim({"A": 1, "B": dictim({"C": 3})}),
              dictim({"A": 1, "B": [dictim({"d": 3}), dictim({"D": 4}), {'a', 2, 3}]}),
              dictim({"A": 1, "B": dictim({"C": 3, "D": dictim({"E": 5})})})]

def test_as_dict_method():
    for test_case in test_cases:
        d_as_dict = test_case.as_dict()
        assert isinstance(d_as_dict, dict)
        assert d_as_dict == test_case

def test_as_dict_function():
    for test_case in test_cases:
        d_as_dict = as_dict(test_case)
        assert isinstance(d_as_dict, dict)
        assert d_as_dict == test_case
