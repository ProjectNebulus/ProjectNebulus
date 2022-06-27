import math


def triangle_area(a, b, c):
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def rectangle_area(a, b):
    return a * b


def circle_area(a):
    return math.pi * a**2


def pentagon_area(a):
    return (3 * math.sqrt(3) / 2) * a**2


def hexagon_area(a):
    return (2 * math.sqrt(3) * a**2) / 2


def octagon_area(a):
    return 2 * math.sqrt(2) * a**2


def square(a):
    return a**2
