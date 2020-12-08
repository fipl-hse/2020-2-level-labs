"""
A module for validation in lab_4
"""


def ensure_type(annotations):
    for instance, arg in annotations.items():
        if not isinstance(arg, instance):
            raise ValueError


def is_empty(*args):
    for arg in args:
        if not arg:
            raise ValueError


def is_in(item, sequence):
    if item not in sequence:
        raise KeyError


def is_correct_length(sequence, length):
    if len(sequence) != length:
        raise ValueError
