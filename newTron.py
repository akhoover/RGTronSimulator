"""
Authors: /u/Azgurath
 	 /u/mpaw975
"""

import random
import sys
# from tronFunctions import two_in_hand, two_tron, use_map, use_scry 
from tronFunctions import *

## Draw or Play, from command line

if sys.argv[1] == "False":
	on_the_draw = False
else:
	on_the_draw = True

## Number of games to test, from command line

N = int(sys.argv[2])

def game(draw):
	# Populate deck
	deck = ["Mine", "Mine", "Mine", "Mine", "PP", "PP", "PP", "PP", "Tower", "Tower", "Tower", "Tower", "star", "star", "star", "star", "star", "star", "star", "star", "map", "map", "map", "map", "scry", "scry", "scry", "scry", "stir", "stir", "stir", "stir", "forest", "forest", "forest", "forest", "forest", "gq", "gq"]
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
		if starting_size <= 6 and not decided_on_hand:
			if two_in_hand(hand):
				decided_on_hand = True
			if "Tower" in hand or "Mine" in hand or "PP" in hand:
				if "map" in hand or "scry" in hand:
					decicded_on_hand = True

		#1 piece
		if starting_size <= 4 and not decided_on_hand:
			if "Tower" in hand or "Mine" in hand or "PP" in hand:
				decided_on_hand = True

		#Mull to 3
		if starting_size <= 3 and not decided_on_hand:
			decided_on_hand = True

		#Mulligan
		if not decided_on_hand:
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

		if scry_bottom:
			deck.remove( new_card )
			new_card = ""
						
	# Main loop for turns!
	turn = 0
	tron = False
	while not tron:

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
			if card == "forest":
				mana += 1
				green += 1

		# play a new tron land
		for card in hand:
			if card in {"Mine", "PP", "Tower"} and card not in field and lands_played == 0:
				hand.remove( card )
				field.append( card )
				mana += 1
				lands_played = 1

		# check if we have tron
		if "PP" in field and "Tower" in field and "Mine" in field:
			tron = True

		# crack stars for green
		if "star" in field:
			field.remove( "star" )
			new_card = random.choice( deck )
			deck.remove( new_card )
			hand.append( new_card )
			green += 1

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

		did_something = True
		while mana > 0 and did_something:

			did_something = False

			# if mana, cast stirrings
			if green > 0 and mana > 0 and "stir" in hand:
				# use stirrings
				green -= 1
				mana -= 1
				use_stir( hand, field, deck )
				did_something = True

			# cast star
			if "star" in hand and mana > 0:
				hand.remove( "star" )
				field.append( "star" )
				mana -= 1
				did_something = True

			# crack star
			if "star" in field and mana > 0:
				field.remove( "star" )
				green += 1
				new_card = random.choice( deck )
				deck.remove( new_card )
				hand.append( new_card )
				did_something = True

		# play a new tron land
		if lands_played == 0:
			for card in hand:
				if card in {"Mine", "PP", "Tower"} and card not in field:
					hand.remove( card )
					field.append( card )
					mana += 1
					lands_played = 1
					if two_tron( hand, field ):
						if "map" in field and mana > 1:
							use_map( hand, field, deck )
							mana -= 2
						if "scry" in hand and green > 0 and mana > 1:
							use_scry( hand, field, deck )
							green -= 1
							mana -= 2
						if "map" in hand and mana > 0:
							hand.remove( "map" )
							field.append( "map" )
							mana -= 1
						
			if lands_played == 0:
				for card in hand:
					if card == "forest":
						hand.remove( card )
						field.append( card )
						mana += 1
						green += 1
						lands_played = 1
			if lands_played == 0:
				for card in hand:
					if card == "gq":
						hand.remove( card )
						field.append( card )
						mana += 1
						lands_played = 1

			if "stir" in hand and green > 0 and mana > 0:
				use_stir( hand, field, deck )
				green -= 1
				mana -= 1

			if "star" in hand and mana > 0:
				hand.remove( "star" )
				field.append( "star" )
				mana -= 1
		# end turn


	return( turn, starting_size )

turn_three_tron = 0
total_turns = 0
failed_to_tron = 0
failed_starting_size = 0
success_starting_size = 0

for i in range( N ):
	turn, starting_size = game( on_the_draw )
	if turn == 3:
		turn_three_tron += 1
	if turn < 10:
		total_turns += turn
		success_starting_size += starting_size
	else:
		failed_to_tron += 1
		failed_starting_size += starting_size

avg_turns = total_turns / float( i - failed_to_tron )
failed_avg_size = failed_starting_size / float( failed_to_tron )
avg_size = success_starting_size / float( i - failed_to_tron )

print "Turn three tron: ", turn_three_tron
print "Average turn tron: ", avg_turns
print "Failed to get tron by tun 10: ", failed_to_tron
print "Mulled to an average of: ", avg_size
print "When failed to get tron, mulled to: ", failed_avg_size
