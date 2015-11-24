from PIL import Image


def load_target(filename):
    img = Image.open(filename)
    return img


def load_key():
    key = Image.open('key.png')
    return key


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


def auth(img,  key):
    w,  h = img.size
    w_k,  h_k = key.size
    offset_x,  offset_y = (int(w/2 - w_k/2),  int(h/2 - h_k/2))
    wtm = Image.new('1',  (w, h))

    resized_key = Image.new("1",  (w, h))
    for y in range(h_k):
        for x in range(w_k):
            v = key.getpixel((x, y))
            if v > 127:
                v = 1
            else:
                v = 0
            resized_key.putpixel((x+offset_x, y+offset_y), v)

    for y in range(h):
        for x in range(w):
            r,  g,  b = img.getpixel((x, y))
            v_img = 0
            if b % 2 == 1:
                v_img = 1
            v_k = resized_key.getpixel((x, y))
            v = xor(v_img,  v_k)
            wtm.putpixel((x, y), v)

    wtm.save('watermark.png')
    return wtm


def main():
    img = load_target('watermarked.png')
    key = load_key()

    wtm = auth(img,  key)

main()
