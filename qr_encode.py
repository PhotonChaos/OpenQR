#
#   OpenQR qr_encode.py
#   By: Carbon
#
#   Handles the encoding of the QRCode data

from enum import Enum
from qr_tables import *


##############################
#   Enums and Constants
#
class EncodingMode(Enum):
    NUMERIC = 0
    ALPHA_NUMERIC = 1
    BYTE = 2
    KANJI = 3
    ECI = 4  # same size as kanji

    def __int__(self):
        if self == EncodingMode.ECI:
            return int(EncodingMode.KANJI)

        return self.value

    def indicator(self):
        if self == EncodingMode.NUMERIC:
            return [0, 0, 0, 1]
        elif self == EncodingMode.ALPHA_NUMERIC:
            return [0, 0, 1, 0]
        elif self == EncodingMode.BYTE:
            return [0, 1, 0, 0]
        elif self == EncodingMode.KANJI:
            return [1, 0, 0, 0]
        else:
            return [0, 1, 1, 1]


class CorrectionLevel(Enum):
    LOW = 0
    MEDIUM = 1
    QUARTILE = 2
    HIGH = 3


VERSION_TOO_HIGH = 41
ERROR_VERSION = -1
PAD_BYTE_17 = [0, 0, 0, 1, 0, 0, 0, 1]
PAD_BYTE_236 = [1, 1, 1, 0, 1, 1, 0, 0]


##############################
#   Helper Methods
#
def as_bin_array(n: int) -> list[int]:
    return [int(i) for i in bin(n)[2:]]


def alphanum_rep(ch: chr) -> int:
    """
    Alphanumeric representation of a character
    :param ch: The character to represent
    :return: The alphanumeric representation of ch
    """
    if ord('0') <= ord(ch) <= ord('9'):
        return ord(ch) - ord('0')

    if ord('A') <= ord(ch) <= ord('Z'):
        return 10 + ord(ch) - ord('A')

    if ch == ' ':
        return 36
    elif ch == '$':
        return 37
    elif ch == '%':
        return 38
    elif ch == '*':
        return 39
    elif ch == '+':
        return 40
    elif ch == '-':
        return 41
    elif ch == '.':
        return 42
    elif ch == '/':
        return 43
    elif ch == ':':
        return 44

    print(f"[!] Unrecognized character {ch}, ord: {ord(ch)}")
    return 0


def get_optimal_encoding(message: str) -> EncodingMode:
    """
    Consumes the message as a string, and produces the best encoding mode.
    Kanji isn't supported yet.
    :param message: The message to be encoded
    :return: The optimal encoding mode for message
    """
    optimal_mode = EncodingMode.NUMERIC

    for i in message:
        if not ord("0") <= ord(i) <= ord("9"):
            # We need alphanumeric.
            optimal_mode = EncodingMode.ALPHA_NUMERIC
        if ord("a") <= ord("i") <= ord("z"):
            return EncodingMode.BYTE

    return optimal_mode


def get_optimal_version(message, encoding_mode: EncodingMode, correction_lvl: CorrectionLevel) -> (int, int):
    """
    Produces the smallest version the message can fit in given its encoding mode and error correction level.
    :param message: The message to be encoded
    :param encoding_mode: The mode the message is to be encoded with (numeric, alphanumeric, etc.)
    :param correction_lvl: The level of error correction desired
    :return: Pair of the smallest version number to fit message & the capacity of that version with the given encoding
    """

    version = 0

    if correction_lvl == CorrectionLevel.LOW:
        correction_map = thresholds_low
    elif correction_lvl == CorrectionLevel.MEDIUM:
        correction_map = thresholds_medium
    elif correction_lvl == CorrectionLevel.QUARTILE:
        correction_map = thresholds_quartile
    elif correction_lvl == CorrectionLevel.HIGH:
        correction_map = thresholds_high
    else:
        print("[!] Error: Invalid correction level")
        return ERROR_VERSION

    while len(message) > correction_map[version][int(encoding_mode)]:
        version += 1

        if version >= len(correction_map):
            return VERSION_TOO_HIGH

    return version + 1, correction_map[version][int(encoding_mode)]


##############################
#   Encoding Methods
#

def encode_numeric(message: str) -> list[int]:
    """
    Encodes a string using the numeric mode.
    :param message: The message to encode
    :return: A binary array, representing the encoded string
    """
    message_blocks = [as_bin_array(int(message[i:i + 3])) for i in range(0, len(message), 3)]

    msg_bin = []

    for i in message_blocks:
        msg_bin.extend(i)

    return msg_bin


def encode_alphanumeric(message: str) -> list[int]:
    # break into pairs
    message_blocks = [message[i:i + 2] for i in range(0, len(message), 2)]

    message_nums = [(45 * alphanum_rep(pair[0])) + alphanum_rep(pair[1]) for pair in message_blocks[:-1]]

    if len(message_blocks[-1]) == 1:
        message_nums.append(alphanum_rep(message_blocks[-1][0]))
    else:
        message_nums.append((45 * alphanum_rep(message_blocks[-1][0])) + alphanum_rep(message_blocks[-1][1]))

    message_bin = []

    for i in range(len(message_nums)):
        bin_arr = as_bin_array(message_nums[i])

        if len(message) % 2 == 1 and i == len(message_nums) - 1:
            if len(bin_arr) < 6:
                bin_arr = [0] * (6 - len(bin_arr)) + bin_arr
        elif len(bin_arr) < 11:
            bin_arr = [0] * (11 - len(bin_arr)) + bin_arr

        message_bin.extend(bin_arr)

    return message_bin


def encode_byte(message: str) -> list[int]:
    msg_nums = [ord(i.encode('utf-8')) for i in message]

    msg_bytes = []

    for i in msg_nums:
        msg_bytes.extend(as_bin_array(i))

    return msg_bytes


def encode_kanji(message: str) -> list[int]:
    """
    NOT IMPLEMENTED
    :param message: The message to encode
    :return: The encoded message
    """
    return []


##############################
#   Main Algorithm
#

def encode_data(message: str, correction_level: CorrectionLevel) -> list[list[int]]:
    """
    Consumes a message, and produces the encoded message and the error correction code
    :param message: The message to encode
    :param correction_level: The desired level of error correction
    :return: A list of codewords, sequenced correctly
    """
    encoding_mode = get_optimal_encoding(message)

    if encoding_mode == EncodingMode.KANJI:
        print("Not supported.")
        return []

    version, capacity = get_optimal_version(message, encoding_mode, correction_level)

    if version <= ERROR_VERSION:
        print("[!] Encoding failed.")
        return []
    elif version >= VERSION_TOO_HIGH:
        print("[!] Message is too long to be encoded in a QR code.")
        print("[!]    Make it shorter, or choose a lower correction mode.")
        print("[!]    Also, try to make it all upper-case alphanumerics if you can.")

    # Encode the data.
    # At this point, 1 <= version <= 40
    # Character count indicator
    count_indicator = as_bin_array(len(message))

    if 1 <= version <= 9:
        bit_cap = indicator_bits[0][int(encoding_mode)]
    elif 10 <= version <= 26:
        bit_cap = indicator_bits[1][int(encoding_mode)]
    else:
        bit_cap = indicator_bits[2][int(encoding_mode)]

    if len(count_indicator) < bit_cap:
        count_indicator.extend([0] * (bit_cap - len(count_indicator)))

    # Now encode the data
    encoded_msg = []

    if encoding_mode == EncodingMode.NUMERIC:
        encoded_msg = encode_numeric(message)
    elif encoded_msg == EncodingMode.ALPHA_NUMERIC:
        encoded_msg = encode_alphanumeric(message)
    elif encoded_msg == EncodingMode.BYTE:
        encoded_msg = encode_byte(message)
    elif encoded_msg == EncodingMode.KANJI or encoded_msg == EncodingMode.ECI:
        print("[!] Kanji/ECI not supported")
        return []

    # Put it all together
    full_coded = encoding_mode.indicator() + count_indicator + encoded_msg

    # Get the encoding table
    codeword_table = []
    if correction_level == CorrectionLevel.LOW:
        codeword_table = codewords_low
    elif correction_level == CorrectionLevel.MEDIUM:
        codeword_table = codewords_medium
    elif correction_level == CorrectionLevel.QUARTILE:
        codeword_table = codewords_quartile
    else:
        codeword_table = CorrectionLevel.HIGH

    byte_capacity = codeword_table[version - 1]
    req_bits = byte_capacity * 8

    # Pad with up to 4 terminating 0s as needed
    full_coded += [0] * min(0, req_bits - len(full_coded), 4)

    # Pad to multiple of 8
    if len(full_coded) % 8 != 0:
        full_coded += [0] * (8 - (len(full_coded) * 8))

    # Break into bytes
    full_coded = [full_coded[x:x + 8] for x in range(0, len(full_coded), 8)]

    # Add both padding bytes, then chop last one off at the end if needed
    while len(full_coded) < byte_capacity:
        full_coded += [PAD_BYTE_236, PAD_BYTE_17]

    if len(full_coded) > byte_capacity:
        full_coded.pop()

    # Now that the bytes are in order, lets get the correction code
    return error_correct(full_coded, correction_level, version)


def error_correct(codewords: list[list[int]], correction_level: CorrectionLevel, version: int) -> list[list[int]]:
    """
    Calculates and inserts the error correction codewords
    :param codewords: List of the message encoded as codewords
    :param correction_level: The desired correction level
    :param version: The version of the QR code
    :return: A list of the error correction codewords and message codewords properly interleaved
    """

    # Step 1: Get the correction data for this version and correction level
    if correction_level == CorrectionLevel.LOW:
        correction_table = ec_low
    elif correction_level == CorrectionLevel.MEDIUM:
        correction_table = ec_medium
    elif correction_level == CorrectionLevel.QUARTILE:
        correction_table = ec_quartile
    else:
        correction_table = ec_high

    total_words, block_ec, g1_blocks, g1_block_words, g2_blocks, g2_block_words = correction_table[version - 1]

    group1, group2 = [], []

    if version > 2:
        # TODO: break up codewords into blocks according to table
        pass
    else:
        # one block
        group1 += [codewords]

    correction_blocks = []

    # TODO: Process Blocks

    if version <= 2:
        return group2 + correction_blocks

    # TODO: Interleave error correction and normal codewords
    interleaved_blocks = []

    return interleaved_blocks
