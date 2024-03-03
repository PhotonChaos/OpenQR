#
#   OpenQR image_gen.py
#   By: Carbon
#
#   This file takes in the encoded data, and stitches together an image from it.

from PIL import Image

##############################
#   Constants
#
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

##############################
#   Main Algorithm
#
def apply_mask(bitmap, mask_mode):
    pass


def gen_image(qr_data: list[list[int]], padding=3) -> Image:
    qr_img = Image.fromarray(qr_data)
    return qr_img


def construct_qr(encoded_content, correction_mode) -> Image:
    # TODO: Auto-calculate the version value based on the size of content and the correction rate
    version = 2
    lw = 4 * version + 17

    img_bitmap = [[1]*lw]*lw

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
    
    # TODO: Pass 6, apply the mask

    return gen_image(img_bitmap)
