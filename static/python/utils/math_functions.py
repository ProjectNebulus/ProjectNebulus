import math


def pythagorean(a, b):
    return math.sqrt(a**2 + b**2)


def midpoint_formula(x1, y1, x2, y2):
    return [(x1 + x2) / 2, (y1 + y2) / 2]


def slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)


def cube_volume(x):
    return x**3


def overlap(a, b):
    return [max(a[0], b[0]), min(a[1], b[1])]


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def absolute_value(a):
    return abs(a)


def factorial(a):
    if a < 0:
        return False
    if a == 0:
        return 1
    num = 1
    for i in range(2, a):
        num *= i
    return num


def choose(a, b):
    # a choose b
    if a < b:
        return False
    return factorial(a) / (factorial(b) * factorial(a - b))


def square(a):
    return a**2


def exponent(a, b):
    return a**b


def square_root(a):
    return math.sqrt(a)


def cube_root(a):
    if a < 0:
        a = abs(a)
        cube_root = a ** (1 / 3) * (-1)
    else:
        cube_root = a ** (1 / 3)
    return cube_root


def root(a, b):
    # b√a
    if a < 0:
        a = abs(a)
        cube_root = a ** (1 / b) * (-1)
    else:
        cube_root = a ** (1 / b)
    return cube_root


def pi():
    return math.pi


def e():
    return math.e


def complex(real, imaginary):
    return complex(real, imaginary)


def graphingCalculator(equations):
    # powered by desmos
    string = """
  <script src="https://www.desmos.com/api/v1.6/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"></script>
<div id="calculator" style="width: 600px; height: 400px;"></div>

<script>
  var elt = document.getElementById('calculator');
  var calculator = Desmos.GraphingCalculator(elt);"""
    for i in range(0, len(equations)):
        string += (
            "calculator.setExpression({ id: 'graph"
            + str(i)
            + "', latex: '"
            + equations[i]
            + "' });"
        )
    string += """</script>
  """
    return string


def ln(a):
    return math.log(a)


def log(a):
    return math.log(a, 10)


def log_base(a, base):
    return math.log(a, base)
