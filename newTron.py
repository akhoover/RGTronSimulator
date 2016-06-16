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

def two_tron( hand, field ):
	
	for card in ["Tower", "Mine", "PP"]:
		if card in hand or card in field:
			for new_card in ["Tower", "Mine", "PP"]:
				if new_card in hand or new_card in field:
					if new_card != card:
						return True
	
	return False


def use_map( hand, field, deck ):

	field.remove( "map" )
	for card in ["Tower", "Mine", "PP"]:
		if card not in hand and card not in field:
			deck.remove( card )
			hand.append( card )

def use_scry( hand, field, deck ):
	
	hand.remove( "scry" )
	for card in ["Tower", "Mine", "PP"]:
		if card not in hand and card not in field:
			deck.remove( card )
			hand.append( card )

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
			and two_in_hand(hand)):
			decided_on_hand = True

		#1 piece
		elif( starting_size <= 4
			and ( "Tower" in hand or "Mine" in hand or "PP" in hand )):
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

	scry = starting_size < 7
	scry_bottom = True
	new_card = ""
	if scry and not have_tron:
	
		new_card = random.choice( deck )
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

		# if scry_bottom:
			# deck.remove( new_card )
			# new_card = ""
						
	# Main loop for turns!
	turn = 0
	tron = False
	while not tron and turn < 4:

		# increment turn counter
		turn += 1
		
		# initialize mana to 0
		mana = 0
		green = 0
		lands_played = 0

		# draw a card

		# if it's the first card after scrying
		if (draw and turn == 1) or (not draw and turn == 2):
			if new_card == "":
				new_card = random.choice( deck )
			hand.append( new_card )
			deck.remove( new_card )

		# otherwise
		elif draw or turn != 1:
			new_card = random.choice( deck )
			hand.append( new_card )
			deck.remove( new_card )

		# tap lands for mana
		for card in field:
			if card in {"Mine", "PP", "Tower", "gq"}:
				mana += 1
			if card == "Forest":
				mana += 1
				green += 1

		# crack stars for green
		if "star" in field:
			field.remove( "star" )
			green += 1

		# play a new tron land
		for card in hand:
			if card in {"Mine", "PP", "Tower"} and card not in field and lands_played == 0:
				hand.remove( card )
				field.append( card )
				mana += 1
				lands_played = 1

		# if two tron pieces, use map or scrying
		if two_tron( hand, field ):
			# use map
			if "map" in field and mana > 1:
				use_map( hand, field,  deck )
				mana -= 2
			# cast scrying
			if "scry" in hand and mana > 1 and green > 0:
				use_scry( hand, field, deck )
				mana -= 2
				green -= 1
			# cast map
			if "map" in hand and mana > 0:
				hand.remove( "map" )
				field.append( "map" )
				mana -= 1

			# cast star
			if "star" in hand and mana > 0:
				hand.remove( "star" )
				field.append( "star" )
				mana -= 1

		# check if we have tron
		if "PP" in field and "Tower" in field and "Mine" in field:
			tron = True

		# end turn


	return( turn, have_tron )

turn_three_tron = 0
should_tron = 0

for i in range( N ):
	turn, tron = game( on_the_draw )
	if turn == 3:
		turn_three_tron += 1
	if tron:
		should_tron += 1

print "Turn three tron: ", turn_three_tron
print "Should be at least: ", should_tron
