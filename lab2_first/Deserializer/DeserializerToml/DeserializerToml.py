import builtins
import inspect
from types import FunctionType, CodeType
from Serializer.SerializerToml.constants import PRIMITIVES


def deserialize(s):
    if isinstance(s, PRIMITIVES):
        return s

    elif isinstance(s, dict):
        if "function_type" in s.values():
            return deserialize_function(s)

        elif "object_type" in s.values():
            return deserialize_object(s)

        elif "class_type" in s.values():
            return deserialize_class(s)

        else:
            try:
                return deserialize_iterable(s)
            except TypeError:
                raise TypeError

    elif is_iterable(s):
        return deserialize_iterable(s)


def deserialize_function(s):
    arguments = s["__args__"]
    globs = s["__globals__"]
    globs["__builtins__"] = builtins

    for key in s["__globals__"]:
        if key in arguments["co_names"]:
            globs[key] = deserialize(s["__globals__"][key])

    temp_consts = []

    for val in list(arguments["co_consts"]):
        func = deserialize(val)

        if is_function(func):
            val = deserialize(val)
            temp_consts.append(val.__code__)

        temp_consts.append(val)

    arguments["co_consts"] = temp_consts

    for val in arguments:
        if is_iterable(arguments[val]) and not isinstance(arguments[val], str):
            temp_ls = []
            for value in arguments[val]:
                if value == "None":
                    temp_ls.append(None)
                else:
                    temp_ls.append(value)
            arguments[val] = temp_ls

    result = FunctionType(CodeType(arguments['co_argcount'],
                                   arguments['co_posonlyargcount'],
                                   arguments['co_kwonlyargcount'],
                                   arguments['co_nlocals'],
                                   arguments['co_stacksize'],
                                   arguments['co_flags'],
                                   bytes(arguments['co_code']),
                                   tuple(arguments['co_consts']),
                                   tuple(arguments['co_names']),
                                   tuple(arguments['co_varnames']),
                                   arguments['co_filename'],
                                   arguments['co_name'],
                                   arguments['co_firstlineno'],
                                   bytes(arguments['co_lnotab']),
                                   tuple(arguments['co_freevars']),
                                   tuple(arguments['co_cellvars'])), globs)
    result.__globals__.update({result.__name__: result})
    return result


def deserialize_object(s):
    meta = type(s.get("__class__"), (), {})
    result = meta()

    for key, value in s.items():

        if key == '__class__':
            continue

        setattr(result, key, deserialize(value))

    return result


def deserialize_class(s):
    my_vars = {}

    for attr, value in s.items():
        my_vars[attr] = deserialize(value)

    result = type(s["__name__"], (), my_vars)
    return result


def is_iterable(obj):
    result = getattr(obj, "__iter__", None) is not None

    return result


def is_function(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj)


def deserialize_iterable(obj):
    result = None

    if isinstance(obj, list) or isinstance(obj, tuple):
        result = []

        for value in obj:
            if value == "None":
                result.append(None)

            result.append(deserialize(value))

    elif isinstance(obj, dict):
        result = {}

        for key, value in obj.items():
            result[key] = deserialize(value)

    return result
