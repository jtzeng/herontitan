"""
herontitan is an assembler for bootnecklad's "Titan" processor.
"""
import sys

REGISTERS = [
    'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9',
    'RA', 'RB', 'RC', 'RD', 'RE', 'RF'
]

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

_labels = {}
_address = 0
_instructions = []


# ???
def debug(s):
    print s


# Resets the label/addr/insts state.
def reset():
    global _labels, _address, _instructions
    _labels = {}
    _address = 0
    _instructions = []


def add_label(label):
    global _address
    debug('({}) Adding label: {}'.format(_address, label))
    _labels[label] = _address


def conv_label(label):
    if _labels.has_key(label):
        debug('Found label: {} => {}'.format(label, _labels[label]))
        return _labels[label]
    return label


def maybe_parse_hex(value):
    if isinstance(value, str):
        if value.startswith('0x'):
            return int(value, 16)
        else:
            return int(value)
    return value


def short_to_bytes(short):
    a = short >> 8
    b = short & 0b11111111
    return a, b


def add_nibbles(a, b):
    add_byte((a << 4) | b)


def add_byte(b):
    global _address
    debug('({}) Adding byte: {}'.format(_address, format(b, '08b')))
    if b < 0 or b > 255:
        raise ValueError('byte is not in range: {}'.format(b))
    _instructions.append(b)
    _address += 1


def add_byte_label(label, byte):
    add_label(label)
    add_byte(byte)


# A word is actually a 16 bit short.
def add_word(label, short):
    add_label(label)

    addrh, addrl = short_to_bytes(short)
    add_byte(addrh)
    add_byte(addrl)


def add_raw(data):
    for d in data:
        add_byte(d)


def add_data(label, data):
    add_label(label)
    add_raw(data)


# Converts a string to a C string and adds it.
def add_string(label, s):
    add_label(label)
    chars = map(ord, list(strip_quotes(s) + '\0'))
    for c in chars:
        add_byte(c)


# Doesn't actually strip the quotes. It just checks if it starts and
# ends with it and removes the beginning and ending char.
def strip_quotes(s):
    if not s.startswith('"') or not s.endswith('"'):
        raise ValueError('string not enclosed in "" quotes: {}'.format(s))
    return s[1:-1]


def parse_line(line, labels_only):
    global _address

    # Remove comments.
    line = line.split(';')[0]

    # Remove whitespace.
    line = line.strip()

    tokens = line.split()
    if not tokens:
        return

    debug('> {}'.format(line))

    mnem = tokens[0]
    args = tokens[1].split(',') if tokens[1:] else None

    if labels_only:
        # Process data.

        if mnem == '.BYTE':
            label = tokens[1]
            value = maybe_parse_hex(tokens[2])
            add_byte_label(label, value)
            return

        if mnem == '.WORD':
            label = tokens[1]
            value = maybe_parse_hex(tokens[2])
            add_word(label, value)
            return

        if mnem == '.DATA':
            label = tokens[1]
            add_data(label, map(maybe_parse_hex, tokens[2:]))
            return

        if mnem == '.RAW':
            add_raw(map(maybe_parse_hex, tokens[1:]))
            return

        if mnem == '.ASCIZ':
            label = tokens[1]
            add_string(label, ' '.join(line.split(' ')[2:]))
            return

        # Process labels.
        if line.endswith(':'):
            label = line[:-1]
            add_label(label)
            return

        if mnem in OPCODES_LEN:
            sz = OPCODES_LEN[mnem]
            _address += sz
            return

        # Don't bother with the rest if we're only parsing labels.
        raise Exception('Undefined instruction: {}'.format(line))


    # Ignore all labels during second-pass.
    if line.startswith('.') or line.endswith(':'):
        debug('(Ignoring label on second pass.)')
        return

    # Converts labels to their memory locations.
    if args:
        args = map(lambda s: conv_label(s), args)

    # Process instructions.

    # (no args)
    if mnem in ['NOP', 'HLT', 'RSB', 'RTE']:
        add_nibbles(*OPCODES[mnem])
        return

    if mnem == 'INT':
        byte = maybe_parse_hex(args[0])
        add_nibbles(*OPCODES[mnem])
        add_byte(byte)
        return

    if mnem in ['ADD', 'ADC', 'SUB', 'AND', 'IOR', 'XOR', 'MOV']:
        rs = REGISTERS.index(args[0])
        rd = REGISTERS.index(args[1])
        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, rd)
        return

    if mnem in ['NOT', 'SHR', 'INC', 'DEC']:
        rs = REGISTERS.index(args[0])
        # Unused?
        rd = 0
        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, rd)
        return

    if mnem in ['PSH', 'POP', 'PEK', 'PSR', 'PPR', 'PKR', 'CLR']:
        r = REGISTERS.index(args[0])
        add_nibbles(OPCODES[mnem][0], r)
        return

    if mnem == 'LDC':
        byte = maybe_parse_hex(args[0])
        rd = REGISTERS.index(args[1])
        add_nibbles(OPCODES[mnem][0], rd)
        add_byte(byte)
        return

    if mnem in ['JMP', 'JMI', 'JMZ', 'JMS', 'JMC', 'JSR']:
        short = maybe_parse_hex(args[0])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_byte(addrh)
        add_byte(addrl)
        return

    if mnem in ['JMR', 'JRA']:
        rh = REGISTERS.index(args[0])
        rl = REGISTERS.index(args[1])
        add_nibbles(*OPCODES[mnem])
        add_nibbles(rh, rl)
        return

    if mnem == 'JMO':
        rh = REGISTERS.index(args[0])
        rl = REGISTERS.index(args[1])
        short = maybe_parse_hex(args[2])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(rh, rl)
        add_byte(addrh)
        add_byte(addrl)
        return

    if mnem == 'LDM':
        short = maybe_parse_hex(args[0])
        rd = REGISTERS.index(args[1])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(0b0000, rd)
        add_byte(addrh)
        add_byte(addrl)
        return

    # BROKEN
    if mnem in ['LDR', 'LRA']:
        rh = REGISTERS.index(args[0])
        rl = REGISTERS.index(args[1])
        rd = REGISTERS.index(args[2])

        add_nibbles(*OPCODES[mnem])
        add_nibbles(0b0000, rd)
        add_nibbles(rh, rl)
        return

    # BROKEN
    if mnem == 'LMO':
        rh = REGISTERS.index(args[0])
        rl = REGISTERS.index(args[1])
        short = maybe_parse_hex(args[2])
        rd = REGISTERS.index(args[3])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(0b0000, rd)
        add_nibbles(rh, rl)
        add_byte(addrh)
        add_byte(addrl)
        return

    if mnem == 'STM':
        rs = REGISTERS.index(args[0])
        short = maybe_parse_hex(args[1])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, 0b0000)
        add_byte(addrh)
        add_byte(addrl)
        return

    # BROKEN
    if mnem in ['STR', 'SRA']:
        rs = REGISTERS.index(args[0])
        rh = REGISTERS.index(args[1])
        rl = REGISTERS.index(args[2])

        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, 0b0000)
        add_nibbles(rh, rl)
        return

    # BROKEN
    if mnem == 'SMO':
        rs = REGISTERS.index(args[0])
        rh = REGISTERS.index(args[1])
        rl = REGISTERS.index(args[2])
        short = maybe_parse_hex(args[3])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, 0b0000)
        add_nibbles(rh, rl)
        add_byte(addrh)
        add_byte(addrl)
        return

    # Any 'undefined' instruction errors should probably be all
    # caught during the first-pass parsing.
    raise Exception('Undefined instruction?: {}'.format(line))


def insts_as_chr(insts):
    return ''.join(map(chr, insts))


def insts_as_bin(insts):
    return '\n'.join(map(lambda b: format(b, '08b'), insts))


# Parse an assembly file and return a copy of the list of instructions.
def parse_file(path):
    global _address
    reset()
    debug('Parsing {}...'.format(path))

    with open(path, 'r') as f:
        lines = f.readlines()

    # Parse the labels and count the total opcodes size.
    for line in lines:
        parse_line(line, True)

    expected_size = _address
    debug('Expected size: {}'.format(expected_size))

    # Reset the address.
    _address = 0

    # Parse the rest.
    for line in lines:
        parse_line(line, False)

    insts = list(_instructions)

    # This probably shouldn't happen.
    assert expected_size == len(insts)

    # debug(insts_as_chr(insts))
    # debug(insts_as_bin(insts))
    # debug(insts)

    return insts


if __name__ == '__main__':
    if not sys.argv[1:]:
        debug('usage: {} path-to-source'.format(sys.argv[0]))
    else:
        print parse_file(sys.argv[1])
