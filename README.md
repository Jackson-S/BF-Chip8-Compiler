# BF -> Chip8 Compiler
This project compiles BrainFuck Code into Chip8 assembly, which can be run on any Chip8 interpreter. 

### Web Version
You can play around with an [online Javascript version on my website.](https://jackson-s.me/converter.html)

### Limitations
 - Compiled programs *must* fit within 3840 bytes.
    - An empty file is 424 bytes, each operator character (i.e. one of .<>+-) requires 2 bytes and very loop instruction ([]) requires 3 bytes.
 - There are 256 tape positions, the tape will loop back to 0 on an overflow.
 - On most emulators due to stack constraints you can only have 15 nested loops.
 - Chip8 runs at 500 hertz, so any programs running on a standard interpreter will be very slow.
 - Programs cannot take any input.

### Screenshots
![Hello World Sample](/samples/hello_world.png)
![Alphabet Sample](/samples/alphabet.png)
