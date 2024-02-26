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


def generate_first_order_model(text, rows, chars_per_row, char_frequency):
    # Tworzymy kumulatywną dystrybuantę prawdopodobieństwa
    cumulative_frequency = {}
    cumulative_sum = 0
    for char, count in char_frequency.items():
        cumulative_sum += count
        cumulative_frequency[char] = cumulative_sum

    # Generujemy tekst w odpowiednich wierszach i kolumnach
    generated_text = ''
    for _ in range(rows):
        row = ''
        for _ in range(chars_per_row):
            random_index = random.randint(0, cumulative_sum - 1)
            for char, cumulative_count in cumulative_frequency.items():
                if random_index < cumulative_count:
                    row += char
                    break
        generated_text += row + '\n'

    return generated_text


def calculate_bigram_probabilities(text, sample_size=1200):
    # Wybierz losową próbkę tekstu
    sample_text = random.sample(text, min(len(text), sample_size))

    # Oblicz wystąpienia poszczególnych znaków
    char_counts = Counter(sample_text)

    # Oblicz wystąpienia bigramów
    bigram_counts = Counter(zip(sample_text, sample_text[1:]))

    # Oblicz prawdopodobieństwa warunkowe
    bigram_probabilities = {}
    for bigram, count in bigram_counts.items():
        char1, char2 = bigram
        probability = count / char_counts[char1]
        bigram_probabilities[bigram] = probability

    return bigram_probabilities


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

    generated_text_first_order = generate_first_order_model(text, 48, 25, char_frequency)
    avg_length_first_order = average_word_length(generated_text_first_order)

    print("Wygenerowany tekst (przybliżenie pierwszego rzędu):")
    print(generated_text_first_order)
    print("Średnia długość słowa (przybliżenie pierwszego rzędu):", avg_length_first_order)

    # Oblicz prawdopodobieństwa bigramów
    bigram_probabilities = calculate_bigram_probabilities(text)

    # Wyświetl obliczone prawdopodobieństwa
    print("Prawdopodobieństwa wystąpienia znaków po każdym z drugiego najczęściej występującego znaku:")
    sorted_bigram_probabilities = dict(sorted(bigram_probabilities.items(), key=lambda item: item[1], reverse=True))
    for bigram, probability in sorted_bigram_probabilities.items():
        char1, char2 = bigram
        print(f"P({char2}|{char1}) = {probability}")
