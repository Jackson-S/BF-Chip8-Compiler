import argparse
from scaffold import Scaffold


def parseArguments():
    programDescription = "Convert BrainFuck code into CHIP-8 assembly instructions"
    parser = argparse.ArgumentParser(description=programDescription)
    memoryHelp="Memory size allotment for the resident Brainfuck code"
    parser.add_argument("--memory", "-m", type=int, default=64, help=memoryHelp)
    parser.add_argument("--output", "-o", default="output.ch8")
    parser.add_argument("program", help="Input brainfuck program to convert")
    return parser.parse_args()


def convertBrainfuck(bf, currentOffset, scaffold):
    INSTR_INC = 0x7001 # Add one to V0
    INSTR_CALL = 0x2000 # Stores curr. address on stack and jumps to new address
    INSTR_JMP = 0x1000 # Jumps to new address

    outputCode = []
    currentChar = 0

    while currentChar < len(bf):
        if bf[currentChar] == '+':
            outputCode.append(INSTR_INC)
            currentChar += 1

        elif bf[currentChar] == '-':
            outputCode.append(INSTR_CALL | scaffold.offset["decrement"])
            currentChar += 1

        elif bf[currentChar] == '<':
            outputCode.append(INSTR_CALL | scaffold.offset["left"])
            currentChar += 1

        elif bf[currentChar] == ">":
            outputCode.append(INSTR_CALL | scaffold.offset["right"])
            currentChar += 1

        elif bf[currentChar] == ".":
            outputCode.append(INSTR_CALL | scaffold.offset["print"])
            currentChar += 1

        elif bf[currentChar] == "[":
            loopEndLocation = findCorrespondingBrace(bf, currentChar)

            loopContents = bf[currentChar+1:loopEndLocation]

            loopStartAddress = (len(outputCode) * 2) + currentOffset

            loopCode = convertBrainfuck(loopContents, loopStartAddress + 4, scaffold)

            loopLength = len(loopCode) * 2

            # Add 3 * 2 bytes to the length to account for 3 extra instructions
            # added for loop control.
            loopEndAddress = loopStartAddress + loopLength + 6

            loopCode = [0x4000, # if V0 != 0, skip next instruction
                        INSTR_JMP | loopEndAddress,
                        *loopCode,
                        INSTR_JMP | loopStartAddress]

            outputCode.extend(loopCode)

            currentChar = loopEndLocation

        else:
            currentChar += 1

    return outputCode


def findCorrespondingBrace(bf, offset):
    depth = 0

    while offset < len(bf):
        if bf[offset] == '[':
            depth += 1

        elif bf[offset] == ']':
            depth -= 1

        if depth == 0:
            return offset

        offset += 1


def convertToProgram(outputCode):
    program = b''

    for instruction in outputCode:
        program += instruction.to_bytes(2, byteorder="big")

    return program


def main():
    args = parseArguments()
    scaffold = Scaffold(args.memory // 2)

    with open(args.program, "r") as bfCode:
        bf = bfCode.read()

    convertedCode = convertBrainfuck(bf, scaffold.offset["program"], scaffold)
    scaffold.appendCode(convertedCode)

    outputBinary = convertToProgram(scaffold.code)

    with open(args.output, "wb") as outputFile:
        outputFile.write(outputBinary)


if __name__ == "__main__":
    main()
