from mylib import utils
from mylib.crypto import MyCrypto

import argparse
import numpy as np
from PIL import Image

# Arguments
parser = argparse.ArgumentParser(description="Image Encryption")
parser.add_argument("--file", "-f", type=str, default="default.jpg", help="Path to image file.")
parser.add_argument("--key", "-k", type=str, default="DefaultKey", help="Encryption Key.")
parser.add_argument("--save", "-s", type=str, default="encrypted_image.jpg", help="File name for output image.")
args = parser.parse_args()

CROP_WIDTH = 16
CROP_HEIGHT = 8



if __name__ == '__main__':
    mycrypto = MyCrypto(args.key)

    # Load image
    image = Image.open(args.file)
    image = image.convert('1')
    img_width, img_height = image.size

    encrypted_crop_imgs = []
    for crop_img in utils.split_image(image, CROP_HEIGHT, CROP_WIDTH):
        # Transform cropped image to bits format
        img_np = np.array(crop_img).flatten()
        img_np = img_np.astype('uint8')
        img_bit = ''.join([str(bit) for bit in img_np])

        # Transform bits to Bytes format
        img_bytes = []
        for i in range(0, len(img_bit), 8):
            img_bytes.append(int(img_bit[i:i+8], 2))
        img_bytes = bytes(img_bytes)

        # Encrypt cropped image
        encrypted_img_bytes = mycrypto.encrypt(img_bytes)

        # Transform Bytes to bits format
        encrypted_img_bits = ''
        for data_byte in encrypted_img_bytes:
            data_bits = bin(data_byte)[2:].zfill(8)
            encrypted_img_bits += data_bits

        # Transform bits to Numpy format
        encrypted_img_bits_np = np.array([int(bit) for bit in encrypted_img_bits])
        encrypted_img_bits_np = encrypted_img_bits_np.reshape((CROP_HEIGHT, CROP_WIDTH))
        encrypted_crop_imgs.append(encrypted_img_bits_np.tolist())


    # Combine cropped images
    encrypted_crop_imgs = np.array(encrypted_crop_imgs)
    encrypted_img = utils.combine_image(encrypted_crop_imgs, img_width, img_height)

    # Numpy to PIL
    encrypted_image = Image.fromarray(encrypted_img*255)
    encrypted_image.convert('RGB').save(args.save)