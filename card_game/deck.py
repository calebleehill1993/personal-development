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

    def size(self):
        return len(self.cards)