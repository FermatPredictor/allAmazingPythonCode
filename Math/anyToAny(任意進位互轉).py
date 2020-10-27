"""
<第一部分> 任意進位的互轉(包括負數進位)
我們實作兩個函數:
1. decToAny(num, base) 表示把十進位數字轉換成任何進位(包括負數進位)
2. anyToDec(numList, base) 表示把任何進位轉換成十進位數字(包括負數進位)
其它進位的數字以一個list的形式表示它，
例如負二進位的[1,1,1,1,1]代表的是
(-2)^4+(-2)^3+(-2)^2+(-2)^1+(-2)^0=11

負進位的介紹
https://en.wikipedia.org/wiki/Negative_base
"""


def decToAny(num, base):
    assert base not in {-1,0,1}, "Base must greater than 1 or less than -1."
    assert  num>=0 or base<=-2, "無法將負數轉正數進位"
    digits = [0] if num == 0 else []
    while num != 0:
        num, remainder = divmod(num, base)
        # python對負數取餘時結果是負的，故需調整
        if remainder < 0:
            num, remainder = num + 1, remainder + abs(base)
        digits.append(remainder)
    return digits[::-1]

def anyToDec(numList, base):
    digits = numList[::-1]
    dec=0
    for i in range(len(digits)):
        dec+=digits[i]*(base**i)
    return dec

n=-22
negBin=[1,1,1,0,1]
print(decToAny(n,-2))
#print(decToAny(n,2))
#print(decToAny(n,0))
print(anyToDec(negBin,-3))

"""
<第二部分> 用內建函數實現一行2~36進位互轉
python的int函數可以把2~36進位的數轉換成十進位
第二個參數用來告訴程式這個數字是幾進位(默認是十進位)
第一個參數放字串
至於為何只能轉到36進位是因為0~9十個數字+A~Z二十六個字母共36個字
也可以第二個參數填0讓python自己去判斷是幾進位(此時第一參數字串前面要有標示它是幾進位)
0b : binary
0o : 八進位
0x : 十六進位
"""

print(int('Z',36))
print(int('0b10',0))
print(int('0o10',0))
print(int('0x10',0))
print(int('10',5))

"""
下面補個十進位(必須是正整數)轉成2~36進位的方法
"""

def baseN(num, b):
    assert num>=0 and 36>=b>=2, "數字必須是正整數且只能轉2~36進位"
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0")+\
            "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

print(baseN(17,18))
