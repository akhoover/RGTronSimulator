"""
Authors: /u/Azgurath
 	 /u/mpaw975
"""

import random
import sys

## Draw or Play, from command line

if sys.argv[1] == "False":
	on_the_draw = False
else:
	on_the_draw = True

## Number of games to test, from command line

N = int(sys.argv[2])

## Useful functions

def two_in_hand(hand):
	return(
			( "Mine" in hand and "PP" in hand )
		or
			( "Mine" in hand and "Tower" in hand )
		or
			( "PP" in hand and "Tower" in hand )
		)

def game(draw):
	# Populate deck
	deck = ["Mine", "Mine", "Mine", "Mine", "PP", "PP", "PP", "PP", "Tower", "Tower", "Tower", "Tower", "star", "star", "star", "star", "star", "star", "star", "star", "map", "map", "map", "map", "scry", "scry", "scry", "scry", "stir", "stir", "stir", "stir"]
	for x in range(60 - len(deck)):
		deck.append("dead")

	# Populate field
	field = []

	# Populate starting hand
	starting_size = 7
	decided_on_hand = False
	hand = random.sample( deck, 7 )
	have_tron = False

	# Mulligan
	# Keep if guarunteed tron
	# Keep if 6 cards or less and 2 or more tron pieces
	# Keep if 4 or less cards and 1 or more tron pieces

	while not decided_on_hand and starting_size > 0:

		#natural tron
		if "Mine" in hand and "Tower" in hand and "PP" in hand:
			have_tron = True
			decided_on_hand = True

		#guarunteed tron
		elif( two_in_hand(hand)
			and (
				( "map" in hand )
				or ( "scry" in hand and "star" in hand )
				)
			):
			have_tron = True
			decided_on_hand = True

		#2 pieces
		elif( starting_size <= 6 
			and ( two_in_hand(hand)):
			decided_on_hand = True

		#1 piece
		elif( starting_size <= 4
			and ( "Tower" in hand or "Mine" in hand or "PP" in hand ):
			decided_on_hand = True

		#Mull to 3
		elif starting_size <= 3 :
			decided_on_hand = True

		#Mulligan
		else:
			starting_size -= 1
			hand = random.sample( deck, starting_size )

	# Take the cards in hand from the deck

	for card in hand:
		deck.remove( card )

	# Scry if mulliganed

	scry = starting_hand < 7
	scry_bottom = True
	new_card = random.choice( deck )
	if scry and not have_tron:
		
		#Have two pieces, keep map or third piece
		if two_in_hand( hand ):
			if new_card in {"map", "Tower", "Mine", "PP"} and new_card not in hand:
				scry_bottom = False
			if new_card == "scry" and "star" in hand:
				scry_bottom = False
			if new_card == "star" and "scry" in hand:
				scry_bottom = False
			if new_card == "stir" and ( "star" in hand or "forest" in hand ):
				scry_bottom = False 
						

	# Main loop for turns!

	
			
				
			
