import random

def power_mod(b, e, m):
    res, b = 1, b % m
    while e > 0:
        if e & 1: res = res * b % m
        e >>= 1
        b = b * b % m
    return res

if __name__ == "__main__":
    # random test
    for i in range(1000):
        b = random.randint(1,1000)
        e = random.randint(1,1000000)
        m = random.randint(1,10000)
        assert power_mod(b, e, m) == pow(b,e,m)