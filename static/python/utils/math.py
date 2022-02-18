import math
def pythagorean(a, b):
  return math.sqrt(a**2+b**2)

def midpoint_formula(x1, y1, x2, y2):
  return [(x1+x2)/2, (y1+y2)/2]

def slope(x1, y1, x2, y2):
  return (y2-y1)/(x2-x1)

def cube_volume(x):
  return x**3

def overlap(a, b):
  return ([max(a[0], b[0]), min(a[1], b[1])])