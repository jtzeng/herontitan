"""
List of opcode data.
"""

OPCODES = {
    # CPU CTRL
    'NOP': [0b0000, 0b0000], # done
    'HLT': [0b0000, 0b0001], # done

    # Interrupt/Exception
    'INT': [0b0000, 0b0010], # done
    'RTE': [0b0000, 0b0011], # done

    # Arithmetic
    'ADD': [0b0001, 0b0000], # done
    'ADC': [0b0001, 0b0001], # done
    'SUB': [0b0001, 0b0010], # done
    'AND': [0b0001, 0b0011], # done
    'IOR': [0b0001, 0b0100], # done
    'XOR': [0b0001, 0b0101], # done
    'NOT': [0b0001, 0b0110], # done
    'SHR': [0b0001, 0b0111], # done
    'INC': [0b0001, 0b1000], # done
    'DEC': [0b0001, 0b1001], # done

    # Data stack
    'PSH': [0b0010], # done
    'POP': [0b0011], # done
    'PEK': [0b0100], # done

    # Return stack
    'PSR': [0b0101], # done
    'PPR': [0b0110], # done
    'PKR': [0b0111], # done

    # Register operations
    'CLR': [0b1000], # done
    'MOV': [0b1001, 0b0000], # done
    'LDC': [0b1010], # done

    # Jumps
    'JMP': [0b1011, 0b0000], # done
    'JMI': [0b1011, 0b0001], # done
    'JMR': [0b1011, 0b0010], # done
    'JRA': [0b1011, 0b0011], # done
    'JMO': [0b1011, 0b0100], # done
    'JMZ': [0b1011, 0b0101], # done
    'JMS': [0b1011, 0b0110], # done
    'JMC': [0b1011, 0b0111], # done
    'JSR': [0b1011, 0b1000], # done
    'RSB': [0b1011, 0b1001], # done

    # Load from memory
    'LDM': [0b1100, 0b0000], # done
    'LDR': [0b1100, 0b0001], # done
    'LRA': [0b1100, 0b0010], # done
    'LMO': [0b1100, 0b0011], # done

    # Store to memory
    'STM': [0b1101, 0b0000], # done
    'STR': [0b1101, 0b0001], # done
    'SRA': [0b1101, 0b0010], # done
    'SMO': [0b1101, 0b0011], # done
}

OPCODES_LEN = {
    # CPU CTRL
    'NOP': 1,
    'HLT': 1,

    # Interrupt/Exception
    'INT': 2,
    'RTE': 1,

    # Arithmetic
    'ADD': 2,
    'ADC': 2,
    'SUB': 2,
    'AND': 2,
    'IOR': 2,
    'XOR': 2,
    'NOT': 2,
    'SHR': 2,
    'INC': 2,
    'DEC': 2,

    # Data stack
    'PSH': 1,
    'POP': 1,
    'PEK': 1,

    # Return stack
    'PSR': 1,
    'PPR': 1,
    'PKR': 1,

    # Register operations
    'CLR': 1,
    'MOV': 2,
    'LDC': 2,

    # Jumps
    'JMP': 3,
    'JMI': 3,
    'JMR': 2,
    'JRA': 2,
    'JMO': 4,
    'JMZ': 3,
    'JMS': 3,
    'JMC': 3,
    'JSR': 3,
    'RSB': 1,

    # Load from memory
    'LDM': 4,
    'LDR': 3,
    'LRA': 3,
    'LMO': 5,

    # Store to memory
    'STM': 4,
    'STR': 3,
    'SRA': 3,
    'SMO': 5,
}