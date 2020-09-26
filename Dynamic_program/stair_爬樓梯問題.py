def stair(n, X):
    """
    函數功能: 經典爬樓梯問題。
    n表示有n階階梯，
    X集合表示每次可以爬的階梯數量(都是正整數)，
    求從第0階開始爬至第n階有幾種爬法?
    example:
    >>> stair(5,{1,3})
    4
    >>> stair(6,{1,3})
    6
    >>> stair(2,{1,2})
    2
    >>> stair(6,{1,2})
    13
    >>> stair(6,{1})
    1
    """
    ways = [1]+ [0]* n
    for i in range(1,n+1):
        ways[i]= sum(ways[i-x] for x in set(X) if i-x>=0)
    return ways[-1]



if __name__ == "__main__":
    import doctest
    doctest.testmod()