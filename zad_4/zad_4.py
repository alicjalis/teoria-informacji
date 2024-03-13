import random

def build_markov_chain(text, order=1):
    markov_chain = {}
    for i in range(len(text) - order):
        ngram = text[i:i + order]
        next_char = text[i + order]
        if ngram not in markov_chain:
            markov_chain[ngram] = {}
        if next_char not in markov_chain[ngram]:
            markov_chain[ngram][next_char] = 0
        markov_chain[ngram][next_char] += 1
    for ngram, transitions in markov_chain.items():
        total = sum(transitions.values())
        for next_char in transitions:
            transitions[next_char] /= total
    return markov_chain

def generate_text(markov_chain, order, starting_sequence='a', length=1000):
    current_sequence = starting_sequence[-order:]
    generated_text = starting_sequence
    for _ in range(length):
        if current_sequence not in markov_chain:
            break
        next_char = random.choices(list(markov_chain[current_sequence].keys()),
                                    weights=list(markov_chain[current_sequence].values()))[0]
        generated_text += next_char
        current_sequence = generated_text[-order:]
    return generated_text

def read_random_sample(file_name, sample_size=1000):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    if len(text) >= sample_size:
        start_index = random.randint(0, len(text) - sample_size)
        text = text[start_index:start_index + sample_size]
    return text

# Wczytanie losowej probki tekstu
text_sample = read_random_sample('norm_wiki_sample.txt', sample_size=5000)

# Tworzenie modelu markova pierwszego rzedu
markov_chain_first_order = build_markov_chain(text_sample, order=1)
generated_text_first_order = generate_text(markov_chain_first_order, order=1)

# Tworzenie modelu markova trzeciego rzedu
markov_chain_third_order = build_markov_chain(text_sample, order=3)
generated_text_third_order = generate_text(markov_chain_third_order, starting_sequence='pro', order=3)

# Tworzenie modelu markova piatego rzedu
markov_chain_fifth_order = build_markov_chain(text_sample, order=5)
generated_text_fifth_order = generate_text(markov_chain_fifth_order, order=5, starting_sequence='probability')


print("Wygenerowany tekst markova pierwszego rzedu:")
print(generated_text_first_order)
print("\nWygenerowany tekst markova trzeciego rzedu:")
print(generated_text_third_order)
print("\nWygenerowany tekst markova piatego rzedu:")
print(generated_text_fifth_order)
