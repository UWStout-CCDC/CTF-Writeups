def convert_to_decimal(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    decimal_values = []
    
    for line in lines:
        # Split the line by the colon character and remove any extra spaces/newlines
        hex_values = line.strip().split(':')
        
        # Convert each hex value to decimal and append it to the list
        decimal_values.extend([str(int(val, 16)) for val in hex_values if val])  # Convert hex to decimal
    
    # Output all decimal values as a space-separated string
    print(" ".join(decimal_values))

if __name__ == '__main__':
    file_path = 'keystroke.txt'  # Update with the correct path to your keystroke.txt
    convert_to_decimal(file_path)
