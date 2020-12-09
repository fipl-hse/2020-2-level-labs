"""
Example of running programm in lab_4
"""


from lab_4.main import tokenize_by_sentence, WordStorage, encode_text
from lab_4.main import BackOffGenerator, save_model, load_model
from lab_4.ngrams.ngram_trie import NGramTrie


def main():
    text = ('I have a cat. His name is Bruno. '
            'I have a dog too. His name is Rex. '
            'Her name is Rex too.')

    corpus = tokenize_by_sentence(text)

    storage = WordStorage()
    storage.update(corpus)

    encoded = encode_text(storage, corpus)

    two = NGramTrie(2, encoded)
    trie = NGramTrie(3, encoded)

    context = (storage.get_id('name'),
               storage.get_id('is'),)

    generator = BackOffGenerator(storage, trie, two)

    expected = 'rex'
    actual = storage.get_word(generator._generate_next_word(context))

    print(f'TEXT:\n{text}')
    print(f'\nEXPECTED WORD AFTER name is IS {expected}')
    print(f'ACTUAL WORD AFTER name is IS {actual}')

    save_model(generator, 'model.txt')
    load_model('model.txt')

    RESULT = actual == expected
    assert RESULT, 'Language genenerator work incorrect'


if __name__ == "__main__":
    main()
