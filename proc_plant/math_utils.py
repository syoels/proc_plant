import numpy as np


def mapFromTo(x, a, b, c, d):
    """
    map between ranges
    :param x: number to map
    :param a: from range start
    :param b: from range end
    :param c: to range start
    :param d: to range end
    :return: relative pos of x in [a,b] stretched and moved to fit [c,d]
    """
    y = (x - a) / float((b - a)) * (d - c) + c
    return y


def angle(b, c, z):
    """
    https://stackoverflow.com/questions/62016425/how-to-calculate-the-rotation-angles-needed-on-x-and-z-to-align-two-vectors
    :return: angle to vector
    """
    return np.arccos(z / np.sqrt(b ** 2 + c ** 2)) - np.arctan2(-b, c)