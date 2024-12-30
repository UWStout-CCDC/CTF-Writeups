import base64

# Convert number to bytes and then to base64
number = 1319448579496083489
byte_data = number.to_bytes((number.bit_length() + 7) // 8, 'big')
base64_encoded = base64.b64encode(byte_data)
print(base64_encoded)
