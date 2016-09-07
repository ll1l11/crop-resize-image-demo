# -*- coding: utf-8 -*-
from PIL import Image


def calc_final_size(image_size, size, exact_size=False):
    """calc final image size"""
    assert image_size[0] and image_size[1]
    assert size[0] or size[1]

    # calc by formula:
    # image_size[0] / image_size[1] == size[0] / size[1]
    # =>
    # image_size[0] * size[1] == height * siez[0]
    if size[0]:
        target_height = size[0] * image_size[1] // image_size[0]
        target_height = min(target_height, size[1])
    else:
        target_height = size[1]

    if size[1]:
        target_width = size[1] * image_size[0] // image_size[1]
        target_width = min(target_width, size[0])
    else:
        target_width = size[0]

    target_size = (target_width, target_height)
    if image_size < target_size and not exact_size:
        return image_size
    else:
        return target_size


def crop_by_scale(img, weight, height):
    size = img.size
    size1 = (size[0], size[1] * weight // height)
    size2 = (size[0] * height // weight, size[1])
    new_size = min(size1, size2)

    if new_size == img.size:
        return img

    # calc left, upper, right, lower
    left = (size[0] - new_size[0]) // 2
    right = left + new_size[0]
    upper = (size[1] - new_size[1]) // 2
    lower = upper + new_size[1]

    return img.crop((left, upper, right,  lower))


def resize_crop(img, weight, height, force=False):
    assert weight or height
    size = img.size
    if not weight:
        weight = (height * size[0] // size[1])

    if not height:
        height = (weight * size[1] // size[0])

    # calc size by weight
    size1 = (weight, weight * size[1] // size[0])

    # calc size by height
    size2 = (height * size[0] // size[1], height)

    new_size = max(size1, size2)
    img2 = img.resize(new_size)

    if (not force and new_size > size) or new_size == (weight, height):
        return img
    # calc left, upper, right, lower
    left = (new_size[0] - weight) // 2
    right = left + weight
    upper = (new_size[1] - height) // 2
    lower = upper + height

    return img2.crop((left, upper, right,  lower))


def crop_resize(img, width, height):
    assert width or height
    size = img.size
    # calc by formula:
    # weight / height == size[0] / size[1]
    # =>
    # weight * size[1] == height * siez[0]
    if not width:
        weight = (height * size[0] // size[1])

    if not height:
        height = (weight * size[1] // size[0])

    # calc size by img.weight
    size1 = (size[0], size[0] * height // size[1])

    # calc size by height
    size2 = (size[1] * height // size[0], size[1])

    new_size = max(size1, size2)
    img2 = img.resize(new_size)

    force = False
    if (not force and new_size > size) or new_size == (weight, height):
        return img

    return crop_by_scale(img2, weight, height)


def test():
    img = Image.open('wanzi.jpg')
    # weight = 200
    # height = 200
    # img = resize_crop(img, weight, height)
    # print('result: ', img.size)

    img2 = crop_by_scale(img, 1, 1)

    img2.save('img2.jpg')


if __name__ == '__main__':
    test()
