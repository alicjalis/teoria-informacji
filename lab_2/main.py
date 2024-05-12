import random

def build_markov_chain(text, order=1):
    words = text.split()
    markov_chain = {}
    for i in range(len(words) - order):
        current_words = tuple(words[i:i+order])  # Tworzenie krotki z określoną liczbą słów
        next_word = words[i + order]
        if current_words in markov_chain:
            markov_chain[current_words].append(next_word)
        else:
            markov_chain[current_words] = [next_word]
    return markov_chain

def generate_text(markov_chain, order = 1, length=1000, starting_sequence=None):
    if starting_sequence == None:
        current_words = random.choice(list(markov_chain.keys()))
    else:
        starting_sequence = starting_sequence.split()
        current_words = tuple(starting_sequence)
    generated_text = ' '.join(current_words)
    word_count = order
    for _ in range(length):
        if current_words in markov_chain:
            next_word = random.choice(markov_chain[current_words])
            generated_text += ' ' + next_word
            current_words = current_words[1:] + (next_word,)  # Aktualizacja krotki słów
            word_count += 1
            if word_count % 10 == 0:
                generated_text += '\n'
        else:
            break
    return generated_text

def read_random_sample(file_name, sample_size=1000):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    if len(text) >= sample_size:
        start_index = random.randint(0, len(text) - sample_size)
        text = text[start_index:start_index + sample_size]
    return text

sample_text = read_random_sample("norm_wiki_sample.txt", 1200)
markov_chain_first_order = build_markov_chain(sample_text)
text_first_order = generate_text(markov_chain_first_order)

markov_chain_second_order = build_markov_chain(sample_text, 2)
text_second_order = generate_text(markov_chain_second_order, 2)
markov_chain_starting_sequence = build_markov_chain(sample_text, 2)
text_with_sequence = generate_text(markov_chain_starting_sequence, 2, 1000, "probability that")
print(markov_chain_first_order)
print(markov_chain_second_order)
print("First order \n")
print(text_first_order + "\n")
print("Second order \n")
print(text_second_order + "\n")
print(text_with_sequence)

