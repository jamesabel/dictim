import collections.abc
from typing import Iterable, Any, get_args
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
    Converts a dictim to a regular dict
    """
    return dict(deepcopy(d))


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
        if isinstance(key, str):
            self._store[key.casefold()] = (key, value)
        else:
            self._store[key] = (key, value)

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._store[key.casefold()][1]
        else:
            return self._store[key][1]

    def __delitem__(self, key):
        if isinstance(key, str):
            del self._store[key.casefold()]
        else:
            del self._store[key]

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
        def __get_pydantic_core_schema__(cls, source_type: type[object], handler: callable) -> core_schema.CoreSchema:
            def with_info_validate(value: object, info: core_schema.ValidationInfo) -> dictim:
                if len(key_type_args := get_args(source_type)) > 0:
                    # restore int keys from JSON
                    key_type = key_type_args[0]
                    if key_type is int and isinstance(value, dict):
                        return dictim({int(k): v for k, v in value.items()})
                if isinstance(value, cls):
                    return value
                raise TypeError(f"Cannot create {cls.__name__} from {type(value)}")

            def serialize(value: dictim) -> dict:
                return value.as_dict()

            return core_schema.with_info_plain_validator_function(
                function=with_info_validate,
                serialization=core_schema.plain_serializer_function_ser_schema(function=serialize),
            )
