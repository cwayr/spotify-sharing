'''Basic test to ensure Travis CI build passes'''

import pytest

def addition(x, y):
    return x + y

def test_addition():
    assert addition(2, 2) == 4