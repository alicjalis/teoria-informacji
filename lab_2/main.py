import random

def build_markov_chain(text):
    words = text.split()
    markov_chain = {}
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        if current_word in markov_chain:
            markov_chain[current_word].append(next_word)
        else:
            markov_chain[current_word] = [next_word]
    return markov_chain


def generate_text(markov_chain, length=1000):
    current_word = random.choice(list(markov_chain.keys()))
    generated_text = current_word
    word_count = 1
    for _ in range(length):
        if current_word in markov_chain:
            next_word = random.choice(markov_chain[current_word])
            generated_text += ' ' + next_word
            current_word = next_word
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


sample_text = read_random_sample("norm_hamlet.txt", 1200)
markov_chain = build_markov_chain(sample_text)
generated_text = generate_text(markov_chain)

print(generated_text)