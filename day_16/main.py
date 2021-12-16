from functools import reduce
from operator import mul
from typing import NamedTuple, Optional


class Instruction(NamedTuple):
    version_number: int
    operator: int
    sub_instructions: list
    value: Optional[int]
    bit_size: int


def load_input(file_name: str) -> str:
    with open(file_name, "r") as input_file:
        return input_file.readline().strip()


def hex_char_to_binary_string(hex_chr: chr) -> str:
    return "{0:04b}".format(int(hex_chr, 16))


def hex_message_to_binary(message: str) -> str:
    return "".join(map(hex_char_to_binary_string, message))


def parse_instruction_from_binary(binary_message: str):
    i = 0
    version = int(binary_message[i: i + 3], 2)
    operator = int(binary_message[i + 3: i + 6], 2)
    sub_instructions = []
    value = None
    i += 6
    if operator == 4:
        sub_packets = []
        while binary_message[i] == "1":
            sub_packets.append(binary_message[i + 1: i + 5])
            i += 5
        sub_packets.append(binary_message[i + 1: i + 5])
        i += 5
        value = int("".join(sub_packets), 2)
    else:
        length_type = binary_message[i]
        i += 1
        if length_type == "0":
            length_of_sub_packets = int(binary_message[i: i + 15], 2)
            i += 15
            end_of_sub_packets = i + length_of_sub_packets
            while i < end_of_sub_packets:
                sub_instruction = parse_instruction_from_binary(
                    binary_message[i: i + end_of_sub_packets]
                )
                i += sub_instruction.bit_size
                sub_instructions.append(sub_instruction)
        else:
            number_of_sub_packets = int(binary_message[i: i + 11], 2)
            i += 11
            for _ in range(number_of_sub_packets):
                sub_instruction = parse_instruction_from_binary(binary_message[i:])
                i += sub_instruction.bit_size
                sub_instructions.append(sub_instruction)
    bit_size = i
    instruction = Instruction(version, operator, sub_instructions, value, bit_size)
    return instruction


def process_instruction(instruction: Instruction):
    if instruction.operator == 4:
        return instruction.value
    elif instruction.operator == 0:
        return sum(map(process_instruction, instruction.sub_instructions))
    elif instruction.operator == 1:
        return reduce(mul, map(process_instruction, instruction.sub_instructions), 1)
    elif instruction.operator == 2:
        return min(map(process_instruction, instruction.sub_instructions))
    elif instruction.operator == 3:
        return max(map(process_instruction, instruction.sub_instructions))
    elif instruction.operator == 5:
        first = process_instruction(instruction.sub_instructions[0])
        second = process_instruction(instruction.sub_instructions[1])
        return 1 if first > second else 0
    elif instruction.operator == 6:
        first = process_instruction(instruction.sub_instructions[0])
        second = process_instruction(instruction.sub_instructions[1])
        return 1 if first < second else 0
    elif instruction.operator == 7:
        first = process_instruction(instruction.sub_instructions[0])
        second = process_instruction(instruction.sub_instructions[1])
        return 1 if first == second else 0


def add_version_numbers(top_instruction: Instruction):
    version_sum = 0
    instructions = [top_instruction]
    while len(instructions) > 0:
        instruction = instructions.pop()
        version_sum += instruction.version_number
        instructions += instruction.sub_instructions
    return version_sum


if __name__ == "__main__":
    file_input = load_input("input.txt")
    converted_file_input = hex_message_to_binary(file_input)
    input_instruction = parse_instruction_from_binary(converted_file_input)
    print(add_version_numbers(input_instruction))
    print(process_instruction(input_instruction))
