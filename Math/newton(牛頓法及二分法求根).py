# -*- coding: utf-8 -*-
"""
這邊利用牛頓法求連續函數f(x)=0的根，
每次做x=x-f(x)/f'(x)的迭代，
再檢查新的f(x)是否足夠接近0。
"""

# 微分，f'(x)，當前需手算
def diff(x):
    return (1-x**2)/(1-x)**4

# y=f(x)
def f(x):
    return x/(1-x)**2 - 8

"""
函數功能:
 用牛頓法求解 f(x)的零根
 ini_val 表示預設的初始值
 err 是預設容許誤差
 maxiter 是預設最大迭代次數(避免程式一直跑停不下來)
 prt_step用來debug，若prt_step設為True, 印出每次迭代後的數值
 結束條件為解足夠靠近0
"""
def Newton(f,diff, ini_val = 1, err=10**-13, maxiter = 100, prt_step = False):
    x = ini_val 
    for i in range(maxiter):
        x -= f(x)/diff(x)    
        if prt_step == True:
            print(f"After {i+1} iteration, the solution is updated to {x}, f(x) is {f(x)}")
        if abs(f(x))<err:
            break
    return x

"""
函數功能:
 用二分法求解 f(x)的零根，
 初始條件需滿足f(left)f(right)<0，
 err 是預設容許誤差
 maxiter 是預設最大迭代次數(避免程式一直跑停不下來)
 prt_step用來debug，若prt_step設為True, 印出每次迭代後的數值.
 結束條件為解足夠靠近0
"""
def Binary(f, left, right,err=10**-13, maxiter = 100, prt_step = False):
    for i in range(maxiter):
        middle = (left+right)/2
        if prt_step == True:
            print(f"After {i+1} iteration, the solution is updated to {middle}, f(x) is {f(middle)}")
        if abs(f(middle))<err:
            break
        if f(left)*f(middle)<=0:
            right=middle
        else:
            left=middle
    return middle

print(Binary(f, 0, 1- 10 ** -11))
print(Newton(f,diff,0.7))
