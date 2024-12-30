def convert_keystrokes(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        # Split the line by the colon character and remove the newline
        hex_values = line.strip().split(':')
        
        # Convert each hex value to decimal and hex
        decimal_values = [int(val, 16) for val in hex_values]
        hex_values = [f'0x{val:02x}' for val in decimal_values]  # Format hex values
        
        # Print the decimal and hex values
        print("Hexadecimal:", ':'.join(hex_values))
        print("Decimal:", decimal_values)
        print()

if __name__ == '__main__':
    file_path = 'keystroke.txt'  # Update with the correct path to your keystroke.txt
    convert_keystrokes(file_path)
