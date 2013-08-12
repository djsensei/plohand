"""
Poker engine for analyzing PLO Hands
adapted originally from Ethan's big2 code by dmo
adapted from dmo's previous open face chinese code

updatelog
{
6/22/13 
- Shifted cards in card2num. Now twos are low and Aces are high.
- Corrected the prime # product possibilities in possible_straights.
- Added HR_ROYAL_FLUSH and is_royal_flush()
- Added HR_TWO_PAIR and is_two_pair()
- Updated is_trips(), is_pair(), is_quads()
7/6/13
- updated rank_hand()
- wrote poker_engine_tester to test rank_hand(). It works!
- commented out safety lines in Hand.add_card()
} - big2 -> openface

{
8/8/13
- began adapting for PLO analysis

} - openface -> PLO

Each card is described as a 32-bit int:
XXXAKQJT98765432SHDCrrrrxxPPPPPP
     0-2:     Nothing.
     3-15:    Card Number.
     16-19:  Card Suit.
     20-23:  rrrr?
     24-25:  xx?
     26-31:  PPPPPP?

"""
ALL_CARDS = {
     # Clubs
     0:  int('00000000000000010001000000000010', 2),
     4:  int('00000000000000100001000100000011', 2),
     8:  int('00000000000001000001001000000101', 2),
     12: int('00000000000010000001001100000111', 2),
     16: int('00000000000100000001010000001011', 2),
     20: int('00000000001000000001010100001101', 2),
     24: int('00000000010000000001011000010001', 2),
     28: int('00000000100000000001011100010011', 2),
     32: int('00000001000000000001100000010111', 2),
     36: int('00000010000000000001100100011101', 2),
     40: int('00000100000000000001101000011111', 2),
     44: int('00001000000000000001101100100101', 2),
     48: int('00010000000000000001110000101001', 2),
     # Diamonds
     1:  int('00000000000000010010000000000010', 2),
     5:  int('00000000000000100010000100000011', 2),
     9:  int('00000000000001000010001000000101', 2),
     13: int('00000000000010000010001100000111', 2),
     17: int('00000000000100000010010000001011', 2),
     21: int('00000000001000000010010100001101', 2),
     25: int('00000000010000000010011000010001', 2),
     29: int('00000000100000000010011100010011', 2),
     33: int('00000001000000000010100000010111', 2),
     37: int('00000010000000000010100100011101', 2),
     41: int('00000100000000000010101000011111', 2),
     45: int('00001000000000000010101100100101', 2),
     49: int('00010000000000000010110000101001', 2),
     # Hearts
     2:  int('00000000000000010100000000000010', 2),
     6:  int('00000000000000100100000100000011', 2),
     10: int('00000000000001000100001000000101', 2),
     14: int('00000000000010000100001100000111', 2),
     18: int('00000000000100000100010000001011', 2),
     22: int('00000000001000000100010100001101', 2),
     26: int('00000000010000000100011000010001', 2),
     30: int('00000000100000000100011100010011', 2),
     34: int('00000001000000000100100000010111', 2),
     38: int('00000010000000000100100100011101', 2),
     42: int('00000100000000000100101000011111', 2),
     46: int('00001000000000000100101100100101', 2),
     50: int('00010000000000000100110000101001', 2),
     # Spades
     3:  int('00000000000000011000000000000010', 2),
     7:  int('00000000000000101000000100000011', 2),
     11: int('00000000000001001000001000000101', 2),
     15: int('00000000000010001000001100000111', 2),
     19: int('00000000000100001000010000001011', 2),
     23: int('00000000001000001000010100001101', 2),
     27: int('00000000010000001000011000010001', 2),
     31: int('00000000100000001000011100010011', 2),
     35: int('00000001000000001000100000010111', 2),
     39: int('00000010000000001000100100011101', 2),
     43: int('00000100000000001000101000011111', 2),
     47: int('00001000000000001000101100100101', 2),
     51: int('00010000000000001000110000101001', 2),
}

prime_filter = int('00000000000000000000000000111111', 2)
rank_filter  = int('00000000000000000000111100000000', 2)
suit_filter  = int('00000000000000001111000000000000', 2)
card_filter  = int('00011111111111110000000000000000', 2)

prime_shift = 0
rank_shift  = 8
suit_shift  = 12
card_shift  = 16

card2num = {
'2c':0, '3c':4, '4c':8,  '5c':12, '6c':16, '7c':20, '8c':24, '9c':28, 'tc':32, 'jc':36, 'qc':40, 'kc':44, 'ac':48,
'2d':1, '3d':5, '4d':9,  '5d':13, '6d':17, '7d':21, '8d':25, '9d':29, 'td':33, 'jd':37, 'qd':41, 'kd':45, 'ad':49,
'2h':2, '3h':6, '4h':10, '5h':14, '6h':18, '7h':22, '8h':26, '9h':30, 'th':34, 'jh':38, 'qh':42, 'kh':46, 'ah':50,
'2s':3, '3s':7, '4s':11, '5s':15, '6s':19, '7s':23, '8s':27, '9s':31, 'ts':35, 'js':39, 'qs':43, 'ks':47, 'as':51,
}

num2card = dict((val,key) for key, val in card2num.iteritems())

possible_straights = {
     8610      :3,
     2310      :4,
     15015     :5,
     85085     :6,
     323323    :7,
     1062347  :8,
     2800733  :9,
     6678671  :10,
     14535931 :11,
     31367009 :12,
}

# Hand _rankings
HR_NONE             = -1
HR_HIGH_CARD        = 0
HR_PAIR             = 1
HR_TWO_PAIR         = 2
HR_TRIPS            = 3
HR_STRAIGHT         = 4
HR_FLUSH            = 5
HR_FULL_HOUSE       = 6
HR_QUADS            = 7
HR_STRAIGHT_FLUSH   = 8
HR_ROYAL_FLUSH      = 9

rank2string = {
     HR_NONE:           'No Hand',
     HR_HIGH_CARD:      'High Card',
     HR_PAIR:           'Pair',
	 HR_TWO_PAIR:       'Two Pair',
     HR_TRIPS:          'Three of a Kind',
     HR_STRAIGHT:       'Straight',
     HR_FLUSH:          'Flush',
     HR_FULL_HOUSE:     'Full House',
     HR_QUADS:          'Four of a Kind',
     HR_STRAIGHT_FLUSH: 'Straight Flush',
	 HR_ROYAL_FLUSH:    'Royal Flush'
}


class Card:
    def __init__(self, c):
        try:
            self.card_num = int(c)
            self.card_name = num2card[c]
        except:
            self.card_name = c
            self.card_num = card2num[c]

    def json_dict(self):
        return {
            "name": self.card_name,
            "num": self.card_num,
            }

    def get_rank(self):
        return (ALL_CARDS[self.card_num] & rank_filter) >> rank_shift

    def get_name(self):
        return self.card_name

    def get_prime(self):
        return (ALL_CARDS[self.card_num] & prime_filter) >> prime_shift

    def get_raw_card(self):
        return ALL_CARDS[self.card_num]

    def __cmp__(self, other):
        return self.card_num - other.card_num
        """
        rank_diff = self.get_rank() - other.get_rank()
        if rank_diff == 0:
            return self.card_num - other.card_num
        else:
            return rank_diff
        """

    def __str__(self):
        return self.card_name

    def __unicode__(self):
        return self.card_name


class Hand:
    def __init__(self, *cs):
        self.num_cards = 0
        self.cards = []
        for c in cs:
            self.add_card(c)

    def json_dict(self):
        return {
            "cards": [c.json_dict() for c in self.cards],
            "num_cards": self.num_cards,
        }

    def set_dist(self):
        self.dist = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for c in range(0, self.num_cards):
            self.dist[self.cards[c].get_rank()] += 1

    def add_card(self, c):
        #if not (hasattr(c, "card_num") or c in card2num or c in num2card):
        #    return False
        self.num_cards += 1
        #if hasattr(c, "card_num"):
        #    self.cards.append(c)
        #else:
        self.cards.append(Card(c))
        self.cards.sort()
        self.set_dist()
        return True

    def __str__(self):
        outStr = ''
        for c in range(0, self.num_cards):
            outStr += self.cards[c].__str__() + ' '
        return outStr

def is_royal_flush(h): # if true, returns the Ace of the flush suit
	if h.num_cards != 5:
		return None
	if h.cards[4].get_rank() == 9:
		if is_flush(h):
			if is_straight(h):
				return h.cards[0]
	return None
		
def is_straight_flush(h): # if true, returns the top card of the straight flush
    if h.num_cards != 5:
        return None
    if is_flush(h):
        return is_straight(h)
    return None

def is_quads(h): # if true, returns one of the quads cards
    if h.dist.count(4) == 1:
		return h.cards[1]
    return None

def is_full_house(h): # if true, returns a card from the over part
    if h.num_cards != 5:
        return None
    trip_index = None
    pair_index = None
    for n in range(0,13):
        if h.dist[n] == 3:
            trip_index = n
        elif h.dist[n] == 2:
            pair_index = n

    if trip_index != None and pair_index != None:
        return h.cards[2]
    return None

def is_flush(h): # if true, returns the top card of the flush
    if h.num_cards != 5:
        return None
    suits = int('1111', 2)
    for c in range(0,5):
        next_suit = (h.cards[c].get_raw_card() & suit_filter) >> suit_shift
        suits &= next_suit
    if suits:
        return h.cards[0]
    return None

def is_straight(h): # if true, returns the top card of the straight
	if h.num_cards != 5:
		return None
	mult = 1
	for c in range(0,5):
		nextMult = (h.cards[c].get_raw_card() & prime_filter) >> prime_shift
		mult *= nextMult
	if mult in possible_straights:
		return h.cards[0]
	return None

def is_trips(h): # if true, returns one of the trips cards
    if h.num_cards < 3:
        return None
    for n in range(0,h.num_cards-2):
		if h.cards[n].get_rank() == h.cards[n+1].get_rank() == h.cards[n+2].get_rank():
			return h.cards[2]
    return None
	
def is_two_pair(h): # if true, returns one of the higher pair cards
    if h.dist.count(2) == 2:
        return h.cards[1]
    return None

def is_pair(h): # if true, returns one of the paired cards
    if h.num_cards < 2:
        return None
    for n in range(0,h.num_cards-1):
		if h.cards[n].get_rank() == h.cards[n+1].get_rank():
			return h.cards[n]
    return None


def rank_hand(h):
	"""
    Returns array [rank int, key card].
	key cards by rank:
		RF = A of that suit
		SF = top card
		Q = one of the quads
		FH = one of the trips part
		F = top card
		S = top card
		Tr = one of the trips
		2P = one of the higher pair
		1P = one of the pair
		HC = highest card
	Note - could be improved with earlier filtering, 
		rather than trying everything from the top down...
    """
	
	best_card = is_royal_flush(h)
	if best_card:
		return [HR_ROYAL_FLUSH, best_card]
	
	best_card = is_straight_flush(h)
	if best_card:
		return [HR_STRAIGHT_FLUSH, best_card]

	best_card = is_quads(h)
	if best_card:
		return [HR_QUADS, best_card]

	best_card = is_full_house(h)
	if best_card:
		return [HR_FULL_HOUSE, best_card]

	best_card = is_flush(h)
	if best_card:
		return [HR_FLUSH, best_card]

	best_card = is_straight(h)
	if best_card:
		return [HR_STRAIGHT, best_card]

	best_card = is_trips(h)
	if best_card:
		return [HR_TRIPS, best_card]
	
	best_card = is_two_pair(h)
	if best_card:
		return [HR_TWO_PAIR, best_card]

	best_card = is_pair(h)
	if best_card:
		return [HR_PAIR, best_card]
	
	if h.num_cards > 0:
		return [HR_HIGH_CARD, h.cards[0]]
	else:
		return [HR_NONE, None]

def compare_hands(h1, h2):
	# returns 
	# 0 if h1 is better
	# 1 if h2 is better
	# 2 if same
	r1 = rank_hand(h1)
	r2 = rank_hand(h2)
	if r1[0] > r2[0]:
		return 0
	elif r1[0] < r2[0]:
		return 1
	else:
		return same_rank_compare(h1, h2, r1, r2)
		
def same_rank_compare(h1, h2, r1, r2):
	if r1[0] == 9:
		# all RF are equal!
		return 2
	elif r1[0] == 8 or r1[0] == 4 or r1[0] == 7 or r1[0] == 6 or r1[0] == 3:
		# SF Q FH S T just need topcard checked
		if r1[1] > r2[1]:
			return 0
		elif r1[1] < r2[1]:
			return 1
		else:
			return 2
	elif r1[0] == 5 or 0:
		# F HC check each card in sequence (from top to bottom)
		for i in range(5):
			if h1.cards[5-i].get_rank() > h2.cards[5-i].get_rank():
				return 0
			elif h1.cards[5-i].get_rank() < h2.cards[5-i].get_rank():
				return 1
		return 2
	elif r1[0] == 2:
		# 2P check top pair first, then bottom pair, then kicker
		if r1[1] > r2[1]:
			return 0
		elif r1[1] < r2[1]:
			return 1
		else:
			if h1.cards[1].get_rank() > h2.cards[1].get_rank():
				return 0
			elif h1.cards[1].get_rank() < h2.cards[1].get_rank():
				return 1
			else:
				for i in range(5):
					if h1.cards[5-i].get_rank() > h2.cards[5-i].get_rank():
						return 0
					elif h1.cards[5-i].get_rank() < h2.cards[5-i].get_rank():
						return 1
				return 2
	elif r1[0] == 1:
		# 1P check pair first, then kickers
		if r1[1] > r2[1]:
			return 0
		elif r1[1] < r2[1]:
			return 1
		else:
			for i in range(5):
				if h1.cards[5-i].get_rank() > h2.cards[5-i].get_rank():
					return 0
				elif h1.cards[5-i].get_rank() < h2.cards[5-i].get_rank():
					return 1
			return 2
	
if __name__ == '__main__':
    #h = Hand('jh', '2s', 'js', 'js', '2s')
    # LOGGING print is_full_house(h)
    test_hand_ranks()
