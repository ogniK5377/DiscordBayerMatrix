# -*- coding: utf-8 -*-
from PIL import Image
import math
import sys

# Py2 support
if (sys.version_info < (3, 0)):
    # In python 2, chr only accepts a range 0->256
    chr = unichr

# https://gamedev.stackexchange.com/a/148980
# https://en.wikipedia.org/wiki/Ordered_dithering
def bit_reverse(x, n):
    return int(bin(x)[2:].zfill(n)[::-1], 2)

def bit_interleave(x, y, n):
    x = bin(x)[2:].zfill(n)
    y = bin(y)[2:].zfill(n)
    return int(''.join(''.join(i) for i in zip(x, y)), 2)

def bayer_entry(x, y, n):
    return bit_reverse(bit_interleave(x ^ y, y, n), 2*n)

def bayer_matrix(n):
    r = range(2**n)
    return [[bayer_entry(x, y, n) for x in r] for y in r]

def build_braille(tbl):
    # https://en.wikipedia.org/wiki/Braille_Patterns#Identifying,_naming_and_ordering
    code = 0x2800
    code += (tbl[0][0] * 0x1)
    code += (tbl[0][1] * 0x8)
    code += (tbl[1][0] * 0x2)
    code += (tbl[1][1] * 0x10)
    code += (tbl[2][0] * 0x4)
    code += (tbl[2][1] * 0x20)
    code += (tbl[3][0] * 0x40)
    code += (tbl[3][1] * 0x80)
    return code

def main(argc, argv):
    if argc < 4:
        print('{} <input> <output> <matrix size>'.format(
            argv[0]
        ))
        return 1
    
    # Calculate the levels step
    MatrixSize = int(argv[3])
    MatrixDim = 2**MatrixSize
    StepCount = MatrixDim*MatrixDim

    # Levels are from 0->255, round up to 256 since our matrix size is to the power of 2
    Step = 256 / StepCount

    # Calulate the bayer matrix
    BAYER = bayer_matrix(MatrixSize)

    # Update the matrix with our step to get an absolute level maximum
    for y in range(len(BAYER)):
        for x in range(len(BAYER[y])):
            BAYER[y][x] = math.floor(BAYER[y][x] * Step)
    
    im = Image.open(argv[1]).convert('L') # Open our image and make it gray scale
    pixels = im.load()

    # https://en.wikipedia.org/wiki/Ordered_dithering
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            # Find element in our matrix
            b = BAYER[y % len(BAYER)][x % len(BAYER[0])]
            # Check the threshold
            if pixels[x,y] > b:
                pixels[x,y] = 255
            else:
                pixels[x,y] = 0
    im.save('{}.dithered.png'.format(argv[1]))

    # Move through the size of our braille characters 2x4
    grid_w = int(math.floor(im.size[0] / 2))
    grid_h = int(math.floor(im.size[1] / 4))

    with open(argv[2], 'wb') as fp:
        # Loop over by braille cell size
        for y in range(grid_h):
            for x in range(grid_w):
                # Get the top left cell location
                bx = 2 * x
                by = 4 * y

                # Cell format
                # 1 = On, 0 = Off
                cell_tbl = [
                    [int(pixels[bx, by] / 255), int(pixels[bx+1, by] / 255)],
                    [int(pixels[bx, by+1] / 255), int(pixels[bx+1, by+1] / 255)],
                    [int(pixels[bx, by+2] / 255), int(pixels[bx+1, by+2] / 255)],
                    [int(pixels[bx, by+3] / 255), int(pixels[bx+1, by+3] / 255)],
                ]
                # Calculate our Braille character
                fp.write(
                    chr(build_braille(
                        cell_tbl
                    )).encode('utf-8')
                )
            # Head over to the next line
            fp.write(b'\n')
    # character count is (grid width * grid height) for each braille character
    # we add grid_h to count the new lines we added
    print('Done! Cell size is {}x{} and is {} characters!'.format(grid_w, grid_h, (grid_w*grid_h) + grid_h))
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
