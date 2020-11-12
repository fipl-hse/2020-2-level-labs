"""
A module of decorators for validation in lab_3
"""

from typing import get_type_hints

def has_none(arg):
    flattened = []
    to_check = [*arg]
    while to_check:
        for value in to_check[:]:
            if isinstance(value, str):
                flattened.append(value)
            else:
                try:
                    to_check.extend([*value])
                except TypeError:
                    if value is None:
                        return True

                    flattened.append(value)
            to_check.remove(value)

    return False

def input_checker(func):
    name = func.__name__
    def wrapper(*args, **kwargs):
        annot = get_type_hints(func)

        if name == '_calculate_distance':
            return_value = -1
        elif annot['return'] == int:
            return_value = 1
        elif annot['return'] == float:
            return_value = -1.0
        else:
            return_value = annot['return']()

        for arg, instance in zip(args, annot.values()):
            # if type doesn't match
            if not isinstance(arg, instance):
                return return_value

            # if int value is non-valid
            if instance == int and (isinstance(arg, bool) or arg < 1):
                return return_value

            # if sequence is empty
            if isinstance(arg, (tuple, list)) and not arg:
                if name in ('update', 'fill_n_grams', '_calculate_distance'):
                    return 0
                return return_value

            # if any is None
            if isinstance(arg, (tuple, list)):
                if has_none(arg):
                    return return_value

        return func(*args, **kwargs)
    return wrapper
