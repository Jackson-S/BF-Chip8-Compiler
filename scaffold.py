import glyphs
import functions

class Scaffold:
    def __init__(self):
        # Halve the memory size as it's specified in 8 bits, but each instruction
        # consists of 16 bits.
        self.program_offset = 0x200
        self.code, self.offset = self._generateScaffold()
    
    def _convert_offset(self, offset):
        """ Converts between the length of the program array to the final chip-8 memory location """
        return offset * 2 + 0x200

    def _generateScaffold(self):
        output_offset = dict() # Stores output locations as determined by array length

        # Initialize code with a 0, this will be replaced by a jump when the length of the program is known,
        # as well as room for the tape code to be store in
        output_code = [0]

        # Add the custom character glyphs (G-Z, !, Space) to the code
        output_offset["ascii"] = len(output_code)
        glyph_set = glyphs.get_characters()
        output_code.extend(glyph_set)

        # Append the initialization function to the code
        output_offset["init"] = len(output_code)
        initialization_code = functions.INITIALIZATION
        output_code.extend(initialization_code)

        # Set the first instruction (0x200) to jump to initialization code.
        jump_to_init_instruction = 0x1000 | self._convert_offset(output_offset["init"])
        output_code[0] = jump_to_init_instruction

        # Append the print function to the code
        output_offset["print"] = len(output_code)
        print_function = functions.PRINT
        output_code.extend(print_function)

        # Correct the position of letters in ASCII table
        character_glyph_address = self._convert_offset(output_offset["ascii"])
        space_character = 0xA000 | character_glyph_address
        output_code[output_code.index("SPACE_REPLACE_ADDRESS")] = space_character

        character_replacement_start = output_code.index("CHARACTER_REPLACE_START_ADDRESS")
        character_replacement_end = character_replacement_start + (len(glyphs.GLYPH_TABLE) - 1) * 2
        character_replacement_range = range(character_replacement_start, character_replacement_end, 2)

        for index, address in enumerate(character_replacement_range):
            character_address = character_glyph_address + ((index + 1) * 5)
            output_code[address] = 0xA000 | character_address

        # Append the shift functions to the code
        output_offset["left"] = len(output_code)
        output_code.extend(functions.MEMORY_LEFT)
        output_offset["right"] = len(output_code)
        output_code.extend(functions.MEMORY_RIGHT)

        # The scaffold code has ended
        output_offset["program"] = len(output_code)

        # Set the jump in the init function to the correct address
        init_jump_location = output_code.index("PROGRAM_JUMP")
        output_code[init_jump_location] = 0x1000 | self._convert_offset(output_offset["program"])

        # Convert all offsets into the chip-8 offset mode (8-bit addressing and 0x200 offset)
        jump_addresses = { x: self._convert_offset(y) for x, y in output_offset.items() }

        return output_code, jump_addresses

    def append(self, code):
        self.code.extend(code)
