# We were sitting at Grandma Bingham's on 2022/08/22 trying to solve the Missoula paper codex problem and were
# looking for words matching the pattern 123345 and 126645 where each number is a distinct letter.
import string
from urllib import request
import re
from itertools import permutations

url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'
f = request.urlopen(url)
text = f.read().decode('utf-8').lower()
words = text.split()


cryptoquote = 'yjr fph syr gppf.'

letters = re.findall(r'[a-z]', cryptoquote)
cryptowords = re.findall(r'[a-z]+', cryptoquote)

cipher = dict()

for letter in letters:
    cipher[letter] = ''

print(letters)
print(cipher)
print(string.ascii_lowercase)
print(cryptowords)

def translate(cryptoquote):
    quote = ''
    for symbol in cryptoquote:
        if symbol in string.ascii_lowercase:
            quote += cipher[symbol]
        else:
            quote += symbol
    return quote

letter_i = 0
word_i = 0

perms = permutations(string.ascii_lowercase, 3)

while True:
    word_perm = next(perms)

    for i in range(min(len(letters), len(word_perm))):
        cipher[letters[i]] = word_perm[i]

    print(translate(cryptowords[0]))

    if translate(cryptowords[0]) in words:
        break

print(translate(cryptoquote))

# six = list(filter(re.compile(r'^[a-z]{6}$').match, words))
# two = list(filter(re.compile(r'^[a-z]{2}$').match, words))
# real_twos = ['ad', 'am', 'an', 'as', 'at', 'by', 'go', 'hi', 'ho', 'if', 'in', 'is', 'me', 'my', 'no', 'oh', 'on', 'or', 'to', 'um', 'us', 'we']
#
# possible_match = []
#
# print('123456'[0:2][::-1])
#
# for word in six:
#     if word[2] == word[3]:
#         if len(set(word)) == 5:
#             if word[0:2][::-1] in real_twos:
#                 possible_match.append(word)
#
# print(possible_match)
#
# possible_combos = {}
#
# for word in possible_match:


