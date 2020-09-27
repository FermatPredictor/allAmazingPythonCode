import math
from _basic_math import euler_phi


def towerLargerThan(base, h, m):
    """
    return base**base**...**base>= m
    idea: 用對數ln化簡
    """
    if m<=0:
        return True
    if h==1:
        return base>=m
    return towerLargerThan(base,h-1, math.log(m)/math.log(base))

def tower(base, h, m):
    """
    題源: https://www.codewars.com/kata/5a08b22b32b8b96f4700001c/train/python
    Return base ** base ** ... ** base, where the height is h, modulo m.
    
    核心想法:
    base 次方的循環節大致上是phi(m)，
    遞迴關係大致是 pow(base, tower(base, h-1, euler_phi(m)), m)
    
    若base, m互質的話一定是(且循環節一定是1結尾, by Euler theorem)，
    若不互質的情況大部分的狀況循環節也是phi(m)，
    如:
    3的次方(mod 15): [3, 9, 12, 6, 3, 9, 12, 6, ...]
    4的次方(mod 10): [4, 6, 4, 6, ...]
    
    但有時有點誤差，
    例如3的次方(mod 9): [3, 0, 0, 0, ...]
    34的次方(mod 40): [34,36,24,16,24,16,...] (此組有點特別)
    如果直接遞迴的話，變成算 34**34 = 34 ** (34%16) = 36 (mod 40)，
    然而34**34應該是16而不是36
    
    但是只要超過phi(m)的部分保證循環，
    所以tower(base, h)對phi(m)取餘數的話，
    如果原本tower(base, h)大於phi(m)的話，不要降到phi(m)以下
    
    example:    
    >>> tower(34,2,40)
    16
    >>> tower(4,3,10)
    6
    >>> tower(3,2,243)
    27
    >>> tower(2,4,131072)
    65536
    """
    if m == 1:
        return 0
    if base == 1 or h==0:
        return 1
    if h==1:
        return base % m
    phi = euler_phi(m)
    power = tower(base, h-1, phi)
    flag = towerLargerThan(base, h-1, phi)
    return pow(base, power+ phi*flag, m)

def zero_tower_judge(bases):
    """
    (判斷次方塔的值是0，1或非零、一，處理CodeWar上次方塔有0的corner case)
    Let bases = [b1, b2,...,bn]= b1**b2**...**bn，
    define corner case 0**0 =1,
    if bases is 0 then return 0,
    if bases is 1 then return 1,
    return -1 else
    """
    assert bases, "bases can not be empty list"
    if bases[0]!=0:
        return 1 if bases[0]==1 else -1
    if len(bases)==1:
        return 0
    power = zero_tower_judge(bases[1:])
    return 1 if power==0 else 0
    

def general_towerLargerThan(bases, m):
    """
    Let bases = [b1, b2,...,bn]= b1**b2**...**bn，
    return bases>= m
    idea: 用對數ln化簡
    """
    if m<=0:
        return True
    if bases[0] in [0,1]:
        return False
    if len(bases) == 1 or bases[0]==1:
        return bases[0]>=m
    return general_towerLargerThan(bases[1:],math.log(m)/math.log(bases[0]))

def general_tower(bases, m):
    """
    題源: https://www.codewars.com/kata/last-digit-of-a-huge-number/train/python
    Let bases = [b1, b2,...,bn]= b1**b2**...**bn，
    計算[b1, b2,...,bn]%m的值
    
    >>> general_tower([3,8],10)
    1
    """
    if not bases:
        return 1
    if m == 1:
        return 0
    if len(bases) == 1:
        return bases[0]%m
    if bases[0]==0:
        return zero_tower_judge(bases)
    phi = euler_phi(m)
    power = general_tower(bases[1:], phi)
    flag = general_towerLargerThan(bases[1:],phi)
    return pow(bases[0], power+ phi*flag, m)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
