"""
A module for validation in lab_4
"""


def ensure_type(*annotations):
    for instance, cls in annotations:
        if not isinstance(instance, cls):
            raise ValueError(f"Input value {instance} has doesn't match {cls}")


def ensure_not_empty(*args):
    for arg in args:
        if not arg:
            raise ValueError('Input value is empty')


def ensure_correct_int(num, null_is_available=False):
    if null_is_available:
        if num < 0:
            raise ValueError(f'Input value {num} is lower than 0')
    elif num <= 0:
        raise ValueError(f'Input value {num} is lower or equal 0')


def ensure_length(sequence, length):
    if len(sequence) != length:
        raise ValueError(f'Input value {sequence} is not correct length {length}')
