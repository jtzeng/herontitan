"""
herontitan is an assembler for bootnecklad's "Titan" processor.
"""

import sys
import logging
import argparse
from opcodes import OPCODES, OPCODES_LEN

REGISTERS = [
    'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9',
    'RA', 'RB', 'RC', 'RD', 'RE', 'RF'
]

LOG_FORMAT = '%(levelname)s: %(message)s'


_labels = {}
_address = 0
_instructions = []


# Reset the label/addr/insts state.
def reset_all():
    global _labels, _address, _instructions
    _labels = {}
    _address = 0
    _instructions = []


def get_reg(r):
    try:
        return REGISTERS.index(r)
    except ValueError:
        raise Exception('Invalid register: {}'.format(r))


def add_label(label):
    global _address
    logging.debug('(%s) Adding label: %s', _address, label)
    _labels[label] = _address


def conv_label(label):
    if _labels.has_key(label):
        logging.debug('Found label: %s => %s', label, _labels[label])
        return _labels[label]
    return label


def maybe_parse_hex(value):
    if isinstance(value, str):
        # base=0 => parse as literal.
        return int(value, 0)
    return value


def short_to_bytes(short):
    a = short >> 8
    b = short & 0b11111111
    return a, b


def add_nibbles(a, b):
    add_byte((a << 4) | b)


def add_byte(b):
    global _address
    logging.debug('(%s) Adding byte: %s', _address, format(b, '08b'))
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


# Convert a string to a C string and add it.
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
    line = line.split(';')[0].split('/')[0]

    # Remove whitespace.
    line = line.strip()

    tokens = line.split()
    if not tokens:
        return

    logging.debug('> %s', line)

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
        logging.debug('(Ignoring label on second pass.)')
        return

    # Convert labels to their memory locations.
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
        rs = get_reg(args[0])
        rd = get_reg(args[1])
        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, rd)
        return

    if mnem in ['NOT', 'SHR', 'INC', 'DEC']:
        rs = get_reg(args[0])
        # Unused?
        rd = 0
        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, rd)
        return

    if mnem in ['PSH', 'POP', 'PEK', 'PSR', 'PPR', 'PKR', 'CLR']:
        r = get_reg(args[0])
        add_nibbles(OPCODES[mnem][0], r)
        return

    if mnem == 'LDC':
        byte = maybe_parse_hex(args[0])
        rd = get_reg(args[1])
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
        rh = get_reg(args[0])
        rl = get_reg(args[1])
        add_nibbles(*OPCODES[mnem])
        add_nibbles(rh, rl)
        return

    if mnem == 'JMO':
        rh = get_reg(args[0])
        rl = get_reg(args[1])
        short = maybe_parse_hex(args[2])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(rh, rl)
        add_byte(addrh)
        add_byte(addrl)
        return

    if mnem == 'LDM':
        short = maybe_parse_hex(args[0])
        rd = get_reg(args[1])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(0b0000, rd)
        add_byte(addrh)
        add_byte(addrl)
        return

    # BROKEN
    if mnem in ['LDR', 'LRA']:
        rh = get_reg(args[0])
        rl = get_reg(args[1])
        rd = get_reg(args[2])

        add_nibbles(*OPCODES[mnem])
        add_nibbles(0b0000, rd)
        add_nibbles(rh, rl)
        return

    # BROKEN
    if mnem == 'LMO':
        rh = get_reg(args[0])
        rl = get_reg(args[1])
        short = maybe_parse_hex(args[2])
        rd = get_reg(args[3])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(0b0000, rd)
        add_nibbles(rh, rl)
        add_byte(addrh)
        add_byte(addrl)
        return

    if mnem == 'STM':
        rs = get_reg(args[0])
        short = maybe_parse_hex(args[1])

        addrh, addrl = short_to_bytes(short)

        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, 0b0000)
        add_byte(addrh)
        add_byte(addrl)
        return

    # BROKEN
    if mnem in ['STR', 'SRA']:
        rs = get_reg(args[0])
        rh = get_reg(args[1])
        rl = get_reg(args[2])

        add_nibbles(*OPCODES[mnem])
        add_nibbles(rs, 0b0000)
        add_nibbles(rh, rl)
        return

    # BROKEN
    if mnem == 'SMO':
        rs = get_reg(args[0])
        rh = get_reg(args[1])
        rl = get_reg(args[2])
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
    reset_all()
    logging.debug('Opening %s...', path)

    with open(path, 'r') as f:
        lines = f.readlines()

    # Parse the labels and count the total opcodes size.
    logging.debug('Parsing labels...')
    for line in lines:
        parse_line(line, True)

    expected_size = _address
    logging.debug('Expected size: %s', expected_size)

    # Reset the address.
    _address = 0

    # Parse the rest.
    logging.debug('Parsing again...')
    for line in lines:
        parse_line(line, False)

    insts = list(_instructions)

    # This probably shouldn't happen.
    assert expected_size == len(insts)

    return insts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug', action='store_const', dest='loglevel',
        const=logging.DEBUG, default=logging.WARNING,
        help='print all parsing steps'
    )
    parser.add_argument(
        '-b', '--bin', action='store_true', dest='binary',
        help='print result in binary format'
    )
    parser.add_argument(
        '-t', '--text', action='store_true',
        help='print result as human-readable binary text with \\n separators'
    )
    parser.add_argument(
        'inputfile',
        help='path to input source file'
    )

    cli_args = parser.parse_args()
    logging.basicConfig(format=LOG_FORMAT, level=cli_args.loglevel)

    insts = parse_file(cli_args.inputfile)
    if cli_args.binary:
        print insts_as_chr(insts)
    elif cli_args.text:
        print insts_as_bin(insts)
    else:
        print insts


if __name__ == '__main__':
    main()
