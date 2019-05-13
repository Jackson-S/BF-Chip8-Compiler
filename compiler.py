import argparse
from scaffold import Scaffold


def parse_arguments():
    program_description = "Convert BrainFuck code into CHIP-8 assembly instructions"

    parser = argparse.ArgumentParser(description=program_description)

    parser.add_argument("--output", "-o", default="output.ch8")
    parser.add_argument("program", help="Input brainfuck program to convert")

    return parser.parse_args()


def convert_brainfuck(bf, current_offset, scaffold):
    INSTR_INC = 0x7001 # Add one to V0
    INSTR_CALL = 0x2000 # Stores curr. address on stack and jumps to new address
    INSTR_JMP = 0x1000 # Jumps to new address
    INSTR_DECR = 0x70FF # Add 255 to V0, equivalent to -1
    INSTR_LEFT = INSTR_CALL | scaffold.offset["left"]
    INSTR_RIGHT = INSTR_CALL | scaffold.offset["right"]
    INSTR_PRINT = INSTR_CALL | scaffold.offset["print"]

    output_code = []
    current_char = 0

    while current_char < len(bf):
        if bf[current_char] == '+':
            output_code.append(INSTR_INC)
            current_char += 1

        elif bf[current_char] == '-':
            output_code.append(INSTR_DECR)
            current_char += 1

        elif bf[current_char] == '<':
            output_code.append(INSTR_LEFT)
            current_char += 1

        elif bf[current_char] == ">":
            output_code.append(INSTR_RIGHT)
            current_char += 1

        elif bf[current_char] == ".":
            output_code.append(INSTR_PRINT)
            current_char += 1

        elif bf[current_char] == "[":
            loop_end_location = find_correspond_brace(bf, current_char)

            loop_contents = bf[current_char+1:loop_end_location]

            loop_start_address = (len(output_code) * 2) + current_offset

            loop_code = convert_brainfuck(loop_contents, loop_start_address + 4, scaffold)

            loop_length = len(loop_code) * 2

            # Add 3 * 2 bytes to the length to account for 3 extra instructions
            # added for loop control.
            loop_end_address = loop_start_address + loop_length + 6

            loop_code = [0x4000, # if V0 != 0, skip next instruction
                        INSTR_JMP | loop_end_address,
                        *loop_code,
                        INSTR_JMP | loop_start_address]

            output_code.extend(loop_code)

            current_char = loop_end_location

        else:
            current_char += 1

    return output_code


def find_correspond_brace(bf, offset):
    depth = 0

    while offset < len(bf):
        if bf[offset] == '[':
            depth += 1

        elif bf[offset] == ']':
            depth -= 1

        if depth == 0:
            return offset

        offset += 1


def convert_to_program(output_code):
    program = b''

    for instruction in output_code:
        program += instruction.to_bytes(2, byteorder="big")

    return program


def main():
    args = parse_arguments()
    scaffold = Scaffold()

    with open(args.program, "r") as bfCode:
        bf = bfCode.read()

    convertedCode = convert_brainfuck(bf, scaffold.offset["program"], scaffold)
    scaffold.append(convertedCode)

    # Create an infinite loop at the end to prevent chip-8 from crashing
    self_loop_address = 0x200 + len(scaffold.code) * 2
    self_loop_code = 0x1000 | self_loop_address
    scaffold.append([self_loop_code])

    output_binary = convert_to_program(scaffold.code)

    with open(args.output, "wb") as output_file:
        output_file.write(output_binary)


if __name__ == "__main__":
    main()
