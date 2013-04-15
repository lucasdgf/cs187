"""
Coded with love by Lucas Freitas
Harvard University Class of 2015 
"""

import re
import sys
from operator import itemgetter

def frequent (list, letter):
	"""
	Takes a list of strings and returns the most frequent string
	in the list starting with the letter "letter:

	Args:
		list: Python list to be analyzed
		letter: first letter of the most frequent string
	Returns:
		string
	Raises:
		None
	"""

	filter = {}

	for word in list:
		if word[0] == letter:
			if word not in filter:
				filter[word] = 1
			else:
				filter[word] += 1

	print sorted(filter.items(), key=itemgetter(1), reverse=True)[0][0]

def tokenize (filename):
	"""
	Takes a text file name and returns a Python list containing
	a tokenized version of the text of the file

	Args:
		filename: name of the text file to be tokenized
	Returns:
		List of strings
	Raises:
		In case of IOError, prints error and exits
	"""

	try:
		file = open(filename, 'r')
	except IOError:
		print "IOError: could not open", filename
		sys.exit()

	return re.findall(r'[\w\'\-]+|[\"\.!?,;:]', file.read().lower())

def main ():
	frequent (tokenize ("Obama_2013_inaugural.txt"), 'f')

if __name__ == "__main__":
	main()
