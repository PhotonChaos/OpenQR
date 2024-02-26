from PIL import Image
from enum import Enum

import numpy as np


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


# Large squares, 7x7
BIG_SQUARE = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

# Small squares, 5x5
SMALL_SQUARE = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

# TODO: Verify the actual standard of these, the number mappings vary
MASK_FORMULAS = {
    0b000: lambda x, y: x % 3,
    0b001: lambda x, y: (x+y) % 3,
    0b010: lambda x, y: (x+y) % 2,
    0b011: lambda x, y: y % 2,
    0b100: lambda x, y: ((x*y) % 3 + x*y) % 2,
    0b101: lambda x, y: ((x*y) % 3 + x + y) % 2,
    0b110: lambda x, y: (x//2 + y//3) % 2,
    0b111: lambda x, y: (x*y % 2) + (x*y % 3)
}

# Overall plan:
# - encode_data(input_string, format_version_info) -> encoded data as array of cells (with err correction)
# - construct_img(encoded_data, format_version_info) -> 2d np array = bitmap
# - gen_img(bitmap, padding=3) -> Image


def encode_data(message, data_format, correction_level):
    construct_img(message, correction_level)


def apply_mask(bitmap: np.ndarray, mask_mode):
    pass


def construct_img(encoded_content, correction_mode):
    # TODO: Auto-calculate the version value based on the size of content and the correction rate
    version = 2
    lw = 4 * version + 17

    img_bitmap = np.ones((lw, lw)).astype(int)

    # pass 1: Add the 3 big squares
    img_bitmap[0:7, 0:7] = BIG_SQUARE
    img_bitmap[0:7, lw - 7:lw] = BIG_SQUARE
    img_bitmap[lw - 7:lw, 0:7] = BIG_SQUARE

    # TODO: Pass 2: Add the small squares
    if version > 1:
        # only needed if the data is big enough
        pass

    # TODO: Pass 3, add timing patterns

    # TODO: Pass 4, add version and format information

    # TODO: Pass 5, add the data.

    gen_image(img_bitmap)


def gen_image(qr_data: np.ndarray, padding=3):
    size = qr_data.shape[::-1]
    data_bytes = np.packbits(qr_data, axis=1)
    QR_image = Image.frombytes(mode="1", size=size, data=data_bytes)
    QR_image.show()


encode_data(input("Message to encode:"), 1, 0)
