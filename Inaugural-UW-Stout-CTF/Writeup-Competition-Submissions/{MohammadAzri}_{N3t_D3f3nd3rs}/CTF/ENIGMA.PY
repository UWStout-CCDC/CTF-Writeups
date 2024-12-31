from python_enigma import Enigma

# Enigma machine settings
rotors = [("VI", "A"), ("I", "Q"), ("III", "L")]
reflector = "Reflector B"
stecker = "BQ CR DI EJ KW MT OS PX UZ GH"

# Set up the Enigma machine
enigma = Enigma(
    catalog="default",
    stecker=stecker,
    rotors=rotors,
    reflector=reflector
)

# The ciphertext you provided
ciphertext = "xased xlzdn snwia wfgnn rekze lytqc pgujf sfcis fiwfn sqxln qoemb mvlkn"

# Decrypt the ciphertext
decrypted_message = enigma.parse(ciphertext.replace(" ", ""))

# Display the decrypted message
print(f"Decrypted Message: {decrypted_message}")
