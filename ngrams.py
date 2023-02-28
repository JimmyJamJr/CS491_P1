import random
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
        if ngram[-1] == "<s>":
            continue

        ngram_count = 0
        previous_count = 0
        for sentence in train_data:
            ngram_count += sentence.count(" ".join(ngram[(ngram.count("<s>") - ("<s>" in ngram)):]))
            if len(ngram) == 1:
                previous_count += len(sentence.split())
            else:
                previous_count += sentence.count(" ".join(ngram[(ngram.count("<s>") - ("<s>" in ngram)):-1]))
        probabilities[ngram] = ngram_count / previous_count if previous_count != 0 else 0

    return probabilities


def generate_language(ngram_model, max_words):
    n = len(list(ngram_model.keys())[0])
    current_index = 0
    generated = []
    window = []

    while len(generated) < max_words - 2:
        if current_index > n - 2:
            window = generated[current_index + 1 - n:current_index]
        else:
            window = ["<s>"] * (n - current_index - 1) + generated[0:current_index]

        acceptable = [(k, v) for k, v in ngram_model.items() if list(k[0:n-1]) == window and k[-1] != "<s>"]
        acceptable = sorted(acceptable, key=lambda x: x[1], reverse=True)
        choice = random.choices(acceptable, weights=list(x[1] for x in acceptable) if not all(x[1] == 0 for x in acceptable) else None, k=1)[0]
        generated.append(choice[0][-1])

        if choice[0][-1] == "</s>":
            break

        current_index += 1

    generated.insert(0, "<s>")
    if generated[-1] != "</s>":
        generated.append("</s>")
    return " ".join(generated)


def calculate_probability(utterance, ngram_model):
    n = len(list(ngram_model.keys())[0])
    tokens = utterance.split(" ")
    current_index = 1
    probability = 1.0

    while current_index < len(tokens):
        if current_index < n - 1:
            ngram = ["<s>"] * (n - 1 - current_index) + tokens[:current_index + 1]
        else:
            ngram = tokens[current_index - n + 1:current_index + 1]

        probability *= ngram_model[tuple(ngram)]
        current_index += 1
    return probability

