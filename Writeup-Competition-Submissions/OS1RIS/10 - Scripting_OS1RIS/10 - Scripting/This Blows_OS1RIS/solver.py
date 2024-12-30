from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import unpad
import binascii

key = b'\xA0\xFF\xDE\x12' #FROM BASE64 TO HEX TO BYTES
iv = b'\x30\xBC\x4F\xAA\x69\xCF\xF1\x00' #FROM BASE64 TO HEX TO BYTES
encoded_hex = "431872ecdb43436aea73f583da85a1598e2cad9d954509d73de618ec6f3eb9f651682eaeb787e288d218db859a4adaa5" #FROM BASE64

encoded = binascii.unhexlify(encoded_hex)

cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)

cdec = cipher.decrypt(encoded)

try:
    flag = unpad(cdec, Blowfish.block_size).decode('utf-8')
except ValueError:
    flag = cdec

print(flag)
