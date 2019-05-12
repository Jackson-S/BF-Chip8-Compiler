# V0 = Current character
# V2 = Memory Offset
# V3 = X Draw Coord
# V4 = Y Draw Coord
# V5 = Register set to 1 for subtracting mem offset
# V7 = Print number splitter
# V8 = Scratch Register
import glyphs
import functions

class Scaffold:
    def __init__(self, memorySize):
        # Halve the memory size as it's specified in 8 bits, but each instruction
        # consists of 16 bits.
        self.memorySize = memorySize // 2
        self.program_offset = 0x200
        self.code, self.offset = self._generateScaffold()
    
    def _convert_offset(self, offset):
        """ Converts between the length of the program array to the final chip-8 memory location """
        return offset * 2 + 0x200

    def _generateScaffold(self):
        output_offset = dict() # Stores output locations as determined by array length

        # Initialize code with a 0, this will be replaced by a jump when the length of the program is known,
        # as well as room for the tape code to be store in
        output_code = [0, *[0 for _ in range(self.memorySize)]]

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
        print_function = functions.PRINT_FUNCTION
        output_code.extend(print_function)

        # Configure the newline jump in the print function
        jump_instruction = output_offset["print"] + 82
        jump_destination = self._convert_offset(output_offset["print"]) + (84 * 2)
        output_code[jump_instruction] |= jump_destination

        # Correct the position of letters in ASCII table
        glyph_address = output_offset["print"] + 36
        for index, value in enumerate(range(glyph_address, glyph_address + 44, 2)):
            output_code[value] |= self._convert_offset(output_offset["ascii"]) + (index * 5)

        # Append the shift functions to the code
        output_offset["left"] = len(output_code)
        output_code.extend(functions.MEMORY_LEFT)
        output_offset["right"] = len(output_code)
        output_code.extend(functions.MEMORY_RIGHT)

        # Append the decrement function to the code
        output_offset["decrement"] = len(output_code)
        # Get the location of the jump address to modify later
        decrement_offset = len(output_code) + 1
        output_code.extend(functions.DECREMENT)
        decrement_jump_loc = self._convert_offset(output_offset["decrement"]) + 8
        output_code[decrement_offset] |= decrement_jump_loc

        # Set the location where program code begins (scaffold ends)
        output_offset["program"] = len(output_code)

        # Set the jump in the init function to the correct address
        init_jump_location = output_offset["init"] + 7
        output_code[init_jump_location] |= self._convert_offset(output_offset["program"])

        jump_addresses = { x: self._convert_offset(y) for x, y in output_offset.items() }

        return output_code, jump_addresses

    def appendCode(self, code):
        self.code.extend(code)
