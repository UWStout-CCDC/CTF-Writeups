upper_cipher = "WSCZMQHNUFBLIDEPJOYTRVXAKG"
lower_cipher = "amuphvibojrtfzwnqyeclxkdgs"
standard_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
standard_lower = "abcdefghijklmnopqrstuvwxyz"
numeric_key = "9085346217"

encoded_text = "YTERTCTQ{M1KyJDS6fXaU8PHzuKjSBHrgs5gt1Uhu}"

def decode_text(encoded, upper_map, lower_map, num_map):
    result = []
    for char in encoded:
        if char in upper_map:
            index = upper_map.index(char)
            result.append(standard_upper[index])
        elif char in lower_map:
            index = lower_map.index(char)
            result.append(standard_lower[index])
        elif char in num_map:
            index = num_map.index(char)
            result.append(str(index))
        else:
            result.append(char)
    return ''.join(result)

decoded_text = decode_text(encoded_text, upper_cipher, lower_cipher, numeric_key)
print("Decoded Text:", decoded_text)
