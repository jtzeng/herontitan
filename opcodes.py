"""
List of opcode data.
"""

OPCODES = {
    # CPU CTRL
    'NOP': [0b00000000, 1],
    'HLT': [0b00000001, 1],

    # Interrupt/Exception
    'INT': [0b00000010, 2],
    'RTE': [0b00000011, 1],

    # Arithmetic
    'ADD': [0b00010000, 2],
    'ADC': [0b00010001, 2],
    'SUB': [0b00010010, 2],
    'AND': [0b00010011, 2],
    'IOR': [0b00010100, 2],
    'XOR': [0b00010101, 2],
    'NOT': [0b00010110, 2],
    'SHR': [0b00010111, 2],
    'INC': [0b00011000, 2],
    'DEC': [0b00011001, 2],

    # Data stack
    'PSH': [0b0010, 1],
    'POP': [0b0011, 1],
    'PEK': [0b0100, 1],

    # Return stack
    'PSR': [0b0101, 1],
    'PPR': [0b0110, 1],
    'PKR': [0b0111, 1],

    # Register operations
    'CLR': [0b1000, 1],
    'MOV': [0b10010000, 2],
    'LDC': [0b1010, 2],

    # Jumps
    'JMP': [0b10110000, 3],
    'JMI': [0b10110001, 3],
    'JMR': [0b10110010, 2],
    'JRA': [0b10110011, 2],
    'JMO': [0b10110100, 4],
    'JMZ': [0b10110101, 3],
    'JMS': [0b10110110, 3],
    'JMC': [0b10110111, 3],
    'JSR': [0b10111000, 3],
    'RSB': [0b10111001, 1],

    # Load from memory
    'LDM': [0b11000000, 4],
    'LDR': [0b11000001, 3],
    'LRA': [0b11000010, 3],
    'LMO': [0b11000011, 5],

    # Store to memory
    'STM': [0b11010000, 4],
    'STR': [0b11010001, 3],
    'SRA': [0b11010010, 3],
    'SMO': [0b11010011, 5],
}
