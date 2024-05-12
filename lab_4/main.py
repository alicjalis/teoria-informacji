import math

def calculate_frequencies(text):
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies

def create(chars, length):
    codes = {}
    for i, char in enumerate(chars):
        code = bin(i)[2:]
        for j in range(length - len(code)):
            code = '0' + code
        codes[code] = char

    # Uzupełnij brakujące kody, jeśli lista znaków jest mniejsza niż 2^min_bits
    if len(codes) < 2 ** length:
        for i in range(len(codes), 2 ** length):
            code = bin(i)[2:]
            for j in range(length - len(code)):
                code = '0' + code
            codes[code] = ''  # Ustaw pusty znak dla brakującego kodu

    return codes

def encode(text, codes):
    encoded = ''
    for char in text:
        for key, value in codes.items():
            if value == char:
                encoded += key
                break
    return encoded

def decode(encoded, codes):
    length = len(list(codes.keys())[0])
    chunks = [encoded[i:i + length] for i in range(0, len(encoded), length)]
    decoded = ""
    for letter in chunks:
        if letter in codes:
            decoded += codes[letter]
    return decoded

def save(codes, encoded_text, filename):
    with open(filename, 'w') as file:
        # Zapisujemy kody w formacie "kod znak", oddzielając każdą parę nową linią
        for code, char in codes.items():
            file.write(f"{code} {char}\n")
        file.write("\n")  # Dodajemy pustą linię jako separator
        # Zapisujemy zakodowany tekst
        file.write(encoded_text)

def load(filename):
    with open(filename, 'r') as file:
        # Wczytujemy kody ze standardowego formatu "kod znak"
        codes = {}
        for line in file:
            line = line.strip()
            if not line:  # Ignorujemy puste linie
                break
            code, char = line.split()  # Rozdzielamy kod i znak
            codes[code] = char
        # Wczytujemy zakodowany tekst
        encoded_text = file.read()
    return codes, encoded_text


file_path = "test.txt"  # Ścieżka do pliku tekstowego
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

unique_characters = set(text)  # zbiór unikalnych znaków
amount = len(unique_characters)
print("Liczba unikalnych znaków:", amount)

min_bits = math.ceil(math.log2(amount))
print("Minimalna liczba bitów: ", min_bits)

frequencies = calculate_frequencies(text)
codes = create(unique_characters, min_bits)
encoded = encode(text,codes)
decoded = decode(encoded,codes)
print("Encoded: ", encoded)
print("Decoded: ", decoded)
