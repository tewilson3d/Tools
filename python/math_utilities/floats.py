EPSILON = 0.00000001

def floatEqual(floatA, floatB):
    '''Function to determine if the given two floats are equal.'''
    return abs(floatA - floatB) < EPSILON
