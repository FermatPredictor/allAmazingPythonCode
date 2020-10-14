import random
import time
from collections import Counter
from itertools import groupby

class Card():
    def __init__(self, cardStr, symbol):
        self.cardStr = cardStr
        self.symbol = symbol
        self.showing=False
    def __repr__(self):
        if self.showing:
            return self.symbol
        else:
            return "Card"
 
#用一字串表示一張牌，比如說梅花10是Tc，紅心A是Ah
def strToCard(cardStr):
    suits = {"h":"♡", "s":"♠", "d":"♢", "c":"♣"}
    symbol = cardStr[0]+suits[cardStr[1]]
    return Card(cardStr,symbol)
       
class Deck():  
    def shuffule(self, time=1):
        random.shuffle(self.cards)
        #print("Deck shuffled")
        
    def deal(self):
        return self.cards.pop(0)
    
    
    #放幾張特定的牌進牌堆，字串格式如 "5d 5s 9c 9d 9h"
    def put(self, cardStr):
        self.cards += list(map(strToCard, cardStr.split()))
    
    #抽出一張指定的牌
    def draw(self, cardStr):
        for c in self.cards:
            if cardStr==c.cardStr:
                card=c
                self.cards.remove(c)
                return card
        
class StardardDeck(Deck):
    def __init__(self):
        self.cards=[]
        suits = "cdhs"
        values= "23456789TJQKA"
        for name in values:
            for suit in suits:
                self.put(name+suit)
                
    def __repr__(self):
        return "Standard deck of cards:{0} remaining".format(len(self.cards))
    
class Player():
    def __init__(self):
        self.cards=[]
        
    def cardCount(self):
        return len(self.cards)
    
    #從牌組取幾張牌，預設抽出第一張牌
    def addCard(self, deck, cardStr=None):
        if cardStr==None:
            self.cards.append(deck.deal())
        else:
            for c in cardStr.split():
                self.cards.append(deck.draw(c))
    
    def strRepr(self):
        return ' '.join([card.cardStr for card in self.cards])
                
    
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
    cards 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌
    輸出為 [9,9,9,5,5] 降序排列
    """
    return sorted(map(lambda s: '0123456789TJQKA'.index(s[0]), cards.split()), reverse=True)


def groupby_suit(cards):
    """
    cards 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌，
    group card by 花色，如{'c': [9], 'd': [9, 5], 'h': [9], 's': [5]}
    """
    cards = sorted(cards.split(), key=lambda x:x[1])
    return {k:sorted(map(lambda c: '0123456789TJQKA'.index(c[0]), group), reverse=True) \
             for k,group in groupby(cards, lambda x:x[1])}


def hand_rank(hand):
    """
    hand 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌
    判斷手牌屬於何種牌型
    """
    rank = card_rank(hand)
    suit_gp = groupby_suit(hand)
    
    flush = sorted(filter(lambda v: len(v)>=5, suit_gp.values()), reverse=True)
    _straight = straight(rank)
    straightFlush = sorted(filter(lambda v: len(v)>=5 and straight(v), suit_gp.values()), reverse=True)
    
    single, pair,three_kind, four_kind = (n_kind(rank, i) for i in range(1,5))
    
    if straightFlush:
        return (9,max(straightFlush[0], key = lambda x: 1 if x==14 else x))
    if four_kind:
        head = four_kind[0]
        return (8,four_kind[0], max(filter(lambda r:r!=head,rank)))
    if len(three_kind)>=2 or three_kind and pair:
        head = three_kind[0]
        return (7,head, max(filter(lambda r:r!=head,rank)))
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

    
if __name__=='__main__':
    """
    程式功能: 用程試測試隨機五張牌的牌型概率，與數學算出來的理論值比較
    各牌型的出現概率如下:
    
    straight flush    0.0014%
    four of a kind    0.0240%
    full house        0.1441%
    flush             0.1965%
    straight          0.3925%
    three of a kind   2.1128%
    two pair          4.7539%
    one pair          42.2569%
    high card         50.1177%
    
    五~七張牌的機率: https://home.gamer.com.tw/creationDetail.php?sn=3828045
    
    實測一百萬次隨機取五張牌，大致與理論值接近:
    Total time= 34.431500 seconds
    #由高牌到同花順的出現次數
    [501392, 421984, 47823, 21211, 3953, 1994, 1406, 222, 15]
    
    [TODO] 目前隨機生成五張牌太花時間，需調整
    """
    List=[0]*9
    tStart = time.time()#計時開始
    deck = StardardDeck()
    deck.shuffule() #洗牌
    Tom=Player()
    for card in deck.cards:
        card.showing=True
    for _ in range(10000):
        deck.shuffule() #洗牌
        for _ in range(5):
            Tom.addCard(deck)
        cardType=hand_rank(Tom.strRepr())[0]
        List[cardType-1]+=1
        deck.put(Tom.strRepr()) #把牌放回牌堆
        Tom.cards.clear() #清空手牌
    tEnd = time.time()#計時結束
    print("Total time= %f seconds" % (tEnd - tStart))
    print(List)
