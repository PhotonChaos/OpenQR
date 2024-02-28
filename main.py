import qr_encode
import image_gen


# Overall plan:
# - encode_data(input_string, format_version_info) -> encoded data as array of cells (with err correction)
# - construct_img(encoded_data, format_version_info) -> 2d np array = bitmap
# - gen_img(bitmap, padding=3) -> Image


if __name__ == '__main__':
    correction_lvl = qr_encode.CorrectionLevel.LOW

    print("Encoding data...")
    encoded_data = qr_encode.encode_data(input("Message to encode: "), correction_lvl)

    print("Stitching bitmap...")
    qr_data = image_gen.construct_img(encoded_data, correction_lvl)

    print("Generating image...")
    qr_img = image_gen.gen_image(qr_data)

    print("Done!")
    qr_img.show()
