import random


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


if __name__ == '__main__':
    text = read_file("norm_hamlet.txt")
    # Wygenerowanie przybliżenia zerowego rzędu
    generated_text = zeroth_order_model(text, 48, 25)
    avg_length = average_word_length(generated_text)

    print("Wygenerowany tekst:")
    print(generated_text)
    print("Średnia długość słowa:", avg_length)
