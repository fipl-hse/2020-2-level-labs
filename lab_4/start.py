"""
Lab 4
"""

import lab_4
from lab_4.main import WordStorage,  tokenize_by_sentence, encode_text, NGramTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__=='__main__':
    text='I have a cat.\nHer name is Mila'
    tok_text = tokenize_by_sentence(text)
    storage = WordStorage()
    storage.update(tok_text)
    print(storage)
    encoded_text = encode_text(storage, tok_text)
    print(encoded_text)
    n_gram_trie = NGramTrie(2, encoded_text)
    print(n_gram_trie)
    gen=NGramTextGenerator(storage, n_gram_trie)
    context = (storage.get_id('a'),)
    print(context)
    RESULT = gen.generate_text(context, 2)
    print(RESULT)
    assert RESULT, 'Not working'
