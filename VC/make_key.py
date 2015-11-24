from PIL import Image
import random


def generate_key():
    key_img = Image.new('1', (152, 10), 1)
    for y in range(10):
        for x in range(152):
            v = random.randint(0, 1)
            key_img.putpixel((x, y), v)

    key_img.save('key.png')

generate_key()
