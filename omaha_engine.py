"""
Omaha hand strength engine
Dan Morris
8/9/13

This module contains the necessary functions to determine the strength of an Omaha hand. 
It uses functions from poker_hand_engine.py. 
"""

import random 
from poker_hand_engine import Card, Hand, rank_hand, HR_NONE, num2card, card2num, rank2string, compare_hands, same_rank_compare

# determine_nuts takes an array 'board' (3, 4, or 5 cards in simple numeric [0-51] format) as input and outputs the rank of the nut hand
# 3 = trips, 4 = straight, 5 = flush, 6 = full house
# quads and straight flushes will be disregarded (for now)
def determine_nuts(board):
	board.sort()
	b = []
	for i in range(len(board)):
		b.append(Card(board[i]))
	# check for pairs - FullHouse
	for i in range(len(b)-1):
		if b[i].get_rank() == b[i+1].get_rank():
			return 6
	# check for 3-suit - Flush
	s = []
	for i in range(len(b)):
		c = b[i].card_name
		s.append(c[1])
	if s.count('s') > 2 or s.count('h') > 2 or s.count('d') > 2 or s.count('c') > 2:
		return 5
	for i in range(len(b)-2):
		if b[i+2].get_rank() - b[i].get_rank() < 5:
			return 4
	# check for 3 cards in a 5-run - Straight
	# no fullhouse flush or straight means Trips is best
	return 3
	
# besthand determines the strongest hand possible given an omaha hand and a board
# it returns the numeric rank of the hand and the two cards used
def besthand(h, b):	

# the following functions take in a hand known to be of a certain rank (just the two cards in use)
# and determine the relative strength, returning 1,2,3... for nut, 2nd nut, etc.
def nutflush(h2, b):

def nutstraight(h2, b):

def topset(h2, b):

def toptwo(h2, b):

def toppair(h2, b):

# freshhand produces a fresh hand and remainder deck
def freshhand():
	deck = range(52)
	random.shuffle(deck)
	hand = deck[:3]
	deck = deck[4:]
	return hand, deck
	
# restdeck takes an omaha hand and returns the remainder of the deck, shuffled
def restdeck(h):
	if isinstance(h[0],Card):
		for i in range(4):
			h[i] = card2num(h[i].get_name())
	deck = range(52)
	for i in range(4):
		deck.remove(h[i])
	random.shuffle(deck)
	return deck