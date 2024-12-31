color_codes = [
    "#53544F", "#555443", "#54467B", "#327147", "#6E4A50", 
    "#61336F", "#6A4966", "#4C5275", "#776D75", "#6E6967", 
    "#52686F", "#313976", "#336A63", "#61397D"
]

def hex_to_chars(hex_code):
    hex_code = hex_code.lstrip('#')
    chars = []
    for i in range(0, len(hex_code), 2):
        hex_pair = hex_code[i:i+2]
        chars.append(chr(int(hex_pair, 16)))
    return ''.join(chars)

decoded_values = [hex_to_chars(code) for code in color_codes]
print(decoded_values)
