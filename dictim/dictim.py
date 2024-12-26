import collections.abc
from typing import Iterable, Any
from copy import deepcopy

try:
    from pydantic_core import CoreSchema, core_schema
    from pydantic import GetCoreSchemaHandler

    using_pydantic = True
except ImportError:
    CoreSchema = Any
    core_schema = Any
    GetCoreSchemaHandler = Any
    using_pydantic = False


class DictimValidationError(Exception):
    """Custom exception for dictim validation errors."""

    pass


def as_dict(d):
    """
    Recursively converts a dictim to a regular dict
    """
    if isinstance(d, dictim):
        ret_d = as_dict(dict(d))
    elif isinstance(d, list):
        ret_d = [as_dict(x) for x in d]
    else:
        ret_d = deepcopy(d)
    return ret_d


class dictim(collections.abc.MutableMapping):
    """
    This is originally taken from Requests' CaseInsensitiveDict ( https://github.com/psf/requests ), but removed from that package so we
    don't take on the baggage of requiring the Requests package itself.  Also made some modifications like using collections.abc and casefold.
    Requests is licensed under the Apache License, Version 2.0
    """

    """
    A case-insensitive ``dict``-like object.
    Implements all methods and operations of
    ``collections.MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.
    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive:
        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True
    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.
    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.casefold()``s, the
    behavior is undefined.
    """

    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.casefold()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.casefold()][1]

    def __delitem__(self, key):
        del self._store[key.casefold()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return ((lowerkey, keyval[1]) for (lowerkey, keyval) in self._store.items())

    def __eq__(self, other):
        if isinstance(other, collections.abc.Mapping):
            other = dictim(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
        return dictim(self._store.values())

    def __repr__(self):
        return f"{dict(self.items())}"

    def deep_get(self, keys: Iterable, default_value: Any = None) -> Any:
        """
        liberal deep get - gets a value from a nested dict or dictim, with a default value. Default value is returned whenever a key is not found.
        Nested dicts are treated as dictims. No error checking is done - if key(s) aren't found, the default value is returned.
        e.g.
        a = dictim({"a": {"b": 1}})
        a.deep_get(["a", "b"])  # returns 1

        :param keys: keys to iterate over, used to descend into a dictim
        :param default_value: default value in case keys don't find a corresponding value
        :return: leaf value or None if not found
        """
        value = self  # type: Any
        for key in keys:
            try:
                value = value.get(key, default_value)
                if isinstance(value, dict):
                    value = dictim(value)  # convert all dicts to dictims
            except AttributeError:
                value = default_value  # .get() raised AttributeError
                break
        return value

    def as_dict(self) -> dict:
        """
        Recursively converts this dictim to a regular dict
        :return: a regular dict
        """
        return as_dict(self)

    # pydantic field compatibility

    if using_pydantic:

        @classmethod
        def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
            return core_schema.no_info_after_validator_function(cls, handler.generate_schema(dict))

        @classmethod
        def validate(cls, value: Any, field: str):
            if isinstance(value, dictim):
                return value
            if isinstance(value, dict):
                return dictim(value)
            raise DictimValidationError(f"Invalid type for dictim: {type(value)}")
