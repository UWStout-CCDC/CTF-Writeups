#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

# Key code mapping
KEY_CODES = {
    0x04: ['a', 'A'],
    0x05: ['b', 'B'],
    0x06: ['c', 'C'],
    0x07: ['d', 'D'],
    0x08: ['e', 'E'],
    0x09: ['f', 'F'],
    0x0A: ['g', 'G'],
    0x0B: ['h', 'H'],
    0x0C: ['i', 'I'],
    0x0D: ['j', 'J'],
    0x0E: ['k', 'K'],
    0x0F: ['l', 'L'],
    0x10: ['m', 'M'],
    0x11: ['n', 'N'],
    0x12: ['o', 'O'],
    0x13: ['p', 'P'],
    0x14: ['q', 'Q'],
    0x15: ['r', 'R'],
    0x16: ['s', 'S'],
    0x17: ['t', 'T'],
    0x18: ['u', 'U'],
    0x19: ['v', 'V'],
    0x1A: ['w', 'W'],
    0x1B: ['x', 'X'],
    0x1C: ['y', 'Y'],
    0x1D: ['z', 'Z'],
    0x1E: ['1', '!'],
    0x1F: ['2', '@'],
    0x20: ['3', '#'],
    0x21: ['4', '$'],
    0x22: ['5', '%'],
    0x23: ['6', '^'],
    0x24: ['7', '&'],
    0x25: ['8', '*'],
    0x26: ['9', '('],
    0x27: ['0', ')'],
    0x28: ['\n', '\n'],
    0x29: ['[ESC]', '[ESC]'],
    0x2a: ['[BACKSPACE]', '[BACKSPACE]'],
    0x2C: [' ', ' '],
    0x2D: ['-', '_'],
    0x2E: ['=', '+'],
    0x2F: ['[', '{'],
    0x30: [']', '}'],
    0x32: ['#', '~'],
    0x33: [';', ':'],
    0x34: ['\'', '"'],
    0x36: [',', '<'],
    0x37: ['.', '>'],
    0x38: ['/', '?'],
    0x39: ['[CAPSLOCK]', '[CAPSLOCK]'],
    0x2b: ['\t', '\t'],
    0x4f: [u'→', u'→'],
    0x50: [u'←', u'←'],
    0x51: [u'↓', u'↓'],
    0x52: [u'↑', u'↑'],
    # Additional key codes for numeric keypad
    0x53: ['Num Lock', 'Clear'],
    0x54: ['/', 'Keypad /'],
    0x55: ['*', 'Keypad *'],
    0x56: ['-', 'Keypad -'],
    0x57: ['+', 'Keypad +'],
    0x58: ['Enter', 'Keypad ENTER'],
    0x59: ['1', 'Keypad 1', 'End'],
    0x5a: ['2', 'Keypad 2', 'Down Arrow'],
    0x5b: ['3', 'Keypad 3', 'Page Down'],
    0x5c: ['4', 'Keypad 4', 'Left Arrow'],
    0x5d: ['5', 'Keypad 5'],
    0x5e: ['6', 'Keypad 6', 'Right Arrow'],
    0x5f: ['7', 'Keypad 7', 'Home'],
    0x60: ['8', 'Keypad 8', 'Up Arrow'],
    0x61: ['9', 'Keypad 9', 'Page Up'],
    0x62: ['0', 'Keypad 0', 'Insert'],
    0x63: ['.', 'Keypad .', 'Delete']
}

def read_use(file):
    with open(file, 'r') as f:
        datas = f.read().split('\n')
    datas = [d.strip() for d in datas if d]
    cursor_x, cursor_y = 0, 0
    lines, output = [""], ''
    skip_next = False

    for data in datas:
        shift = int(data.split(':')[0], 16)
        key = int(data.split(':')[2], 16)

        if skip_next:
            skip_next = False
            continue
        
        if key == 0 or int(data.split(':')[3], 16) > 0:
            continue
        
        shift = 1 if shift != 0 else 0
        
        if key in KEY_CODES:
            char = KEY_CODES[key][shift]
            
            # Handle special keys
            if char == 'Num Lock':
                continue  # Optional: Log 'Num Lock' status
            elif char == 'Clear':
                output = ''
            elif char == 'Keypad ENTER':
                lines.append("")
                cursor_y += 1
                cursor_x = 0
                output = ''
            elif char in ['Up Arrow', 'Down Arrow', 'Left Arrow', 'Right Arrow']:
                # Arrow key navigation
                if char == 'Up Arrow':
                    cursor_y = max(0, cursor_y - 1)
                elif char == 'Down Arrow':
                    cursor_y += 1
                elif char == 'Left Arrow':
                    cursor_x = max(0, cursor_x - 1)
                elif char == 'Right Arrow':
                    cursor_x += 1
            elif char == '[BACKSPACE]':
                output = output[:-1]
            elif char == '\n':
                lines.append("")
                cursor_y += 1
                cursor_x = 0
                output = ''
            else:
                output += char
                cursor_x += 1

    if lines == [""]:
        lines[0] = output
    if output != '' and output not in lines:
        lines[cursor_y] += output
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing file to read...')
        exit(-1)
    sys.stdout.write(read_use(sys.argv[1]))
