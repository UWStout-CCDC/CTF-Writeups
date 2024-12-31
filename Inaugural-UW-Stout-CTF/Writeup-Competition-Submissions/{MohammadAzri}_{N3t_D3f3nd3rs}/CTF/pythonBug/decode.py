import base64
from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
import binascii

# Function to decode Base64 encoded strings
def b64decode(string):
    return base64.b64decode(string)

# Function to decode hex string into raw bytes
def hex_to_bytes(hex_string):
    return binascii.unhexlify(hex_string)

# Function to decrypt the data using Blowfish
def decode(ciphertext, key, iv):
    # Create a new Blowfish cipher object using the key and IV
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    # Decrypt the ciphertext
    plaintext = cipher.decrypt(ciphertext)
    # Unpad the plaintext if padding was used (usually Blowfish uses 8-byte padding)
    plaintext = plaintext.rstrip(b'\0')
    return plaintext

# Parse the necessary files and assign the data to global variables
def parse():
    with open('pythonBug/k.txt', 'r') as f:
        k = f.read().strip()
    
    key = b64decode(k)  # Decode the key from Base64

    with open('pythonBug/i.txt', 'r') as g:
        iv = g.read().strip()  # IV (Initialization Vector) might be in i.txt

    iv = b64decode(iv)  # Decode the IV from Base64

    # The provided hex string from fish.fossilem
    hex_data = "48d9b1523c306da201378d263de222debd2bab737da4a915695d6f439940362f14792276384117d1c0265a1a2db221c3f314da6f8cee925a75937582022b34633120698fe3e03411be1c88b85daddbea36a933e7b0be58320efc1590bbfd349660b90c217cdc4cb97a25d986da6afbcf0d0a78199e57e60204666098e8f3b893aaa6519e9192e0f2fd8ff719ee859bacbdc6d085fd621fefe486832554d8e2494f80c824a3d0b4f575e761e75dbc5c20f178022dd9b7568d9b90830872edd77ccde36aa6b72fdd56b7cbffd9e87dab867aaa01074e6b74bf7cfd92c275d8a4dd863b22823e756342c07af716cdb86cfa40855acf27214e0ad0fd68e58e7d081636bcc5597749a985fe72484744afdd6b3efb27c8317c39963295102e6d60d3b89cee458f047aaeae1cf811bbf4b975c906495ff01a9027e78f1d0efa540dc4b836c613178f85307fb08afc32de9415cd0c0df0ed2129a324c44abbb26551f1434f1fa25784d0e8aa88bcfce760a416765b63872b3dec40605a6d67c7cc706f75d40a9631305b0e39"
    
    ciphertext = hex_to_bytes(hex_data)  # Convert the hex string to raw bytes

    return key, iv, ciphertext

# Main function to tie everything together
def main():
    key, iv, ciphertext = parse()
    decrypted_data = decode(ciphertext, key, iv)
    print("Decrypted data: ", decrypted_data.decode('utf-8', errors='ignore'))

# Runs the main function
if __name__ == "__main__":
    main()
