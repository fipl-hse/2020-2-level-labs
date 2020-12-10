from lab_4 import main

text = main.tokenize_by_sentence('I have a dog. It is name is Bruno.')
storage = main.WordStorage()
text_encoded = main.encode_text(storage, text)
trie = main.NGramTrie(2, text_encoded)
text_generator = main.NGramTextGenerator(storage, trie)
new_text = text_generator.generate_text((1,), 1)

end = storage.get_id('<END>')
actual = new_text.count(end)
RESULT = 1

assert RESULT == actual, 'not generating'
