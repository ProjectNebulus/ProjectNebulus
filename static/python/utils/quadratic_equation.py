import math
def solveequation(a, b, c):
  try:
    return [(-b+math.sqrt(b**2-4*a*c))/(2*b),(-b-math.sqrt(b**2-4*a*c))/(2*b)]
  except:
    return ["No Real Solution"]

equation = "x^2+6x+5"
print("Quadratic Formula method")
sections = equation.split("+")
