def decrypt_caesar(ciphertext, shift):
    result = []
    for char in ciphertext:
        if char.isalpha():  # Only shift alphabetic characters
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - shift) % 26 + base))
        else:
            result.append(char)  # Keep numbers and special characters as is
    return ''.join(result)

# Given ciphertext
ciphertext = "VWRXWFWI{Vr3J8NJks4Tn58PjDv3IPNc9VueGFwlu}"

# Known plaintext and corresponding ciphertext
plaintext_hint = "STOUTCTF"
ciphertext_hint = "VWRXWFWI"

# Step 1: Calculate the shift
shift = (ord(ciphertext_hint[0]) - ord(plaintext_hint[0])) % 26

# Step 2: Decrypt the entire ciphertext
decrypted = decrypt_caesar(ciphertext, shift)

# Print the result
print(f"Decrypted text: {decrypted}")
