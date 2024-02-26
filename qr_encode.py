#
#   OpenQR qr_encode.py
#   By: Carbon
#
#   Handles the encoding of the QRCode data

from enum import Enum


class EncodingMode(Enum):
    NUMERIC = 0
    ALPHA_NUMERIC = 1
    BYTE = 2
    KANJI = 3


class CorrectionLevel(Enum):
    LOW = 0
    MEDIUM = 1
    QUARTILE = 2
    HIGH = 3


##############################
#   Helper Methods
#

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


##############################
#   Main Algorithm
#
def encode_data(message, correction_level) -> list[int]:
    encoding_mode = get_optimal_encoding(message)

    if encoding_mode == EncodingMode.KANJI:
        print("Not supported.")
        return message

    # TODO: Encode data

    # TODO: Error correction

    return message
