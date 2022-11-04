import random

class Card:
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value

    def __str__(self):
        return '{name} of {suit}'.format(name=self.name.capitalize(), suit=self.suit.capitalize())

class Deck:
    def __init__(self, type='standard'):
        if type == 'standard':
            names = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
            names_and_values = {}
            value = 1
            for name in names:
                names_and_values[name] = value
                value += 1
            suits = ['hearts', 'diamonds', 'spades', 'clubs']
            self.cards = []
            for suit in suits:
                for name in names_and_values:
                    self.cards.append(Card(name, suit, names_and_values[name]))
        elif type == 'empty':
            self.cards = []

    def __str__(self):
        cards = []
        for card in self.cards:
            cards.append(str(card))
        return str(cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_1(self):
        return self.cards.pop(0)

    def empty(self):
        self.cards = []

    def add(self, card):
        self.cards.insert(0, card)

    def add_bottom(self, card):
        self.cards.append(card)

    def size(self):
        return len(self.cards)

player1 = Deck('empty')
player2 = Deck('empty')

mydeck = Deck()
mydeck.shuffle()

while mydeck.size() > 1:
    player1.add(mydeck.deal_1())
    player2.add(mydeck.deal_1())

battles = 0

while player1.size() > 0 and player2.size() > 0:
    p1cards = [player1.deal_1()]
    p2cards = [player2.deal_1()]
    if p1cards[-1].value > p2cards[-1].value:
        player1.add_bottom(p1cards[-1])
        player1.add_bottom(p2cards[-1])
    elif p2cards[-1].value > p1cards[-1].value:
        player2.add_bottom(p1cards[-1])
        player2.add_bottom(p2cards[-1])
    else:
        while p1cards[-1].value == p2cards[-1].value:
            if player1.size() < 2 or player2.size() < 2:
                print(player1)
                print(p1cards)
                print(player2)
                print(p2cards)
                break

            for i in range(2):
                p1cards.append(player1.deal_1())
                p2cards.append(player2.deal_1())
        if p1cards[-1].value > p2cards[-1].value:
            for i in range(len(p1cards)):
                player1.add_bottom(p1cards.pop(0))
            for i in range(len(p2cards)):
                player1.add_bottom(p2cards.pop(0))
        elif p2cards[-1].value > p1cards[-1].value:
            for i in range(len(p2cards)):
                player2.add_bottom(p2cards.pop(0))
            for i in range(len(p1cards)):
                player1.add_bottom(p1cards.pop(0))
    battles += 1
    if battles > 10000:
        print(player1)
        print(p1cards)
        print(player2)
        print(p2cards)
        break

print(player1.size(), player2.size(), battles)

