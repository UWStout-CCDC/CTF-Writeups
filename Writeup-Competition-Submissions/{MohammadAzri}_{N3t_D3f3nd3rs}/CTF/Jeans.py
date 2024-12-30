# Encoding and decoding text using a DNA-like representation

# Mapping characters to DNA-like codons (3 nucleotide per character)
def encode_text_as_gene(text):
    """Encodes a text string into a DNA-like sequence."""
    char_to_codon = {
        'A': 'AAA', 'B': 'AAC', 'C': 'AAG', 'D': 'AAT',
        'E': 'ACA', 'F': 'ACC', 'G': 'ACG', 'H': 'ACT',
        'I': 'AGA', 'J': 'AGC', 'K': 'AGG', 'L': 'AGT',
        'M': 'ATA', 'N': 'ATC', 'O': 'ATG', 'P': 'ATT',
        'Q': 'CAA', 'R': 'CAC', 'S': 'TGA', 'T': 'CAT',
        'U': 'CCA', 'V': 'CCC', 'W': 'CCG', 'X': 'CCT',
        'Y': 'CGA', 'Z': 'CGC', ' ': 'CGG',
        '0': 'CGT', '1': 'CTA', '2': 'CTC', '3': 'CTG',
        '4': 'CTT', '5': 'GAA', '6': 'GAC', '7': 'GAG',
        '8': 'GAT', '9': 'GCA',
        '.': 'GCC', ',': 'GCG', '!': 'GCT', '?': 'GGA',
        '-': 'GGC', '_': 'GGG', ':': 'GGT', ';': 'GTA'
    }
    dna_sequence = ''.join(char_to_codon.get(char.upper(), 'NNN') for char in text)
    return dna_sequence

# Decoding function to retrieve text from DNA-like sequence
def decode_gene_to_text(dna_sequence):
    """Decodes a DNA-like sequence back into a text string."""
    codon_to_char = {v: k for k, v in {
        'A': 'AAA', 'B': 'AAC', 'C': 'AAG', 'D': 'AAT',
        'E': 'ACA', 'F': 'ACC', 'G': 'ACG', 'H': 'ACT',
        'I': 'AGA', 'J': 'AGC', 'K': 'AGG', 'L': 'AGT',
        'M': 'ATA', 'N': 'ATC', 'O': 'ATG', 'P': 'ATT',
        'Q': 'CAA', 'R': 'CAC', 'S': 'TGA', 'T': 'CAT',
        'U': 'CCA', 'V': 'CCC', 'W': 'CCG', 'X': 'CCT',
        'Y': 'CGA', 'Z': 'CGC', ' ': 'CGG',
        '0': 'CGT', '1': 'CTA', '2': 'CTC', '3': 'CTG',
        '4': 'CTT', '5': 'GAA', '6': 'GAC', '7': 'GAG',
        '8': 'GAT', '9': 'GCA',
        '.': 'GCC', ',': 'GCG', '!': 'GCT', '?': 'GGA',
        '-': 'GGC', '_': 'GGG', ':': 'GGT', ';': 'GTA'
    }.items()}
    text = ''.join(codon_to_char.get(dna_sequence[i:i+3], '?') for i in range(0, len(dna_sequence), 3))
    return text

# Example usage
if __name__ == "__main__":
    # Original text
    original_text = "STOUTCTF"
    print(f"Original text: {original_text}")

    # Encode the text as a DNA sequence
    encoded_dna = encode_text_as_gene(original_text)
    print(f"Encoded DNA sequence: {encoded_dna}")

    # Decode the DNA sequence back to text
    decoded_text = decode_gene_to_text(encoded_dna)
    print(f"Decoded text: {decoded_text}")

    # Verify if the original and decoded text match
    assert original_text.upper() == decoded_text, "The decoded text does not match the original!"
