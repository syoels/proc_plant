import math


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


def angle_vect2d(vect_2d_xz):
    """
    :param vect_2d_xz: 2d vector [x, z]
    :return: angles in degrees to orient outwards
    """
    x = vect_2d_xz[0]
    z = vect_2d_xz[1]
    return math.degrees(math.atan2(x, z))
