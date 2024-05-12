import numpy as np

# The alphabet considered for the Huffman Coding
alphabet_list = list('abcdefghijklmnopqrstuvwxyz 1234567890')

# Huffman Tree Node class
class HuffmanNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right


def calc_frequency(text, alphabet):
    frequency_dict = dict.fromkeys(alphabet, 0)
    for char in text:
        frequency_dict[char] += 1
    return sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True) # Zwraca posortowaną listę krotek, gdzie każda krotka zawiera parę (znak, częstość)


def build_huffman_tree(node, left_flag=True, binary_string=''):
    if type(node) is str:
        return {node: binary_string}
    (left, right) = node.children()
    result = {}
    result.update(build_huffman_tree(left, True, binary_string + '0'))
    result.update(build_huffman_tree(right, False, binary_string + '1'))
    return result


def construct_huffman_code(text):
    node_list = calc_frequency(text, alphabet_list)

    while len(node_list) > 1:
        (char1, freq1) = node_list[-1]
        (char2, freq2) = node_list[-2]
        node_list = node_list[:-2]
        node = HuffmanNode(char1, char2)
        node_list.append((node, freq1 + freq2))
        node_list = sorted(node_list, key=lambda item: item[1], reverse=True)

    huffman_code = build_huffman_tree(node_list[0][0])

    return huffman_code


def huffman_encode(text, huffman_code):
    encoded_text = "".join([huffman_code[char] for char in text])
    return encoded_text


def huffman_decode(encoded_text, huffman_code):
    reversed_code = {v: k for k, v in huffman_code.items()}
    decoded_text, start = '', 0
    for i in range(len(encoded_text) + 1):
        if encoded_text[start:i] in reversed_code:
            decoded_text += reversed_code[encoded_text[start:i]]
            start = i
    return decoded_text


def save_encoded_data(code_file_name, huffman_code, encoded_file_name, encoded_text):
    with open(code_file_name, 'w') as code_file:
        for char, code in huffman_code.items():
            code_file.write(f'{char};{code};')

    with open(encoded_file_name, 'w') as encoded_file:
        encoded_file.write(encoded_text)


def load_encoded_data(code_file_name, encoded_file_name):
    code_data = open(code_file_name).read().split(";")
    loaded_code = {code_data[i]: code_data[i + 1] for i in range(0, len(code_data) - 1, 2)}

    with open(encoded_file_name, 'r') as encoded_file:
        encoded_text = encoded_file.read()

    return encoded_text, loaded_code


def calculate_compression_ratio(text, huffman_code):
    uncompressed_length = len(text) * 8
    compressed_length = sum([len(huffman_code[char]) for char in text])
    return uncompressed_length / compressed_length


def calculate_average_word_length(huffman_code, text_length, frequency_dict):
    return np.sum([(freq / text_length) * len(huffman_code[char]) for char, freq in frequency_dict])


def calculate_entropy(text, frequency_dict):
    len_text = len(text)
    return -np.sum([(freq / len_text) * np.log2(freq / len_text) for _, freq in frequency_dict])


text_sample = open("norm_wiki_sample.txt").read()
huffman_code = construct_huffman_code(text_sample)
encoded_text = huffman_encode(text_sample, huffman_code)
decoded_text = huffman_decode(encoded_text, huffman_code)

save_encoded_data("code.txt", huffman_code, "encoded_text.txt", encoded_text)

loaded_encoded_text, loaded_huffman_code = load_encoded_data("code.txt", "encoded_text.txt")
decoded_text_from_file = huffman_decode(loaded_encoded_text, loaded_huffman_code)

print("Compression Ratio: ", calculate_compression_ratio(text_sample, huffman_code))

frequency_dict = calc_frequency(text_sample, alphabet_list)
avg_word_length = calculate_average_word_length(huffman_code, len(text_sample), frequency_dict)

print("Average Word Length: ", avg_word_length)

text_entropy = calculate_entropy(text_sample, frequency_dict)

print("Text Entropy: ", text_entropy)
print("Effectiveness: ", text_entropy / avg_word_length)