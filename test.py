# -*- coding: utf-8 -*-
from PIL import Image


def get_target_size(img_size, size, exact_size=False):
    assert img_size[0] and img_size[1]
    assert size[0] or size[1]

    size = list(size)
    if not size[0]:
        size[0] = size[1] * img_size[0] // img_size[1]
    if not size[1]:
        size[1] = size[0] * img_size[1] // img_size[0]

    if not exact_size:
        return min(img_size[0], size[0]), min(img_size[1], size[1])
    else:
        return tuple(size)


def crop_by_aspect_ratio(image, aspect_ratio):
    """crop image by scale without aspect ratio distortion

    :param image: a PIL image object
    :param aspect_ratio: aspect ratio,  as a 2-tuple: (width, height).
    :returns: An :py:class:`~PIL.Image.Image` object.
    """
    size = image.size
    size1 = (size[0], size[0] * aspect_ratio[1] // aspect_ratio[0])
    size2 = (size[1] * aspect_ratio[0] // aspect_ratio[1], size[1])
    new_size = min(size1, size2)

    if new_size == image.size:
        return image

    # calc left, upper, right, lower
    left = (size[0] - new_size[0]) // 2
    right = left + new_size[0]
    upper = (size[1] - new_size[1]) // 2
    lower = upper + new_size[1]

    return image.crop((left, upper, right, lower))


def crop_resize(image, size, exact_size=False):
    """

    :param image: a PIL image object
    :param size: a 2-tuple of (width,height);  at least one must be specified
    :param exact_size: whether to scale up for smaller images.
        Defaults to ``False``.
    :return: An :py:class:`~PIL.Image.Image` object.
    """
    target_size = get_target_size(image.size, size, exact_size)
    img2 = crop_by_aspect_ratio(image, target_size[0], target_size[1])
    return img2.resize(target_size, Image.ANTIALIAS)


def test():
    img = Image.open('img.png')
    size = (255, 255)
    exact_size = False
    img3 = crop_resize(img, size, exact_size)
    img3.save('img4.png', 'PNG')


if __name__ == '__main__':
    test()

