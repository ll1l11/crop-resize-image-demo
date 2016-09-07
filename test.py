# -*- coding: utf-8 -*-
from PIL import Image


def get_target_size(img_size, size, exact_size=False):
    """get target image size"""
    assert img_size[0] and img_size[1]
    assert size[0] or size[1]

    # calc by formula:
    # x / y == m / n
    # =>
    # x * n == y * m
    size = list(size)
    if not size[0]:
        size[0] = size[1] * img_size[0] // img_size[1]
    if not size[1]:
        size[1] = size[0] * img_size[1] // img_size[0]

    if not exact_size:
        return min(img_size[0], size[0]), min(img_size[1], size[1])
    else:
        return tuple(size)


def crop_by_scale(img, width, height):
    size = img.size
    size1 = (size[0], size[0] * height // width)
    size2 = (size[1] * width // height, size[1])
    new_size = min(size1, size2)
    print('按照比例剪裁', new_size)

    if new_size == img.size:
        return img

    # calc left, upper, right, lower
    left = (size[0] - new_size[0]) // 2
    right = left + new_size[0]
    upper = (size[1] - new_size[1]) // 2
    lower = upper + new_size[1]

    return img.crop((left, upper, right,  lower))


def crop_resize(img, size, exact_size=False):
    # resize
    target_size = get_target_size(img.size, size, exact_size)
    print('生成的图片大小: ', target_size)
    img2 = crop_by_scale(img, target_size[0], target_size[1])
    return img2.resize(target_size, Image.ANTIALIAS)


# def resize_crop(img, max_width, max_height):
#     target_size = calc_target_size(img.size, max_width, max_height)
#     size1 = (target_size[0], target_size[0] * img.size[1] // img.size[0])
#     size2 = (target_size[1] * img.size[0] // img.size[1], target_size[1])
#     print(size1, size2)
#     img2 = img.resize(max(size1, size2))
#     print('缩放后图片大小', img2.size)
#     return crop_by_scale(img2, target_size[0], target_size[1])


def test():
    img = Image.open('chang.png')
    # img = Image.open('/Users/xyz/Downloads/3.jpg')
    print('原图片大小:', img.size)

    # width = 200
    # height = 200
    size = (255, 255)
    exact_size = False
    img3 = crop_resize(img, size, exact_size)
    img3.save('img4.png', 'PNG')


if __name__ == '__main__':
    test()
