from Crypto import Random
from Crypto.Cipher import AES
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

encrypted_image = Image.open("encrypted_img.jpg")
encrypted_image = encrypted_image.convert('1')

# tmp_np = np.array(encrypted_image)
# x_count, y_count = tmp_np.shape
# import random
# for i in range(math.ceil(x_count * y_count * 1e-3)):
#     x = random.randint(0, x_count-1)
#     y = random.randint(0, y_count-1)
#     tmp_np[x][y] = not(tmp_np[x][y])
# encrypted_image = Image.fromarray(tmp_np)
# encrypted_image.convert('RGB').save('Disturbed_img.jpg')
# encrypted_image.show()

img_width, img_height = encrypted_image.size

decrypted_crop_imgs = []
for crop_img in split_image(encrypted_image, CROP_HEIGHT, CROP_WIDTH):
    # Crop imgage to bits
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

    # Decrypt Crop image
    decrypted_img_bytes = crypt.decrypt(img_bytes)

    # Bytes to bits
    decrypted_img_bits = ''
    for data_byte in decrypted_img_bytes:
        data_bits = bin(data_byte)[2:].zfill(8)
        decrypted_img_bits += data_bits

    # bits to np format
    decrypted_img_bits_np = np.array([int(bit) for bit in decrypted_img_bits])
    decrypted_img_bits_np = decrypted_img_bits_np.reshape((CROP_HEIGHT, CROP_WIDTH))
    decrypted_crop_imgs.append(decrypted_img_bits_np.tolist())



# Combine crop images
decrypted_crop_imgs = np.array(decrypted_crop_imgs)
decrypted_img = combine_image(decrypted_crop_imgs, img_width, img_height)

# np to PIL
decrypted_image = Image.fromarray(decrypted_img*255)
decrypted_image.show()
decrypted_image.convert('RGB').save('decrypted_img.jpg')