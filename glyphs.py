# Glyphs for the letters G-Z, and punctuation.
# Glyphs for A-Z and 0-9 are supplied by the chip 8 rom.
GLYPH_TABLE = [
    [ # Space (0x20)
        0b0000,
        0b0000,
        0b0000,
        0b0000,
        0b0000
    ], [ # G
        0b0111,
        0b1000,
        0b1001,
        0b1001,
        0b0111
    ], [ # H
        0b1001,
        0b1001,
        0b1111,
        0b1001,
        0b1001
    ], [ # I
        0b1110,
        0b0100,
        0b0100,
        0b0100,
        0b1110,
    ], [ # J
        0b1111,
        0b0010,
        0b0010,
        0b1010,
        0b0100
    ], [ # K
        0b1001,
        0b1010,
        0b1100,
        0b1010,
        0b1001,
    ], [ # L
        0b1000,
        0b1000,
        0b1000,
        0b1000,
        0b1111,
    ], [ # M
        0b1001,
        0b1111,
        0b1001,
        0b1001,
        0b1001,
    ], [ # N
        0b1001,
        0b1101,
        0b1011,
        0b1001,
        0b1001,
    ], [ # O
        0b1111,
        0b1001,
        0b1001,
        0b1001,
        0b1111,
    ], [ # P
        0b1111,
        0b1001,
        0b1111,
        0b1000,
        0b1000,
    ], [ # Q
        0b1111,
        0b1001,
        0b1001,
        0b1011,
        0b1111,
    ], [ # R
        0b1111,
        0b1001,
        0b1111,
        0b1010,
        0b1001,
    ], [ # S
        0b1111,
        0b1000,
        0b1111,
        0b0001,
        0b1111,
    ], [ # T
        0b1110,
        0b0100,
        0b0100,
        0b0100,
        0b0100,
    ], [ # U
        0b1001,
        0b1001,
        0b1001,
        0b1001,
        0b1111,
    ], [ # V
        0b1001,
        0b1001,
        0b1001,
        0b1001,
        0b0110,
    ], [ # W
        0b1001,
        0b1001,
        0b1111,
        0b1111,
        0b0110,
    ], [ # X
        0b1001,
        0b1001,
        0b0110,
        0b1001,
        0b1001,
    ], [ # Y
        0b1001,
        0b1001,
        0b1111,
        0b0001,
        0b1111,
    ], [ # Z
        0b1111,
        0b0011,
        0b0110,
        0b0100,
        0b1111,
    ], [ # ! (0x21)
        0b0100,
        0b0100,
        0b0100,
        0b0000,
        0b0100
    ], [ # " (0x22)
        0b0101,
        0b0101,
        0b0000,
        0b0000,
        0b0000
    ], [ # # (0x23)
        0b1001,
        0b1111,
        0b1001,
        0b1111,
        0b1001
    ], [ # $ (0x24)
        0b1111,
        0b1010,
        0b1111,
        0b0101,
        0b1111,
    ], [ # % (0x25)
        0b1001,
        0b0010,
        0b0110,
        0b0100,
        0b1001
    ], [ # & (0x26)
        0b0110,
        0b1001,
        0b1110,
        0b1001,
        0b0110
    ], [ # ' (0x27)
        0b0010,
        0b0010,
        0b0000,
        0b0000,
        0b0000
    ], [ # ( (0x28)
        0b0001,
        0b0010,
        0b0010,
        0b0010,
        0b0001
    ], [ # ) (0x29)
        0b1000,
        0b0100,
        0b0100,
        0b0100,
        0b1000
    ], [ # * (not that great looking)
        0b0000,
        0b0110,
        0b1111,
        0b0110,
        0b0000
    ], 
]

def get_characters():
    """ Stitches the letters into an array that will be used in the final program
        this facilitates editing the characters, as they are store in binary in
        individual cells inside the python script
    """
    result = []
    for index, letter in enumerate(GLYPH_TABLE):
        if index % 2 == 0:
            letter_row_a = letter[0] << 12 | letter[1] << 4
            letter_row_b = letter[2] << 12 | letter[3] << 4
            letter_row_c = letter[4] << 12
            result.extend([letter_row_a, letter_row_b, letter_row_c])
        else:
            letter_row_a = letter[0] << 4
            letter_row_b = letter[1] << 12 | letter[2] << 4
            letter_row_c = letter[3] << 12 | letter[4] << 4
            result[-1] |= letter_row_a
            result.extend([letter_row_b, letter_row_c])
    return result