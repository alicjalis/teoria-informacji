import random
from collections import Counter

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def zeroth_order_model(text, rows, chars_per_row):
    generated_text = ''
    for _ in range(rows):
        row = ''.join(random.choices(text, k=chars_per_row))
        generated_text += row + '\n'
    return generated_text


def average_word_length(text):
    words = text.split()
    total_length = sum(len(word) for word in words)
    num_words = len(words)
    if num_words == 0:
        return 0
    return total_length / num_words


def calculate_character_frequency(text, sample_size=1200):
    # Wybierz losową próbkę tekstu
    sample_text = random.sample(text, min(len(text), sample_size))

    # Utwórz słownik częstości znaków
    char_frequency = Counter(sample_text)

    # Uporządkuj znaki według częstości występowania
    sorted_char_frequency = dict(sorted(char_frequency.items(), key=lambda item: item[1], reverse=True))

    return sorted_char_frequency
if __name__ == '__main__':
    text = read_file("norm_hamlet.txt")
    # Wygenerowanie przybliżenia zerowego rzędu
    generated_text = zeroth_order_model(text, 48, 25)
    avg_length = average_word_length(generated_text)

    print("Wygenerowany tekst:")
    print(generated_text)
    print("Średnia długość słowa:", avg_length)
    char_frequency = calculate_character_frequency(text, sample_size=1200)

    print("Częstość występowania poszczególnych znaków:")
    for char, count in char_frequency.items():
        print(f"{char}: {count}")
