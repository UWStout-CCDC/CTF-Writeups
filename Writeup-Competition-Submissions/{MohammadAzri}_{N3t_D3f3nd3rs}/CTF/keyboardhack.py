import pyshark

# HID key mapping based on USB HID usage table
HID_KEY_MAP = {
    0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd',
    0x08: 'e', 0x09: 'f', 0x0A: 'g', 0x0B: 'h',
    0x0C: 'i', 0x0D: 'j', 0x0E: 'k', 0x0F: 'l',
    0x10: 'm', 0x11: 'n', 0x12: 'o', 0x13: 'p',
    0x14: 'q', 0x15: 'r', 0x16: 's', 0x17: 't',
    0x18: 'u', 0x19: 'v', 0x1A: 'w', 0x1B: 'x',
    0x1C: 'y', 0x1D: 'z',
    0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4',
    0x22: '5', 0x23: '6', 0x24: '7', 0x25: '8',
    0x26: '9', 0x27: '0',
    0x28: '\n',  # Enter
    0x2C: ' ',   # Space
    0x2D: '-',   # Minus
    0x2E: '=',   # Equal
    0x2F: '[',   # Left Bracket
    0x30: ']',   # Right Bracket
    0x31: '\\',  # Backslash
    0x33: ';',   # Semicolon
    0x34: "'",   # Apostrophe
    0x36: ',',   # Comma
    0x37: '.',   # Period
    0x38: '/',   # Slash
}

def parse_pcap(file_path):
    """
    Parses a pcap file to extract USB HID keycodes and map them to characters.
    """
    print(f"Opening {file_path}...")
    try:
        cap = pyshark.FileCapture(file_path, display_filter="usb")
        keystrokes = []

        for packet in cap:
            try:
                if hasattr(packet, 'usb'):
                    # Extract raw USB data from the packet
                    usb_data = packet.usb.data_hex
                    if usb_data:
                        bytes_data = bytes.fromhex(usb_data)
                        # The 3rd byte in HID data represents the keycode
                        keycode = bytes_data[2]
                        if keycode in HID_KEY_MAP:
                            keystrokes.append(HID_KEY_MAP[keycode])
            except Exception as e:
                print(f"Error processing packet: {e}")

        cap.close()
        return ''.join(keystrokes)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# File path to the .pcapng file
file_path = r"C:\Users\moham\Downloads\keyboard\keyboard.pcapng"

# Extract and print the flag
flag = parse_pcap(file_path)
if flag:
    print(f"Extracted Flag: {flag}")
else:
    print("No flag found or unable to parse.")
