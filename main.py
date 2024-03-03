import qr_encode
import image_gen

# Overall plan:
# 1. Get the data and user's desired parameters
# 2. Encode the data via qr_encode.py
# 3. Stitch the data into a bitmap and display it via image_gen.py

if __name__ == '__main__':
    correction_lvl = qr_encode.CorrectionLevel.LOW

    print("[*] Encoding data...")
    encoded_data = qr_encode.encode_data(input("[*] Message to encode: "), correction_lvl)

    print("[*] Stitching bitmap...")
    qr_img = image_gen.construct_qr(encoded_data, correction_lvl)
    
    print("[*] Done!")
    
    qr_img.show()
