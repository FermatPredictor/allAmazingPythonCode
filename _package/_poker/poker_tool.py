import random

# cardStr是一個字串，表示一張牌，比如說梅花10是Tc，紅心A是Ah
# return 視覺化表示
def symbol(cardStr):
    suits = {"h":"♡", "s":"♠", "d":"♢", "c":"♣"}
    return cardStr[0]+suits[cardStr[1]]

class Deck():
    def __init__(self, cards):
        self.cards = cards
        
    def shuffule(self):
        random.shuffle(self.cards)
    
    #抽一張牌，默認抽牌堆最上方的牌，或指定抽特定牌
    def draw(self, card=None):
        if card:
            self.cards.remove(card)
            return card
        return self.cards.pop(0)
    
    #放幾張特定的牌進牌堆，如 ["5d", "5s", "9c", "9d", "9h"]
    def put(self, cards):
        self.cards += cards
    
    # 隨機不重複的展示n張牌
    def rand_card(self, n):
        return random.sample(self.cards, k=n)
        
    def __repr__(self):
        return str([symbol(c) for c in self.cards])
        
class StardardDeck(Deck):
    def __init__(self):
        self.cards=[v+s for v in "23456789TJQKA" for s in "cdhs"]
                
    
class Player():
    def __init__(self):
        self.cards=[]
    
    #從牌組取幾張牌，預設抽出第一張牌
    def addCard(self, deck, cards=None):
        if not cards:
            self.cards.append(deck.draw())
            return
        for c in cards:
            self.cards.append(deck.draw(c))
    
    def __repr__(self):
        return str([symbol(c) for c in self.cards])
    
    
if __name__=='__main__':
    deck=StardardDeck()
    deck.shuffule()
    print(deck)    
    
    # 抽7張牌
    Tom = Player()
    for _ in range(7):
        Tom.addCard(deck)
    print(Tom)
    print(deck)
    