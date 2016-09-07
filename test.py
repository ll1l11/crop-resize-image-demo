# -*- coding: utf-8 -*-
from PIL import Image


def calc_target_size(size, max_width, max_height, exact_size=False):
    """calc target_size image size"""
    assert size[0] and size[1]
    assert max_width or max_height

    # calc by formula:
    # x / y == m / n
    # =>
    # x * n == y * m
    if max_width:
        target_height = max_width * size[1] // size[0]
        if max_height:
            target_height = min(target_height, max_height)
    else:
        target_height = max_height

    if max_height:
        target_width = max_height * size[0] // size[1]
        if max_width:
            target_width = min(target_width, max_width)
    else:
        target_width = max_width

    target_size = (target_width, target_height)
    if size < target_size and not exact_size:
        return size
    else:
        return target_size


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


def crop_resize(img, max_width, max_height):
    # resize
    target_size = calc_target_size(img.size, max_width, max_height)
    img2 = crop_by_scale(img, target_size[0], target_size[1])
    return img2.resize(target_size)


def resize_crop(img, max_width, max_height):
    target_size = calc_target_size(img.size, max_width, max_height)
    size1 = (target_size[0], target_size[0] * img.size[1] // img.size[0])
    size2 = (target_size[1] * img.size[0] // img.size[1], target_size[1])
    print(size1, size2)
    img2 = img.resize(max(size1, size2))
    print('缩放后图片大小', img2.size)
    return crop_by_scale(img2, target_size[0], target_size[1])


def test():
    img = Image.open('wanzi.jpg')
    print('原图片大小:', img.size)

    # width = 200
    # height = 200
    max_width = 100
    max_height = 100
    target_size = calc_target_size(img.size, max_width, max_height)
    print('生成的图片大小: ', target_size)
    img2 = resize_crop(img, max_width, max_height)
    img3 = crop_resize(img, max_width, max_height)
    # print('result: ', img.size)

    # img2 = crop_by_scale(img, 1, 1)

    img2.save('img2.jpg')
    img3.save('img3.jpg')


if __name__ == '__main__':
    test()
