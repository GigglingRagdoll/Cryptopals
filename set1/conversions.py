import string

from functools import reduce

HEX = string.hexdigits[:-6] # only need the lowercase letters
B64 = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'

### conversions to bits

def int_to_bits(x, bitlen=8):
    bits = []

    while bitlen > 0:
        bits.append(x % 2)
        x = x // 2
        bitlen -= 1

    return bits[::-1]

def ascii_to_bits(ascii_s):
    ords = [ ord(c) for c in ascii_s ]
    bitlists = [ int_to_bits(x) for x in ords ]

    return connect(bitlists)

def hex_to_bits(hex_s):
    ints = [ HEX.index(c) for c in hex_s ]
    bitlists = [ int_to_bits(x, bitlen=4) for x in ints ]

    return connect(bitlists)

def b64_to_bits(b64_s):
    pad = b64_s.count('=')
    ints = [ B64.index(c) for c in b64_s ]
    bitlists = [ int_to_bits(x, bitlen=6) for x in ints ]

    if pad > 0:
        return connect(bitlists)[:-pad]
    else:
        return connect(bitlists)
    
### conversions from bits

def bits_to_int(bits):
    bit_s = ''.join(map(str, bits))
    return int(bit_s, 2)

def bits_to_ascii(bits):
    ords = [ bits_to_int(bitlist) for bitlist in partition(bits, 8) ]
    return ''.join([ chr(x) for x in ords ])

def bits_to_hex(bits):
    ords = [ bits_to_int(bitlist) for bitlist in partition(bits, 4) ]
    return ''.join([ HEX[x] for x in ords ])

def bits_to_b64(bits):
    pad = 6 - len(bits) % 6
    parts = partition(bits, 6)
    parts[-1] = parts[-1] + [ 0 for i in range(pad) ]
    ords = [ bits_to_int(bitlist) for bitlist in parts ]
    return ''.join([ B64[x] for x in ords ]) + ('='*(pad//2))

### helper functions

def connect(lists):
    return reduce(lambda x, y: x + y, lists)

def partition(a_list, size):
    lists = []

    while a_list:
        lists.append(a_list[:size])
        a_list = a_list[size:]

    return lists

