"""
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import re

def prior (filename):
	"""
	Takes a file name, reads the file and calculates the class priors,
	printing them to standard output

	Args:
		filename: name of the file to be read
	Returns:
		None
	Raises:
		None
	"""

	file = open(filename, 'r')
	
	all = {}
	total = 0.

	for line in file:
		word = re.match(r'[\w\'\-]+', line).group()
		if word not in all:
			all[word] = 1
		else:
			all[word] += 1
		total += 1

	for category in all:
		print "Pr(%s) = %f" %(category, all[category]/total)

def main ():
	prior ("state_of_union_train_positional.txt")

if __name__ == "__main__":
	main()
