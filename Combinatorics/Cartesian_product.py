def cart_prod(*sets):
    res = {()}
    for arg in sets:
        res = {e + (s,) for e in res for s in arg}
    return res
    
A = {1}
B = {1, 2}
C = {1, 2, 3}
print(cart_prod(A, B, C))
