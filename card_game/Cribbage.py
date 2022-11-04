__author__ = 'chill'

import random
from itertools import chain, combinations


def powerset(iterable, smallest=1):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(smallest, len(s) + 1)))


print(powerset([1, 2, 3, 4], 3))

class Combo_holder:
    def __init__(self):
        self.combinations = []
        self.value = 0

    def print_combinations(self):
        combos = []
        for combo in self.combinations:
            combo_str = []
            for card in combo:
                combo_str.append(str(card))
            combos.append(combo_str)
        print(combos)

class Card:
    def __init__(self, name, suit, value, order):
        self.name = name
        self.suit = suit
        self.value = value
        self.order = order

    def __str__(self):
        return '{name}{suit}'.format(name=self.name.capitalize(), suit=self.suit.capitalize())


class Deck:
    def __init__(self, type='standard'):
        self.type = type
        if type == 'standard':
            names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
            names_and_values = {}
            value = 1
            for name in names:
                names_and_values[name] = value
                value += 1
            suits = ['\u2664', '\u2665', '\u2666', '\u2667']
            self.cards = []
            for suit in suits:
                for name in names_and_values:
                    self.cards.append(Card(name, suit, names_and_values[name], names_and_values[name]))
        elif type == 'empty':
            self.cards = []
        elif type == 'cribbage':
            names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
            names_and_values = {}
            value = 1
            for name in names:
                names_and_values[name] = value
                if value < 10:
                    value += 1
            suits = ['\u2664', '\u2665', '\u2666', '\u2667']
            self.cards = []
            for suit in suits:
                for name in names_and_values:
                    if name == 'J':
                        self.cards.append(Card(name, suit, names_and_values[name], 11))
                    elif name == 'Q':
                        self.cards.append(Card(name, suit, names_and_values[name], 12))
                    elif name == 'K':
                        self.cards.append(Card(name, suit, names_and_values[name], 13))
                    else:
                        self.cards.append(Card(name, suit, names_and_values[name], names_and_values[name]))

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

    def sum(self):
        total = 0
        for card in self.cards:
            total += card.value
        return total


class Hand(Deck):

    def can_play(self, current):
        for card in self.cards:
            if current + card.value <= 31:
                return True
        return False

    def play_card(self, current=0):
        while True:
            try:
                while True:
                    print(self)
                    index = input("Choose a card to play: ")
                    if self.cards[int(index)].value + current <= 31:
                        break
                    else:
                        print("Card value was too high")

                return self.cards.pop(int(index))
                break
            except:
                print("Invalid Choice....")

    def play_random(self, current=0):
        while True:
            index = random.randint(0, self.size() - 1)
            if self.cards[index].value + current <= 31:
                return self.cards.pop(index)

    def powerset(self, iterable, smallest=1):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return list(chain.from_iterable(combinations(s, r) for r in range(smallest, len(s) + 1)))

    def straight_value(self, cards):
        for i in range(1, len(cards)):
            if cards[i - 1].order + 1 == cards[i].order:
                continue
            return 0
        return len(cards)

    def fifteen_value(self, cards):
        if sum([x.value for x in cards]) == 15:
            return 2
        return 0

    def double_value(self, cards):
        if cards[0].order == cards[1].order:
            return 2
        return 0

    def suit_value(self, cards):
        suit = cards[0].suit
        for card in cards:
            if card.suit != suit:
                return 0
        return len(cards)

    def score(self):
        cards = self.cards
        cards.sort(key=lambda x: x.order)
        powerset = self.powerset(cards, 2)
        straight = Combo_holder()
        fifteens = Combo_holder()
        doubles = Combo_holder()
        suits = Combo_holder()
        for combo in powerset:
            if len(combo) == 2:
                new_value = self.double_value(combo)
                if new_value > 0:
                    doubles.value += self.double_value(combo)
                    doubles.combinations.append(combo)
            else:
                highest_straight = 0
                new_straight = self.straight_value(combo)
                if new_straight > 0:
                    if highest_straight < new_straight:
                        highest_straight = new_straight
                        straight.value = 0
                        straight.combinations = []
                    if highest_straight == new_straight:
                        straight.value += new_straight
                        straight.combinations.append(combo)
                if len(combo) > 3:
                    new_suits = self.suit_value(combo)
                    if suits.value < new_suits:
                        suits.value = new_suits
                        suits.combinations = [combo]
            new_fifteen = self.fifteen_value(combo)
            if new_fifteen > 0:
                fifteens.value += new_fifteen
                fifteens.combinations.append(combo)
        print("Straight: " + str(straight.value))
        straight.print_combinations()
        print("Fifteens: " + str(fifteens.value))
        fifteens.print_combinations()
        print("Doubles: " + str(doubles.value))
        doubles.print_combinations()
        print("Suits: " + str(suits.value))
        suits.print_combinations()
        return None


myDeck = Deck('cribbage')
myDeck.shuffle()
hands = []
score = []
for i in range(2):
    hands.append(Hand('empty'))
extraHand = Hand('empty')
score.append([0, 0])

for i in range(6):
    for hand in hands:
        hand.add(myDeck.deal_1())
print("Player 1 gets the extra hand")
print("Discard 2 cards to the extra hand")
for i in range(2):
    extraHand.add(hands[0].play_random())
    extraHand.add(hands[1].play_random())
top_card = myDeck.deal_1()
# todo: points for top card reveal
print("The top card is " + str(top_card))
print("Your Hand: ")

discard_pile = Deck('empty')
discard = [[], []]
hands[1].cards.sort(key=lambda x: x.value)
for i in range(4):
    for j in range(2):
        if not hands[j].can_play(discard_pile.sum()):
            discard_pile = Deck('empty')
            score[-1][(j + 1) % 2] += 1
            print(score)
        discard[j].append(hands[j].play_random(discard_pile.sum()))
        # if j == 0:
        #     discard[j].append(hands[j].play_card(discard_pile.sum()))
        # else:
        #     discard[j].append(hands[j].deal_1())
        discard_pile.add(discard[j][i])
        if discard_pile.sum() == 31:
            score[-1][j] += 2
            print(score)
            discard_pile = Deck('empty')
        if discard_pile.sum() == 15:
            score[-1][j] += 2
            print(score)
        print(discard_pile)
        print(discard_pile.sum())
if discard_pile.size() > 0:
    score[-1][1] += 1

for i in range(4):
    for j in range(2):
        hands[j].add(discard[j].pop())

print(top_card)

for i in range(2):
    print(hands[i])
    hands[i].add(top_card)
    hands[i].score()

print(score)
