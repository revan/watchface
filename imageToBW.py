#!/bin/python
from PIL import Image, ImageOps

def imageToBW(path):
    size = (148, 168)

    image_file = Image.open(path)

    image_file = ImageOps.fit(image_file, size, Image.ANTIALIAS)

    image_file = image_file.convert('1') # convert image to black and white

    image_file = image_file.transpose(Image.FLIP_LEFT_RIGHT)

    path = path + '.png'
    image_file.save(path)

    return path
