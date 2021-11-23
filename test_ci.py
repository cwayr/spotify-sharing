'''Basic test to ensure CI build passes'''

def increment(x):
    return x + 1

def test_answer():
    assert increment(3) == 4