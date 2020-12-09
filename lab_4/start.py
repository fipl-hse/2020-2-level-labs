"""
Example of running programm in lab_4
"""

from lab_4.main import tokenize_by_sentence, WordStorage, encode_text
from lab_4.main import BackOffGenerator, save_model, load_model
from ngrams.ngram_trie import NGramTrie


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

    expected_word = storage.get_id('rex')
    context = (storage.get_id('name'),
               storage.get_id('is'),)

    generator = BackOffGenerator(storage, trie, two)

    actual = generator._generate_next_word(context)

    print(f'TEXT:\n{text}')
    print('\nEXPECTED WORD AFTER name is IS rex')
    print(f'ACTUAL WORD AFTER name is IS {storage.get_word(actual)}')
    
    save_model(generator, 'model.txt')
    generator = load_model('model.txt')


if __name__ == "__main__":
    main()

