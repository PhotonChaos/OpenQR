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
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
]

# Small squares, 5x5
SMALL_SQUARE = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

def gen_qr_data(content, version, correction_mode):
    # TODO: Auto-calculate the version value based on the size of content and the correction rate
    lw = 4 * version + 17

    img_bitmap = np.zeros((lw, lw)).astype(int)

    # pass 1: Add the 3 big squares
    img_bitmap[0:7, 0:7] = BIG_SQUARE
    img_bitmap[0:7, lw-7:lw] = BIG_SQUARE
    img_bitmap[lw-7:lw, 0:7] = BIG_SQUARE

    # Pass 2: Add the small squares
    if version > 1:
        # only needed if the data is big enough
        pass

    # Final pass, invert the bitmap. Since 0=black, we actually want to invert it.
    img_bitmap = (img_bitmap + 1) % 2
    gen_image(img_bitmap)


def gen_image(qr_data: np.ndarray):
    size = qr_data.shape[::-1]
    databytes = np.packbits(qr_data, axis=1)
    QR_image = Image.frombytes(mode="1", size=size, data=databytes)
    QR_image.show()

gen_qr_data("ASAA", 1, 0)