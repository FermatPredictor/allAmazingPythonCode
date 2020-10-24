import random


def random_re(regex):
    """
    函數功能: 根據正則表達式隨機生成字串
    範例: random_re(r'([a-z])(\d{1,2}|[AJQK])')
    """
    try:
        from xeger import Xeger
    except Exception as e:
        print(e)
        print("Use 'pip install xeger' first")
        return ''
    _x = Xeger()
    return  _x.xeger(regex)



if __name__=='__main__':
    print(random_re(r'([a-z])(\d{1,2}|[AJQK])'))