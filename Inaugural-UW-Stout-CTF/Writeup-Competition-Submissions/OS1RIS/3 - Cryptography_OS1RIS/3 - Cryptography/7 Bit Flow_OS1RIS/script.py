from PIL import Image
import numpy as np

img = Image.open("bit_flow.jpg").convert("RGB")
width, height = img.size

pixels = np.array(img)

blue_channel = pixels[:, :, 0]

bit_plane_7 = (blue_channel >> 7) & 1

text_output = []
for row in bit_plane_7:
    bits = "".join(map(str, row))
    chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8)]
    text_output.append("".join(chars))

for line in text_output:
    print(line)
