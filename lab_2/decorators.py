"""
A module of decorators for checking in lab_2
"""

def input_checker(func):
    def wrapper(*args, **kwargs):
        if func.__annotations__['return'] == int:
            return_value = -1
        elif func.__annotations__['return'] == float:
            return_value = -1.0
        else:
            return_value =  func.__annotations__['return']()

        for arg, instance in zip(args, func.__annotations__.values()):
            if not isinstance(arg, instance):
                return return_value

            if instance == int and (isinstance(arg, bool) or arg < 0):
                return return_value
            if instance == float and (arg < 0 or arg > 1):
                return return_value

            if instance in [tuple, list] and not len(arg):
                return return_value
            if arg == (None, None):
                return return_value
        return func(*args, **kwargs)
    return wrapper
