import argparse
import numpy as np
from PIL import Image

# Arguments
parser = argparse.ArgumentParser(description="Image Encryption")
parser.add_argument("--file", "-f", type=str, default="default.jpg", help="Path to image file.")
parser.add_argument("--save", "-s", type=str, default="bits_count.txt", help="Path to save the results.")
args = parser.parse_args()



# Counting how many white bits in an image
if __name__ == '__main__':
    # Load image
    image = Image.open(args.file)
    image = image.convert('1')
    image_np = np.array(image)

    # Count white and black bits
    white_count = np.sum(image_np)
    black_count = np.sum(image_np == False)

    # Show and Save results
    print(f"White bits count: {white_count}")
    print(f"Black bits count: {black_count}")
    print(f"Total bits count: {white_count + black_count}")
    with open(args.save, 'w') as out_file:
        out_file.write(f"White bits count: {white_count}\n")
        out_file.write(f"Black bits count: {black_count}\n")
        out_file.write(f"Total bits count: {white_count + black_count}")