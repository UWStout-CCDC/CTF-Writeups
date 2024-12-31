def atbash_cipher(text):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    reversed_alphabet = alphabet[::-1]
    result = ""
    for char in text:
        if char.isalpha():  # Apply substitution only to letters
            if char.isupper():
                result += reversed_alphabet[alphabet.index(char)]
            else:
                result += reversed_alphabet[alphabet.index(char.upper())].lower()
        else:
            result += char  # Non-alphabetic characters remain unchanged
    return result

encoded_flag = "YBCPTPZN{EaT8CK2zVexEqjdCmP6URd14xW6kNg7B}"
decoded_flag = atbash_cipher(encoded_flag)
print(decoded_flag)
