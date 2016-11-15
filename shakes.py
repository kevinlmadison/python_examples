# This script takes a given string and 
# continuously generates a random string
# until the given string and random string
# match. The script will also rank each
# random string according to how closely it
# matches the given string.

import random as rdm

def generate_string(to_match):
	alphabet = "abcdefghijklmnopqrstuvwxyz "
	new_string = ""
	for i in range(len(to_match)):
		new_string += alphabet[rdm.randrange(27)]
	return new_string

def rank(given_string, rand_string):
	matching = 0
	for i in range(len(given_string)):
		if given_string[i] == rand_string[i]:
			matching += 1
	return matching / len(given_string)

def main():
	string = "why so serious"
	new_string = generate_string(string)
	best = 0
	new_rank = rank(string, new_string)
	while new_rank < 1:
		if new_rank > best:
			print(new_rank, new_string)
			best = new_rank
		new_string = generate_string(string)
		new_rank = rank(string, new_string)

main()		
