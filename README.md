# RGTronSimulator
Python code to simulate a given number of games of  R/G Tron to find the earliest average turn Tron can be assembled, assuming no opponent interaction.

Bugs:
	- Using a shuffle effect, such as map or scrying, doesn't make the odds of drawing cards put on the bottom of the deck from the Vancouver mulligan scry or Ancient Stirring non-zero.
	- If all four of a tron piece are put on the bottom of the deck with the Vancouver mulligan scry and Ancient Stirrings, using map or scrying won't be able to find it. Happens about once every 150,000 - 200,000 games or so.
