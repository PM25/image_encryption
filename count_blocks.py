from mylib import utils

import argparse
import numpy as np
from PIL import Image

# Arguments
parser = argparse.ArgumentParser(description="Image Encryption")
parser.add_argument("--file", "-f", type=str, default="default.jpg", help="Path to image file.")
parser.add_argument("--save", "-s", type=str, default="blocks_count.txt", help="Path to save the results.")
args = parser.parse_args()

CROP_WIDTH = 16
CROP_HEIGHT = 8



# Start from here
if __name__ == '__main__':
    # Load image
    image = Image.open(args.file)
    image = image.convert('1')

    image = utils.expand_white_bg(image, CROP_WIDTH, CROP_HEIGHT)

    white_blocks_count = 0
    black_blocks_count = 0

    for crop_img in utils.split_image(image, CROP_HEIGHT, CROP_WIDTH):
        img_np = np.array(crop_img).flatten()

        # Check if the cropped image is consist with all white
        if(np.all(img_np == True) == True):
            white_blocks_count += 1
        else:
            black_blocks_count += 1

    # Show and Save results
    print(f"White blocks count: {white_blocks_count}")
    print(f"Black blocks count: {black_blocks_count}")
    print(f"Total blocks count: {white_blocks_count + black_blocks_count}")
    with open(args.save, 'w') as out_file:
        out_file.write(f"White blocks count: {white_blocks_count}\n")
        out_file.write(f"Black blocks count: {black_blocks_count}\n")
        out_file.write(f"Total blocks count: {white_blocks_count + black_blocks_count}")