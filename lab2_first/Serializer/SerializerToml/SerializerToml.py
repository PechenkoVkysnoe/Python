import inspect
from types import FunctionType
from Serializer.SerializerToml.constants import PRIMITIVES


def serialize(obj):
    if isinstance(obj, PRIMITIVES):
        return obj

    elif is_function(obj):
        return serialize_function(obj)

    elif inspect.iscode(obj):
        return serialize_code(obj)

    elif inspect.isclass(obj):
        return serialize_class(obj)

    elif is_iterable(obj):
        return serialize_iterable(obj)

    else:
        try:
            return serialize_object(obj)
        except TypeError:
            raise TypeError


def serialize_function(obj):
    if inspect.ismethod(obj):
        obj = obj.__func__

    glob = get_globals(obj)
    arguments = {}

    for (key, value) in inspect.getmembers(obj.__code__):
        if key.startswith("co_"):

            if isinstance(value, bytes):
                value = list(value)

            elif is_iterable(value) and not isinstance(value, str):
                data = []

                for val in value:
                    if val is not None:
                        data.append(serialize(val))

                    else:
                        data.append("None")

                arguments[key] = data
                continue

            arguments[key] = value

    result = {"__type__": "function_type",
              "__name__": obj.__name__,
              "__globals__": serialize_iterable(glob),
              "__args__": arguments}

    return result


def serialize_object(obj):
    result = {"__type__": "object_type", "__class__": obj.__class__.__name__}

    for attr in dir(obj):

        if not attr.startswith("__"):
            value = serialize(getattr(obj, attr))
            result[attr] = value

    return result


def serialize_class(obj):
    result = {'__type__': 'class_type', '__name__': obj.__name__}

    for attr in dir(obj):
        if attr == "__init__":
            attr_value = getattr(obj, attr)
            result[attr] = serialize_function(attr_value)

        if not attr.startswith('__'):
            attr_value = getattr(obj, attr)
            result[attr] = serialize(attr_value)

    return result


def is_iterable(obj):
    result = getattr(obj, "__iter__", None) is not None

    return result


def is_function(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj)


def get_globals(func):
    result = {}

    for global_var in func.__code__.co_names:

        if func.__name__==global_var:
            continue

        if global_var in func.__globals__:
            result[global_var] = func.__globals__[global_var]

    return result


def serialize_iterable(obj):
    result = None

    if isinstance(obj, list) or isinstance(obj, tuple):
        result = []

        for value in obj:
            if value is None:
                result.append("None")

            result.append(serialize(value))

    elif isinstance(obj, dict):
        result = {}

        for key, value in obj.items():
            result[key] = serialize(value)

    return result


def serialize_code(obj):
    result=serialize_function(FunctionType(obj, {}))
    return result
