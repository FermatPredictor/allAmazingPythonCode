from itertools import count

def isPrime(n):
    """
    函數功能: 判斷一個整數是不是質數
    example:
    >>> isPrime(0)
    False
    >>> isPrime(1)
    False
    >>> isPrime(2)
    True
    >>> isPrime(97)
    True
    >>> isPrime(121)
    False
    """
    return n==2 or (n > 2 and n%2 and all(n%x for x in range(3,int(n**.5)+1,2)))


def nextPrime(n):
    """
    函數功能: 找n的下一個質數是誰，
    count是無窮迭代器，從n+1開始一直往後生成{n+1, n+2, n+3,...}
    example:
    >>> nextPrime(15)
    17
    >>> nextPrime(2)
    3
    """
    return next(x for x in count(n+1) if isPrime(x))

if __name__ == "__main__":
    import doctest
    doctest.testmod()