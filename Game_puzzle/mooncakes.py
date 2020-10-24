"""
從數歸法來的月餅問題。
買n個月餅的價錢為不斷將它分堆直到一堆一個，
每次分兩堆的月餅數量乘積會加到總價中。
(公式: 買n個月餅的價錢為1+2+…+n)
"""

import random

def divMoonCakes(n):
    mooncakes = [n]
    money = 0
    while mooncakes:
        m = random.choice(mooncakes)
        mooncakes.remove(m)
        div = random.randint(1,m-1)
        print(f"取出{m}個月餅，把它分成{div}和{m-div}兩堆，總共增加{div*(m-div)}元")
        money += div*(m-div)
        print(f"目前月餅小計 {money} 元")
        if div!=1:
            mooncakes.append(div)
        if m-div!=1:
            mooncakes.append(m-div)
        print("目前待分月餅堆: ", mooncakes)
    return money

divMoonCakes(8)
