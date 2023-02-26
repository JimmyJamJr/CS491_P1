def load_data(fname):
    data = []
    fin = open(fname,'r')
    for line in fin:
        line = line.strip()
        data.append(line)
    fin.close()
    return data


from collections import defaultdict
from itertools import product


def train_ngram(train_data, n):
    counts = defaultdict(lambda: 0)
    words = set()

    for sentence in train_data:
        for word in sentence.split():
            counts[word] += 1
            words.add(word)

    ngrams = list(product(words, repeat=n))

    probabilities = {}
    for ngram in ngrams:
        ngram_count = 0
        previous_count = 0
        for sentence in train_data:
            ngram_count += sentence.count(" ".join(ngram))
            if len(ngram) == 1:
                previous_count += len(sentence.split())
            else:
                previous_count += sentence.count(" ".join(ngram[:-1]))
        probabilities[ngram] = ngram_count / previous_count

    return probabilities


def generate_language(ngram_model, max_words):
    generated = "<s>"


def calculate_probability(utterance, ngram_model):
    pass


train_data = load_data('data1.txt')
print(train_data)
model = train_ngram(train_data, 2)
print(model)