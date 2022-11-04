import sympy
from sympy import symbols, expand, factor

x, y = symbols('x y')
expr = x + 2*y

expr + 1

expr - x

expanded_expr = expand(x*expr)
expanded_expr


