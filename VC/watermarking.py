from PIL import Image
from time import strftime
import random


def load_numbers():
    numbers = []
    img = Image.open('number.png')
    for i in range(12):
        num = Image.new('1',  (8, 10),  1)  # binary,  8x10,  all white
        numbers.append(num)

    for y in range(10):
        for x in range(8):
            for i in range(12):
                r,  g,  b = img.getpixel((x+8*i, y))
                v = (r+g+b)/3
                if v > 200:
                    v = 1
                else:
                    v = 0
                numbers[i].putpixel((x, y), v)

    return numbers


def load_key():
    key = Image.open('key.png')
    return key


def timestamp(numbers):
    t = strftime("%Y-%m-%d %H:%M:%S")
    secret = Image.new("1",  (8 * len(t),  10),  1)
    for i in range(len(t)):
        offset = -1
        if t[i] == '0':
            offset = 0
        elif t[i] == '1':
            offset = 1
        elif t[i] == '2':
            offset = 2
        elif t[i] == '3':
            offset = 3
        elif t[i] == '4':
            offset = 4
        elif t[i] == '5':
            offset = 5
        elif t[i] == '6':
            offset = 6
        elif t[i] == '7':
            offset = 7
        elif t[i] == '8':
            offset = 8
        elif t[i] == '9':
            offset = 9
        elif t[i] == ':':
            offset = 10
        elif t[i] == '-':
            offset = 11
        else:
            offset = -1

        if offset < 0:
            continue
        for y in range(10):
            for x in range(8):
                v = numbers[offset].getpixel((x, y))
                secret.putpixel((x+i*8, y), v)
    secret.save('timestamp.png')
    return secret


def xor(x,  y):
    if x == 0 and y == 0:
        return 0
    elif x == 0 and y == 1:
        return 1
    elif x == 1 and y == 0:
        return 1
    elif x == 1 and y == 1:
        return 0
    else:
        return (x + y) % 2


def distribution(secret,  key):
    w,  h = secret.size
    share = Image.new("1",  (w, h),  1)
    for y in range(h):
        for x in range(w):
            s = secret.getpixel((x, y))
            k = key.getpixel((x, y))
            if k > 127:
                k = 1
            else:
                k = 0
            share.putpixel((x, y), xor(s, k))
    share.save('share.png')
    return share


def reconstruction(share,  key):
    w,  h = share.size
    reconst = Image.new("1",  (w, h),  1)
    for y in range(h):
        for x in range(w):
            s = share.getpixel((x, y))
            k = key.getpixel((x, y))
            if k > 127:
                k = 1
            else:
                k = 0
            reconst.putpixel((x, y), xor(s, k))
    reconst.save('reconstructed_timestamp.png')
    return reconst


def load_signature(filename):
    sign = Image.open(filename)
    sign = sign.convert("RGB")
    return sign


def watermark(sign,  share):
    w,  h = sign.size
    w_s,  h_s = share.size
    offset_x,  offset_y = (int(w/2 - w_s/2),  int(h/2 - h_s/2))
    wtm_sign = Image.new("RGB",  (w, h))

    resized_share = Image.new("1",  (w, h))
    for y in range(h):
        for x in range(w):
            v = random.randint(0, 1)
            resized_share.putpixel((x, y), v)
    for y in range(h_s):
        for x in range(w_s):
            v = share.getpixel((x, y))
            resized_share.putpixel((x+offset_x, y+offset_y), v)

    for y in range(h):
        for x in range(w):
            r,  g,  b = sign.getpixel((x, y))
            if b % 2 == 1:
                b -= 1
            b += resized_share.getpixel((x, y))
            wtm_sign.putpixel((x, y), (r, g, b))
    wtm_sign.save('watermarked.png')
    return wtm_sign


def main():
    # Generate Timestamp & (2, 2) Scheme using XOR
    numbers = load_numbers()
    key = load_key()
    secret = timestamp(numbers)
    share = distribution(secret,  key)
    reconst = reconstruction(share,  key)

    # Watermarking
    sign = load_signature('kaist.gif')
    wtm_sign = watermark(sign,  share)

main()
