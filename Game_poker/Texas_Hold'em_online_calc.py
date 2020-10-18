"""
程式功能:
用於線上玩Texas_Hold'em，假設對手的牌全是隨機，計算己方勝率
"""
from collections import Counter
from itertools import groupby

import sys
sys.path.append('..') # 添加相對路徑上層到sys.path，讓程式找到的模組_package
from _package._poker.poker_tool import StardardDeck

# 順子(注意A需要看作是1而非14)
def straight(rank):
    rank = sorted(set([1 if x==14 else x for x in rank]))
    for i in range(len(rank)-4):
        if rank[i+4]-rank[i]==4:
            return rank[i+4]
    return False
    
#回傳數字陣列恰好出現n次的數字，降序排列
def n_kind(rank, n):
    return sorted([k for k,v in Counter(rank).items() if v==n], reverse=True)


def card_rank(cards):
    """
    example: cards = ["5d", "5s", "9c", "9d", "9h"]
    輸出為 [9,9,9,5,5] 降序排列
    """
    return sorted(map(lambda s: '0123456789TJQKA'.index(s[0]), cards), reverse=True)


def groupby_suit(cards):
    """
    example: cards = ["5d", "5s", "9c", "9d", "9h"]
    group card by 花色，如{'c': [9], 'd': [9, 5], 'h': [9], 's': [5]}
    """
    cards = sorted(cards, key=lambda x:x[1])
    return {k:sorted(map(lambda c: '0123456789TJQKA'.index(c[0]), group), reverse=True) \
             for k,group in groupby(cards, lambda x:x[1])}


def hand_rank(hand):
    """
    hand 的格式為列表如 ["5d", "5s", "9c", "9d", "9h"] 來表示一手牌
    判斷手牌屬於何種牌型
    """
    rank = card_rank(hand)
    suit_gp = groupby_suit(hand)
    
    flush = sorted(filter(lambda v: len(v)>=5, suit_gp.values()), reverse=True)
    _straight = straight(rank)
    straightFlush = sorted(filter(lambda v: len(v)>=5 and straight(v), suit_gp.values()), reverse=True)
    
    single, pair, three_kind, four_kind = (n_kind(rank, i) for i in range(1,5))
    
    if straightFlush:
        return (9,max(straightFlush[0], key = lambda x: 1 if x==14 else x))
    if four_kind:
        head = four_kind[0]
        return (8,four_kind[0], max(filter(lambda r:r!=head,rank)))
    if len(three_kind)>=2 or three_kind and pair:
        head = three_kind[0]
        return (7,head, max(filter(lambda r:r!=head, pair+three_kind)))
    if flush:
        return (6, *flush[0][:5])
    if _straight:
        return (5, _straight)
    if three_kind:
        return (4,three_kind[0],*single[:2])
    if len(pair)>=2:
        return (3,*pair[:2],single[0])
    if len(pair)==1:
        return (2, pair[0],*single[:3])
    return (1,*single[:5])

#將一堆手牌按照牌型大小排序    
def pokerSort(hands):
    return sorted(hands,key=hand_rank,reverse=True)

def sepList(L,step):
    return [L[i:i+step] for i in range(0,len(L),step)]


def myCardWin(myCard, field, rivalCardList):
    """
    判斷自己的手牌是否獲勝, 範例格式:
    myCard= ["Kc", "Ac"]
    field= ["Kd", "Th", "4c", "6h", "As"]
    rivalCardList= [['Qd', 'Qc'], ['Ah', 4s']]
    return True
    """
    if not field:
        field = []
    myHand = myCard+field
    rivalHands=[r+field for r in rivalCardList]
    Hands=[myHand]+rivalHands
    
    """ 查看哪些牌可以贏過自己 """
    BIG_CARD = max(Hands,key=hand_rank)
    if myHand != BIG_CARD:
        print('--------------------')
        print(myHand, hand_rank(myHand))
        for r in rivalCardList:
            if hand_rank(r+field)> hand_rank(myHand):
                print(field, r, hand_rank(r+field))
            
    return myHand == BIG_CARD

def winProb(myCard, fieldCard=None, simulate=100, rivalNum=1):  
    """
    計算自己的手牌在一對多任意牌的狀況下的勝率
    """
    deck = StardardDeck()
    if not fieldCard:
        fieldCard = []
    
    # 將牌堆已展示的牌抽掉
    for card in myCard+fieldCard:
        deck.draw(card)
        
    field_card_num = len(fieldCard)
    assert field_card_num<=5, "Too many number of field cards."
    
    winNum = 0
    for _ in range(simulate):
        # 若公共牌還沒亮至5張，隨機補至5張牌
        # 隨機產生對手的牌
        cards = deck.rand_card(rivalNum*2 + 5-field_card_num)
        rival_card, field_card = sepList(cards[:2*rivalNum],2), cards[2*rivalNum:]
        if myCardWin(myCard, fieldCard + field_card , rival_card):
            winNum += 1        
    return winNum/simulate*100



def input_card(hintStr):
    """
    輸入撲克牌字串如: "2c Qc Ah"
    """
    cardStr = input(hintStr)
    if cardStr=="q":
        return "q"
    try:
        return list(map(lambda s:s[0].upper()+s[1], cardStr.split()))
    except:
        raise Exception("Error: wrong format of card")

if __name__=='__main__':
 
    """
    example cardForm: "8c 9c"
    """
    
    while True:
        print("--------------------------------------------")
        print("start a new game")
        mycard = input_card("What is your hand card? (e.g, ac(梅花a), 8d(方塊8))")
        r = ''
        while r=='':
            try:
                r = int(input(f"How many other players?"))
            except:
                pass
            
        print(f"Win prob is {winProb(mycard,rivalNum=1):.2f} for 1v1")
        print(f"Win prob is {winProb(mycard,rivalNum=r):.2f} for 1v{r}")
        
        hints = ["What is field?",
                 "What is fourth card?",
                 "What is fifth card?"]
        field_cards = [] 
        for h in hints:
            card = input_card(h+ " (Enter 'q' to Start a new game) ") 
            if card=='q':
                break
            field_cards.extend(card)
            print(f'field is {field_cards}')
            print(f"Win prob for {mycard} is {winProb(mycard,fieldCard=field_cards, rivalNum=r):.2f}")
            
    