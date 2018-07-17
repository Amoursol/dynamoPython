"""
ASSIGNMENT OPERATORS
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# Default values
num01 = 10
num02 = 5

plusEquals = num01 + num02 # Simple addition (10 + 5)
plusEquals += num01 # The positive assignment operator will take the right operand (num01) and add this to the left operand (plusEquals) before assingning the result back to the left operand (plusEquals): e.g original plusEquals (10+5) + num01(10) = 25 --> plusEquals == 25

subtractEquals = num01 + num02 # Simple addition (10 + 5)
subtractEquals -= num02 # The negative assignment operator will take the right operand (num02) and subtract this from the left operand (subtractEquals) before assingning the result back to the left operand (subtractEquals): e.g original subtractEquals (10+5) - num02(5) = 10 --> subtractEquals == 10

multiplyEquals = num01 + num02 # Simple addition (10 + 5)
multiplyEquals *= num01 # The multiplication assignment operator will take the right operand (num01) and multiply this to the left operand (multiplyEquals) before assingning the result back to the left operand (multiplyEquals): e.g original multiplyEquals (10+5) * num01(10) = 150 --> multiplyEquals == 150

divideEquals = num01 + num02 # Simple addition (10 + 5)
divideEquals /= num02 # The division assignment operator will take the right operand (num02) and divide this to the left operand (divideEquals) before assingning the result back to the left operand (divideEquals): e.g original divideEquals (10+5) / num02(5) = 3 --> multiplyEquals == 3

modulusEquals = num01 + num02 # Simple addition (10 + 5)
modulusEquals %= num01 # The modulus assignment operator will take the right operand (num01) and take the remainder of this to the left operand (modulusEquals) before assingning the result back to the left operand (modulusEquals): e.g original modulusEquals (10+5) % num01(10) = 5 --> modulusEquals == 5

exponentEquals = num01 + num02 # Simple addition (10 + 5)
exponentEquals **= num02 # The exponent assignment operator will take the right operand (num02) and take the exponent of this to the left operand (exponentEquals) before assingning the result back to the left operand (exponentEquals): e.g original exponentEquals (10+5) ** num02(5) = 759375 --> modulusEquals == 759375

floorDivisionEquals = num01 + num02 # Simple addition (10 + 5)
floorDivisionEquals //= num02 # The floor division assignment operator will take the right operand (num02) and take the floor division of this to the left operand (floorDivisionEquals) before assingning the result back to the left operand (floorDivisionEquals): e.g original floorDivisionEquals (10+5) // num02(5) = 3 --> modulusEquals == 3

OUT = plusEquals, subtractEquals, multiplyEquals, divideEquals, modulusEquals, exponentEquals, floorDivisionEquals