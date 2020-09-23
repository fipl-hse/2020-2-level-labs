"""
Concordance implementation starter
"""

from main import read_from_file
from pathlib import Path
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    data = read_from_file(next(Path(os.getcwd()).rglob('data.txt')))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py

    RESULT = None
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT == [(), ()], 'Concordance not working'
