from functools import partial
from conversions import *

# english letter frequency in ascending order
EN_FREQ = 'etaoinshrdlcumwfgypbvkjxqz'[::-1]

def fixed_xor(bits1, bits2):
    zipped_bits = zip(bits1, bits2)
    xord_bits = map(lambda x: x[0] ^ x[1], zipped_bits)

    return list(xord_bits)

def single_byte_xor(bits, key):
    assert len(key) == 8

    parts = partition(bits, 8)
    curry_key = partial(fixed_xor, bits2=key)

    return connect(map(curry_key, parts))

def break_sbx(bits):
    possibilities = []
    scores = []

    for i in range(256):
        key = int_to_bits(i)
        ascii_s = bits_to_ascii(single_byte_xor(bits, key))
        possibilities.append(ascii_s)
        scores.append(score(ascii_s))

    return possibilities[scores.index(max(scores))]
    
### helper functions

def score(ascii_s):
    score = 0

    for c in ascii_s:
        try:
            score += EN_FREQ.index(c.lower())
        except:
            score -= 1

    return score

