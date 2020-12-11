"""
Text Generator implementation starter
"""

import lab_4.main
from lab_4.ngrams.ngram_trie import NGramTrie


if __name__ == '__main__':

    TEXT = """I have a cat. His name is Max. I have a dog. His name is Jake.
              I do not have a dog or a cat. I have a parrot. Her name is Max too.
              And I have a parrot too. But his name is Leo."""

    corpus = lab_4.main.tokenize_by_sentence(TEXT)

    storage = lab_4.main.WordStorage()
    storage.update(corpus)

    encoded_text = lab_4.main.encode_text(storage, corpus)

    ngram_trie_2 = NGramTrie(2, encoded_text)
    ngram_trie_3 = NGramTrie(3, encoded_text)
    ngram_trie_4 = NGramTrie(4, encoded_text)

    expected_word = storage.get_id('a')
    CONTEXT = (storage.get_id('i'),
               storage.get_id('have'),)

    generator_ngram_trie = lab_4.main.NGramTextGenerator(storage, ngram_trie_3)
    generator_likelihood = lab_4.main.LikelihoodBasedTextGenerator(storage, ngram_trie_3)
    generator_backoff = lab_4.main.BackOffGenerator(storage, ngram_trie_3, ngram_trie_2, ngram_trie_4)

    generated_text_1 = lab_4.main.decode_text(storage, generator_ngram_trie.generate_text(CONTEXT, 3))
    generated_text_2 = lab_4.main.decode_text(storage, generator_likelihood.generate_text(CONTEXT, 3))
    generated_text_3 = lab_4.main.decode_text(storage, generator_backoff.generate_text(CONTEXT, 3))

    print('Generated text, class NGramTextGenerator:', generated_text_1)
    print('\nGenerated text, class LikelihoodBasedTextGenerator:', generated_text_2)
    print('\nGenerated text, class BackOffGenerator:', generated_text_3)

    generated_text = list(generated_text_3)

    RESULT = '. '.join(generated_text) + '.'
    print('\nGenerated text:', RESULT)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 'I have a dog. His name is max. I have a dog.', 'Generator is not working.'
