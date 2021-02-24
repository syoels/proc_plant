
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
