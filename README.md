# BF -> Chip8 Compiler
This project compiles BrainFuck Code into Chip8 assembly, which can be run on any Chip8 interpreter. 

### Web Version
You can play around with an [online Javascript version on my website.](https://jackson-s.me/converter.html)

### Limitations
 - Compiled programs *must* fit within 3840 bytes.
    - An empty file is 424 bytes.
    - Every occurrence of .<>+- requires 2 bytes.
    - Every occurrence of [] requires 3 bytes in total.
 - Input code only has 255 tape slots (i.e. ">" loops to 0 after 256 occurrences).
 - Cannot have more than 15 nested loops at a time (this can be worked around in some non-compliant emulators that have a larger stack size).
 - Chip8 runs at *500**hz***, so any programs running on a standard interpreter will be very slow. Like at least 1000x slower than what you expect (not an exaggeration).
 - Does not support input character (,) due to lack of full size keyboard.

### Screenshots
![Hello World Sample](/samples/hello_world.png)
![Alphabet Sample](/samples/alphabet.png)
