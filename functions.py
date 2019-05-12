INITIALIZATION = [
    0x6200, # V2 = 0 (Memory offset = 0)
    0xA202, # I = 0x202 (Start of BF tape array)
    0xF065, # V0 = (&I + V2) (Current char = Tape location)
    0x6501, # V5 = 1 (Constant to subtract by 1)
    0x00E0, # Clear the display
    0x6301, # V3 = 1 (X Draw Coords)
    0x6401, # V4 = 1 (Y Draw Coords)
    # Skip to program code
    0x1000, # Jump to beginning of program code (this will be modified with the correct code start address later)
]

PRINT_FUNCTION = [
    # Convert into ASCII
    0x8700, # V7 = V0 (Load V0 into a temp reg.)
    # Convert V7 to lowercase (OR with 0x20)
    0x6820, # V8 = 0x20
    0x8781, # V7 |= V8
    # Cycle through supported chars to find correct one, then set I to
    # the address of the character's glyph
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
    0x4761, # Skip if not a
    0xA032, # Set I to address of a
    0x4762, # Skip if not b
    0xA037, # Set I to address of b
    0x4763, # Skip if not c
    0xA03C, # Set I to address of c
    0x4764, # Skip if not d
    0xA041, # Set I to address of d
    0x4765, # Skip if not e
    0xA046, # Set I to address of e
    0x4766, # Skip if not f
    0xA04B, # Set I to address of f
    0x4767, # Skip if not g
    # Characters below are not in the builtin font set, so the access method differs
    # The correct addresses for each character is added in later by the program.
    0xA000, # Set I to address of g
    0x4768, # Skip if not h
    0xA000, # Set I to address of h
    0x4769, # Skip if not i
    0xA000, # Set I to address of i
    0x476A, # Skip if not j
    0xA000, # Set I to address of j
    0x476B, # Skip if not k
    0xA000, # Set I to address of k
    0x476C, # Skip if not l
    0xA000, # Set I to address of l
    0x476D, # Skip if not m
    0xA000, # Set I to address of m
    0x476E, # Skip if not n
    0xA000, # Set I to address of n
    0x476F, # Skip if not o
    0xA000, # Set I to address of o
    0x4770, # Skip if not p
    0xA000, # Set I to address of p
    0x4771, # Skip if not q
    0xA000, # Set I to address of q
    0x4772, # Skip if not r
    0xA000, # Set I to address of r
    0x4773, # Skip if not s
    0xA000, # Set I to address of s
    0x4774, # Skip if not t
    0xA000, # Set I to address of t
    0x4775, # Skip if not u
    0xA000, # Set I to address of u
    0x4776, # Skip if not v
    0xA000, # Set I to address of v
    0x4777, # Skip if not w
    0xA000, # Set I to address of w
    0x4778, # Skip if not x
    0xA000, # Set I to address of x
    0x4779, # Skip if not y
    0xA000, # Set I to address of y
    0x477A, # Skip if not z
    0xA000, # Set I to address of z
    0x4721, # Skip if not !
    0xA000, # Set I to address of !
    0x4720, # Skip if not Space
    0xA000, # Set I to address of Space
    # Begin drawing character at I
    0xD345, # Draw character that I points to at X=V3, Y=V4, H=0x05
    0x7305, # V3 += 5 (Increment X offset by 5 for next character)
    0x433D, # Skip V3 != 0x3D (Used to create a new line if necessary)
    0x1000, # Jump to new line subroutine (OR'd in later)
    0x00EE, # Return from print function
    # New line subroutine
    0x6301, # V3 = 0x01 (X value reset to 1)
    0x7406, # V4 += 0x06 (Y Value increased for new line offset)
    0x00EE, # Return from print function
]

MEMORY_LEFT = [
    # Memory Pointer Left Function
    # Store previous value in V0 to memory
    0xA202, # Set I to beginning of memory
    0xF21E, # Increment I to current memory offset
    0xF055, # Store contents of V0 to memory
    # Begin setting new offset
    0x8255, # Subtract 1 (in V5) from V2
    0xA202, # Set I to beginning of memory
    0xF21E, # Increment I to new memory offset
    0xF065, # Fill register V0 with new value
    0x00EE, # Return from pointer left function
]

MEMORY_RIGHT = [
    #Store previous value in V0 to memory
    0xA202, # Set I to beginning of memory
    0xF21E, # Increment I to current memory offset
    0xF055, # Store contents of V0 to memory
    # Begin setting new offset
    0x7201, # V2 (mem offset) += 1
    0xA202, # Set I to beginning of memory
    0xF21E, # Increment I to new memory offset
    0xF065, # Load V0 with content in I
    0x00EE, # Return from pointer right function
]

DECREMENT = [
    0x3000, # Skip if V0 != 0
    0x1000, # Goto standard sub code (OR'd in later)
    # If V0 == 0
    0x60FF, # Set V0 = 0xFF
    0x00EE, # Return from Decrement
    # Standard subtract
    0x8055, # V0 -= 1
    0x00EE, # Return from Decrement
]