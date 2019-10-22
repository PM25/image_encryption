from mylib import utils
from mylib.crypto import MyCrypto

import argparse
import numpy as np
from PIL import Image

# Arguments
parser = argparse.ArgumentParser(description="Image Encryption")
parser.add_argument("--file", "-f", type=str, default="encrypted_image.jpg", help="Path to encrypted image file.")
parser.add_argument("--key", "-k", type=str, default="DefaultKey", help="Encryption Key.")
parser.add_argument("--save", "-s", type=str, default="decrypted_image.jpg", help="File name for output image.")
args = parser.parse_args()

CROP_WIDTH = 16
CROP_HEIGHT = 8



if __name__ == '__main__':
    mycrypto = MyCrypto(args.key)

    # Load image
    encrypted_image = Image.open(args.file)
    encrypted_image = encrypted_image.convert('1')

    img_width, img_height = encrypted_image.size

    decrypted_crop_imgs = []
    for crop_img in utils.split_image(encrypted_image, CROP_HEIGHT, CROP_WIDTH):
        # Transform cropped image to bits format
        img_np = np.array(crop_img).flatten()
        img_np = img_np.astype('uint8')
        img_bit = ''.join([str(bit) for bit in img_np])

        # Transform bits to Bytes format
        img_bytes = []
        for i in range(0, len(img_bit), 8):
            img_bytes.append(int(img_bit[i:i+8], 2))
        img_bytes = bytes(img_bytes)

        # Decrypt Crop image
        decrypted_img_bytes = mycrypto.decrypt(img_bytes)

        # Transform Bytes to bits format
        decrypted_img_bits = ''
        for data_byte in decrypted_img_bytes:
            data_bits = bin(data_byte)[2:].zfill(8)
            decrypted_img_bits += data_bits

        # Transform bits to Numpy format
        decrypted_img_bits_np = np.array([int(bit) for bit in decrypted_img_bits])
        decrypted_img_bits_np = decrypted_img_bits_np.reshape((CROP_HEIGHT, CROP_WIDTH))
        decrypted_crop_imgs.append(decrypted_img_bits_np.tolist())


    # Combine crop images
    decrypted_crop_imgs = np.array(decrypted_crop_imgs)
    decrypted_img = utils.combine_image(decrypted_crop_imgs, img_width, img_height)

    # Numpy to PIL
    decrypted_image = Image.fromarray(decrypted_img*255)
    decrypted_image.show()
    decrypted_image.convert('RGB').save(args.save)