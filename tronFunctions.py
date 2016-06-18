## Useful functions

import random

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


def use_map( hand, field, deck, bottom ):

	field.remove( "map" )
	deck.extend( bottom )
	bottom = []
	for card in ["Tower", "Mine", "PP"]:
		if card not in hand and card not in field:
			try:
				deck.remove( card )
			except ValueError:
				print "Hand: "
				print hand
				print "Field: "
				print field
				print "Deck:"
				print deck
			hand.append( card )

def use_scry( hand, field, deck, bottom ):
	
	hand.remove( "scry" )
	deck.extend( bottom )
	bottom = []
	for card in ["Tower", "Mine", "PP"]:
		if card not in hand and card not in field:
			try:
				deck.remove( card )
			except:
				print "Oops..."
			hand.append( card )

def use_stir( hand, field, deck, bottom ):
	
	hand.remove( "stir" )
	cards = random.sample( deck, 5 )
	card_chosen = ""

	# Look for if we have guraunteed tron
	if two_tron( hand, field ):
		if( ( "map" in hand or "map" in field )
			or( ( "star" in hand or "star" in field )
			and( "scry" in hand ))):

			# If so, take Karn or stars to dig.
			if "Karn" in cards and card_chosen == "":
				card_chosen = "Karn"
			if "star" in cards and card_chosen == "": 
				card_chosen = "star"
			if "forest" in cards and card_chosen == "": 
				card_chosen = "forest"

	# If we don't have tron, get things to help us get it

	# Get new tron piece
	for card in cards:
		if card in {"Tower", "Mine", "PP"}:
			if card not in field and card not in hand and card_chosen == "":
				card_chosen = card
	
	# Get map if we have two pieces in hand
	if two_tron( hand, field ) and "map" in cards and card_chosen == "":
		card_chosen = "map"

	# Get a star
	if "star" in cards and card_chosen == "":
		card_chosen = "star"

	# Get a forest
	if "forest" in cards and card_chosen == "":
		card_chosen = "forest"

	# Get any other land
	for card in cards:
		if card in {"Tower", "Mine", "PP", "gq"} and card_chosen == "":
			card_chosen = card
	
	# Add chosen card to hand, remove other five from the deck.
	# Ideally these cards will be stored in a list and re-appended
	#   to the deck when a map or scrying is used.
	if card_chosen != "":
		hand.append( card_chosen )

	for card in cards:
		deck.remove( card )
		bottom.append( card )

