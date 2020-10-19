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
            # if type doesn't match
            if not isinstance(arg, instance):
                return return_value

            # if int or float value is non-valid
            if instance == int and (isinstance(arg, bool) or arg < 0):
                return return_value
            if instance == float and (arg < 0 or arg > 1):
                return return_value

            # if sequence is empty
            if isinstance(arg, (tuple, list)) and not arg:
                return func.__annotations__['return']()

            # if any is None
            if isinstance(arg, (tuple, list)):
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
                                flattened.append(value)
                        to_check.remove(value)

                if any(item is None for item in flattened):
                    return return_value

        return func(*args, **kwargs)
    return wrapper
