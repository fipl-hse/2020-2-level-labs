"""
A module for validation in lab_4
"""


def ensure_type(*annotations):
    for instance, cls in annotations:
        if not isinstance(instance, cls):
            raise ValueError


def ensure_not_empty(*args):
    for arg in args:
        if not arg:
            raise ValueError


def ensure_length(sequence, length):
    if len(sequence) != length:
        raise ValueError
