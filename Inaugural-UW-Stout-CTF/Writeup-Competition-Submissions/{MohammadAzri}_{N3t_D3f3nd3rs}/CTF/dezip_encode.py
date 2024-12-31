import base64
import gzip
from io import BytesIO

def decode_and_decompress(encoded_data):
    # Decode the base64 encoded data
    decoded_data = base64.b64decode(encoded_data)
    
    # Decompress the data using gzip
    with gzip.GzipFile(fileobj=BytesIO(decoded_data), mode='rb') as f:
        decompressed_data = f.read()
    
    return decompressed_data.decode('utf-8')

# The Base64-encoded string
encoded_data = "H4sIAA7WWGcA/4VSQQ7DMAg7J1L+QD+0X6Bll1Xa8v1DIEwamKhNqkq42IDp4xz99X7SOOnLTJ0/fLRK6xS5rZZfqBEViTwgkAfke864odyLSoIH5ESKiQDgKYpEDXuQctWH1pU3+oFVQsaubJ4lGoSz5DWghl5sHYZLja0sXAMahMOhQdlCdAxFkx8bxyLFOJcauDn7H6LJ/2lb1TsBTpgJ6fcCAAA="

# Decode and decompress
decoded_message = decode_and_decompress(encoded_data)

# Save the decoded and decompressed message to a file
with open('decoded_output.txt', 'w') as output_file:
    output_file.write("Decoded and Decompressed Message:\n")
    output_file.write(decoded_message)

print("Decoded and decompressed message saved to 'decoded_output.txt'")
