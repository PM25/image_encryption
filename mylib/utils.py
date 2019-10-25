import math
import numpy as np
from PIL import Image

CROP_WIDTH = 16
CROP_HEIGHT = 8


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


def expand_white_bg(image, crop_width, crop_height):
    img_width, img_height = image.size
    if(img_width % crop_width == 0 and img_height % crop_height == 0):
        return image
    else:    
        new_width = img_width + (CROP_WIDTH - img_width % CROP_WIDTH)
        new_height = img_height + (CROP_HEIGHT - img_height % CROP_HEIGHT)
        bg_size = (new_width, new_height)
        new_img = Image.new('RGB', bg_size, (255,255,255))
        new_img.paste(image, (0, 0))
        return new_img.convert('1')