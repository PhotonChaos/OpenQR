from PIL import Image
import numpy as np

# Encoding modes
NUMERIC = "numeric"
ALPHA_NUMERIC = "alpha_numeric"
BYTE = "byte"
KANJI = "kanji"

# Shapes

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


# Overall plan:
# - encode_data(input_string, format_version_info) -> encoded data as array of cells (with err correction)
# - stitch_img_bitmap(encoded_data, format_version_info) -> 2d np array = bitmap
# - gen_img(bitmap, padding=3) -> Image

def gen_qr_data(content, version, correction_mode):
    # TODO: Auto-calculate the version value based on the size of content and the correction rate
    lw = 4 * version + 17

    img_bitmap = np.ones((lw, lw)).astype(int)

    # pass 1: Add the 3 big squares
    img_bitmap[0:7, 0:7] = BIG_SQUARE
    img_bitmap[0:7, lw-7:lw] = BIG_SQUARE
    img_bitmap[lw-7:lw, 0:7] = BIG_SQUARE

    # TODO: Pass 2: Add the small squares
    if version > 1:
        # only needed if the data is big enough
        pass

    # TODO: Pass 3, add timing patterns

    # TODO: Pass 4, add version and format information

    # TODO: Pass 5, add the data.

    gen_image(img_bitmap)


def gen_image(qr_data: np.ndarray):
    size = qr_data.shape[::-1]
    databytes = np.packbits(qr_data, axis=1)
    QR_image = Image.frombytes(mode="1", size=size, data=databytes)
    QR_image.show()

gen_qr_data("ASAA", 1, 0)