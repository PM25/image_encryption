from Crypto import Random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import numpy as np
from PIL import Image
import math

CROP_WIDTH = 16
CROP_HEIGHT = 8

class Crypt:
    def __init__(self, key, block_sz=16):
        while(len(key) < 16):
            key += '\0'
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        # self.IV = Random.new().read(block_sz)
        self.IV = b'0000000000000000'

    def encrypt(self, data):
        while(len(data) % 16 != 0):
            data += '\0'
        cryptor = AES.new(self.key, self.mode, self.IV)
        encrypted_data = cryptor.encrypt(data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        cryptor = AES.new(self.key, self.mode, self.IV)
        original_data = cryptor.decrypt(encrypted_data)
        return original_data


def split_image(image, height, width):
    sub_images = []
    img_width, img_height = image.size
    for col in range(0, img_width, width):
        for row in range(0, img_height, height):
            box = (col, row, col+width, row+height)
            sub_images.append(image.crop(box))

    return sub_images


def combine_image(images, width, height):

    img_height, img_width = images[0].shape

    i_count = math.ceil(width / CROP_WIDTH)
    j = math.ceil(height / CROP_HEIGHT)

    li = []
    for i in range(i_count):
        tmp = np.concatenate(images[i*j:(i+1)*j])
        li.append(tmp)

    return np.concatenate(li, axis=1)



# if __name__ == '__main__':
crypt = Crypt("keys")

image_file = Image.open("pm25.png")
image_file = image_file.convert('1')
image_file.convert('RGB').save('black_white.jpg')
img_width, img_height = image_file.size

encrypted_crop_imgs = []
for crop_img in split_image(image_file, CROP_HEIGHT, CROP_WIDTH):
    # Cropped imgage to bits
    img_np = np.array(crop_img).flatten()
    img_np = img_np.astype('uint8')
    img_bit = ''
    for bit in img_np:
        img_bit += str(bit)

    # bits to Bytes
    img_bytes = []
    for i in range(0, len(img_bit), 8):
        img_bytes.append(int(img_bit[i:i+8], 2))
    img_bytes = bytes(img_bytes)

    # Encrypt Crop image
    encrypted_img_bytes = crypt.encrypt(img_bytes)

    # Bytes to bits
    encrypted_img_bits = ''
    for data_byte in encrypted_img_bytes:
        data_bits = bin(data_byte)[2:].zfill(8)
        encrypted_img_bits += data_bits

    # bits to np format
    encrypted_img_bits_np = np.array([int(bit) for bit in encrypted_img_bits])
    encrypted_img_bits_np = encrypted_img_bits_np.reshape((CROP_HEIGHT, CROP_WIDTH))
    encrypted_crop_imgs.append(encrypted_img_bits_np.tolist())



# Combine crop images
encrypted_crop_imgs = np.array(encrypted_crop_imgs)
encrypted_img = combine_image(encrypted_crop_imgs, img_width, img_height)

# np to PIL
# image_file.show()
encrypted_image = Image.fromarray(encrypted_img*255)
# encrypted_image.show()
encrypted_image.convert('RGB').save("encrypted_img.jpg")