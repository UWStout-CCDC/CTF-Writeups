# Given binary string to decode
binary_string = "01110111101100111110011101100101001100001101000001001011101111110100111101110111101000111110000101010001100101101011100000101011010111011111111111010110100000011000011000011000001111011111101100111001001110110000100101101001111001101011000011010011011011110101011001000111100000110100011110111001011110000000000000110110111111111111110000101110101111111110000100011000011001000110110111111011101101011101111100110100111000100011101101110011111111100011010100111001101000111010111110000001111010011010011100011110111001011111111010100111010100110000100001111101011101000011100110101001110100101011111011010010111110010000000000011101011000010100000100000000111110101010010000011110111001001101010010111010001101111101100100101111111011110011000110001001111100111110000011010101101001111100000001011110010110011011011001000011011000010010010111111111000010011010000011111100100010100101000001000011110111010101000100010001001010101110010110101110110010001110101010001011110011000110011001010101101111010111001101011101101111011111001100110101000101101110001111011111101011101000001110010111100100111100011101111001001110010101110100010111110001110101111101011011111101101101000010001101101011111010100110101100100010111010001010100010001001010101101100000101"

# Provided key mapping
key = {
    "001": " ",
    "10010": "a",
    "11101": "e",
    "11111": "o",
    "01000": "r",
    "10101": "s",
    "10111": "t",
    "00011": "y",
    "010010": "t",
    "011010": ".",
    "010011": "T",
    "011100": "W",
    "010100": "c",
    "010101": "e",
    "010110": "g",
    "100110": "h",
    "100111": "i",
    "101000": "l",
    "011111": "m",
    "101001": "n",
    "010111": "ou",
    "000001": "p",
    "101100": "s",
    "100001": "t",
    "000010": "th",
    "100011": "u",
    "0110001": "I",
    "1011010": "a",
    "1100000": "i",
    "0110010": "'",
    "0110011": ".",
    "0110110": "C",
    "0110111": "I",
    "0111010": "as",
    "1110000": "b",
    "1110010": "d",
    "11100110": "e.",
    "11100111": "er",
    "11110000": "es",
    "11110001": "f",
    "11110010": "ha",
    "11110011": "hi",
    "11110100": "la",
    "11110101": "le",
    "11110110": "me",
    "11110111": "ne",
    "00010000": "v",
    "00010001": "x",
    "01100000": "{",
    "01100001": "}",
    "110010010": "-",
    "110010011": "2",
    "110011000": "3",
    "110011001": "7",
    "11001101": "6",
    "11001110": "8",
    "110011110": ":",
    "110011111": "?",
    "11010000": "A",
    "11010001": "CT",
    "11010011": "F",
    "11010100": "I'",
    "11010101": "J",
    "110101100": "K",
    "110101101": "L",
    "110101110": "M",
    "110101111": "O",
    "110111000": "Z",
    "110111001": "k",
}

# Function to decode binary string
def decode_binary(binary_string, key):
    result = ""
    while binary_string:
        for k, v in key.items():
            if binary_string.startswith(k):
                result += v
                binary_string = binary_string[len(k):]
                break
    return result

# Decode the message
decoded_message = decode_binary(binary_string, key)
print(decoded_message)