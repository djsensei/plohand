"""
Omaha tester
Dan Morris
8/9/13

This module is designed to test the omaha engine
"""

import random 
from poker_hand_engine import Card, Hand, rank_hand, HR_NONE, num2card, card2num, rank2string, compare_hands, same_rank_compare
from omaha_engine import determine_nuts

""" This module tests determine_nuts. It works!
deck = range(52)
for i in range(20):
	n = random.randint(3,5)
	random.shuffle(deck)
	b = []
	bs = ''
	for j in range(n):
		b.append(deck[j])
		bs += num2card[deck[j]]
	print bs + ' ' + str(determine_nuts(b))
"""