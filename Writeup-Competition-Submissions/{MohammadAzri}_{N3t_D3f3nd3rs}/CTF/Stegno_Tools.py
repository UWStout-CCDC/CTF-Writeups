from PIL import Image

def text_to_bin(text):
    """Convert text to binary, handle encoding issues"""
    binary = ''.join(format(ord(c), '08b') for c in text)
    return binary

def bin_to_text(binary):
    """Convert binary to text, handle decoding correctly"""
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text += chr(int(byte, 2))
    return text

def embed_message(image_path, message, output_path):
    """Embed the message into the image"""
    binary_message = text_to_bin(message) + '1111111111111110'  # Add delimiter at the end
    print(f"Binary message to embed: {binary_message[:100]}...")  # Print first 100 bits for debugging

    img = Image.open(image_path)
    img = img.convert('RGB')  # Ensure it's in RGB mode
    pixels = img.load()
    width, height = img.size

    message_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if message_index < len(binary_message):
                r = (r & ~1) | int(binary_message[message_index])  # Modify LSB of red channel
                message_index += 1
            if message_index < len(binary_message):
                g = (g & ~1) | int(binary_message[message_index])  # Modify LSB of green channel
                message_index += 1
            if message_index < len(binary_message):
                b = (b & ~1) | int(binary_message[message_index])  # Modify LSB of blue channel
                message_index += 1
            pixels[x, y] = (r, g, b)  # Set modified pixel

    img.save(output_path)
    print(f"Message successfully embedded and saved to {output_path}")

def extract_message(image_path):
    """Extract the hidden message from the image"""
    img = Image.open(image_path)
    img = img.convert('RGB')  # Ensure it's in RGB mode
    pixels = img.load()
    width, height = img.size

    binary_message = ''
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)  # Extract LSB from red channel
            binary_message += str(g & 1)  # Extract LSB from green channel
            binary_message += str(b & 1)  # Extract LSB from blue channel

    # Find the delimiter (the end of the message)
    delimiter = '1111111111111110'
    binary_message = binary_message[:binary_message.find(delimiter)]

    print(f"Extracted binary message (first 100 bits): {binary_message[:100]}...")  # Print first 100 bits for debugging

    # Convert binary message to text
    return bin_to_text(binary_message)

# Example usage
if __name__ == "__main__":
    message = "Hello, this is a secret message!"
    input_image = "cover_image.jpg"  # Use PNG for better lossless storage
    output_image = "output_image.jpg"  # Path to save the image with hidden message
    embed_message(input_image, message, output_image)

    extracted_message = extract_message(output_image)
    print(f"Extracted message: {extracted_message}")
