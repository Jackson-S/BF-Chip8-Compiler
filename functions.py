# V0 = Current character on tape
# V2 = Memory Offset (0xF00 + V2 is memory address of current tape position)
# V3, V4 = X & Y coordinate for print function respectively.
# V7, V8, V9 = Temp. Used in print function.
# Free use:
# V1, V5, V6, VA, VB, VC, VD, VE

INITIALIZATION = [
    # REGISTER SETUP
    0x6200, # V2 = 0. Register 2 will store the tape index

    0xAF00, # I = Tape start address (0xF00), or 0xFFF - 0xFF (last memory address - 256)
    
    # Setup X and Y coordinates for drawing.
    0x6301, # V3 = 1 (X Draw Coords)
    0x6401, # V4 = 1 (Y Draw Coords)

    # Jump to program code. This is added in later.
    "PROGRAM_JUMP",
]


PRINT = [
    # PREPARATION TO PRINT VALUE
    # Set up temporary values to be modified
    0x8700, # V7 = V0 (Will be used as a temp register, as the value may be altered to be uppercase)
    
    0x8A00, # VA = V0 (Will be used as a temp register, to check if value is in upper case letter range, 
            # as this requires a subtraction.)
    
    # Check if the character is lowercase and convert it if it is
    0x6861, # V8 = 0x61 (Load in lowercase a to register 8 to subtract from register 7)
    0x8A85, # VA = VA - V8, VF = VA > V8 (Equivalent to VF = bool('a' > V8). 
            # Should return true if value is upper case)

    0x6920, # V9 = 0x20, as (lower case character - 0x20 = Upper case character)
    0x3F00, # Skip next line if VA was < 'a', i.e. Skip if letter is below lower case range.
    0x8795, # V7 -= V9 (0x20), Subtract 20 from lower case character to make upper case.

    # LOAD CHARACTER GLYPH ADDRESS INTO REGISTER I
    "SPACE_REPLACE_ADDRESS", # Set I to address of space, this will act as a default character
    
    # These characters exist in the chip-8 rom, so to save memory that representation will be used.
    0x4730, # Skip if not 0
    0xA000, # Set I to address of 0
    0x4731, # Skip if not 1
    0xA005, # Set I to address of 1
    0x4732, # Skip if not 2
    0xA00A, # Set I to address of 2
    0x4733, # Skip if not 3
    0xA00F, # Set I to address of 3
    0x4734, # Skip if not 4
    0xA014, # Set I to address of 4
    0x4735, # Skip if not 5
    0xA019, # Set I to address of 5
    0x4736, # Skip if not 6
    0xA01E, # Set I to address of 6
    0x4737, # Skip if not 7
    0xA023, # Set I to address of 7
    0x4738, # Skip if not 8
    0xA028, # Set I to address of 8
    0x4739, # Skip if not 9
    0xA02D, # Set I to address of 9
    0x4741, # Skip if not a
    0xA032, # Set I to address of a
    0x4742, # Skip if not b
    0xA037, # Set I to address of b
    0x4743, # Skip if not c
    0xA03C, # Set I to address of c
    0x4744, # Skip if not d
    0xA041, # Set I to address of d
    0x4745, # Skip if not e
    0xA046, # Set I to address of e
    0x4746, # Skip if not f
    0xA04B, # Set I to address of f
    
    # Characters below are not in the builtin font set, so we load in a custom
    # glyph set. The 0xA000 commands are replaced later with the correct address, which
    # is determined by the order of appearance in the glyph set.
    0x4747, # Skip if not g
    "CHARACTER_REPLACE_START_ADDRESS", # Set I to address of g
    0x4748, # Skip if not h
    0xA000, # Set I to address of h
    0x4749, # Skip if not i
    0xA000, # Set I to address of i
    0x474A, # Skip if not j
    0xA000, # Set I to address of j
    0x474B, # Skip if not k
    0xA000, # Set I to address of k
    0x474C, # Skip if not l
    0xA000, # Set I to address of l
    0x474D, # Skip if not m
    0xA000, # Set I to address of m
    0x474E, # Skip if not n
    0xA000, # Set I to address of n
    0x474F, # Skip if not o
    0xA000, # Set I to address of o
    0x4750, # Skip if not p
    0xA000, # Set I to address of p
    0x4751, # Skip if not q
    0xA000, # Set I to address of q
    0x4752, # Skip if not r
    0xA000, # Set I to address of r
    0x4753, # Skip if not s
    0xA000, # Set I to address of s
    0x4754, # Skip if not t
    0xA000, # Set I to address of t
    0x4755, # Skip if not u
    0xA000, # Set I to address of u
    0x4756, # Skip if not v
    0xA000, # Set I to address of v
    0x4757, # Skip if not w
    0xA000, # Set I to address of w
    0x4758, # Skip if not x
    0xA000, # Set I to address of x
    0x4759, # Skip if not y
    0xA000, # Set I to address of y
    0x475A, # Skip if not z
    0xA000, # Set I to address of z
    0x4721, # Skip if not !
    0xA000, # Set I to address of !
    0x4722, # Skip if not "
    0xA000, # Set I to address of "
    0x4723, # Skip if not #
    0xA000, # Set I to address of #
    0x4724, # Skip if not $
    0xA000, # Set I to address of $
    0x4725, # Skip if not %
    0xA000, # Set I to address of %
    0x4726, # Skip if not &
    0xA000, # Set I to address of &
    0x4727, # Skip if not '
    0xA000, # Set I to address of '
    0x4728, # Skip if not (
    0xA000, # Set I to address of (
    0x4729, # Skip if not )
    0xA000, # Set I to address of )
    0x472A, # Skip if not *
    0xA000, # Set I to address of *


    # DRAW CHARACTER TO SCREEN
    # Draws the character at the address loaded into register I to the display,
    # and takes care of newlines and new pages.
    0xD345, # Draw the glyph in register I, at location x=V3, y=V4, height=5.
    
    # Add offsets for next character draw
    0x7305, # V3 += 5 (Increment X offset by 5 for next character)
    0x333D, # Skips the return if x is at the end of the page (goes into newline code)
    0x00EE, # Return from print function
    
    # Set drawing coordinates to new line start position.
    0x6301, # V3 = 0x01 (X value reset to 1)
    0x7406, # V4 += 0x06 (Y Value increased for new line offset)
    
    0x341F, # Skip if v4 == 0x25. This will go to the new page code if 
            #the Y value is at the bottom of the display.
    0x00EE, # Return from print
    
    # New page setup
    0x00E0, # Clear the display
    0x6401, # Load 0x01 into V4, (y value reset to 1)
    0x00EE, # Return from newline function
]

MEMORY_LEFT = [
    # Performs the brainfuck "<" operator
    # Set I back to the correct memory position (as it may be changed by printing)
    0xAF00, # Set I to beginning of memory
    0xF21E, # Increment I to current memory offset

    # Stores the contents of V0 (the current value at the tape address) to memory
    0xF055, # Store contents of V0 to memory
    
    # Set I to the new offset
    0x72FF, # Subtract 1 (via wrapping register with += 0xFF) from Register 2 (Tape index register)
    0xAF00, # Set I to beginning of memory
    0xF21E, # Increment I to new memory offset
    
    # Load new value pointed to by register I
    0xF065, # Fill register V0 with new value
    0x00EE, # Return from pointer left function
]

MEMORY_RIGHT = [
    # Performs the brainfuck ">" operator
    # Set I back to the correct memory position (as it may be changed by printing)
    0xAF00, # Set I to beginning of memory
    0xF21E, # Increment I to current memory offset
    
    # Stores the contents of V0 (the current value at the tape address) to memory
    0xF055, # Store contents of V0 to memory
    
    # Set I to the new offset
    0x7201, # Add 1 to Register 2 (Tape index register)
    0xAF00, # Set I to beginning of memory
    0xF21E, # Increment I to new memory offset
    
    # Load new value pointed to by register I
    0xF065, # Load V0 with content in I
    0x00EE, # Return from pointer right function
]