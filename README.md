# BF Chip8 Compiler
This project compiles Brainfuck Code into Chip8 assembly, which can be run on any Chip8 interpreter. 

### Limitations
 - Compiled programs must fit within 3.5Kb unless using a non-compliant Emulator
 - Only A-Z and 1-9 are possible output characters.
 - Tape length is limited to 64 slots by default, it's possible to increase length however it requires recompiling the program. Length is limited by the amount of free memory available to the interpreter.
 - Chip8 runs at only 500hz, so any programs running on a standard interpreter will be very slow. Like at least 1000x slower than what you expect (not an exaggeration).
 - Does not support input character (,) due to lack of full size keyboard.

### Screenshots
![Hello World Sample](/samples/hello_world.png)
![Alphabet Sample](/samples/alphabet.png)
