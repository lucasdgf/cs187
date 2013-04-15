"""
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import re
import os
import sys
import numpy
from math import log
from operator import itemgetter
import matplotlib.pyplot as plt
from pylab import *

# total number of word tokens
tokens = 0

# total number of word types
types = 0

# dictionary of all word types
word_types = {}

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

	return re.findall(r'[a-zA-Z][\w\'\-]*', file.read().lower())

def count_words (folder):
	"""
	Takes a folder name and goes through the text files in it,
	counting number of word tokens and creating a dictionary
	of all the words in the files

	Args:
		folder: name of the folder to be visited
	Returns:
		None
	Raises:
		None
	"""

	global tokens
	global types
	global word_types

	for root, dirs, files in os.walk(folder):
		for file in files:
			words = tokenize(folder + "/" + file)
			# count word tokens and types
			for word in words:
				tokens += 1
				if word not in word_types:
					word_types[word] = 1
					types += 1
				else:
					word_types[word] += 1

def count_unique (dict):
	"""
	Takes a dictionary of words and returns the number of word
	types that appear in the dictionary exactly once

	Args:
		dict: dictionary to be analyzed
	Returns:
		Integer
	Raises:
		None
	"""

	uniques = 0
	for word in dict:
		if dict[word] == 1:
			uniques += 1
	return uniques

def probability_new (news, tokens):
	"""
	Calculates the percentage news/tokens, or returns
	0 if tokens == 0

	Args:
		news: number of new words
		tokens: total number of tokens in text
	Returns:
		Integer
	Raises:
		None
	"""

	if tokens == 0:
		return 0
	else:
		return 100. * news / tokens

def count_new (dict, folder):
	"""
	Takes a dictionary of words and a folder and returns
	the percentage of new word types that appear in the
	folder but not in the dictionary

	Args:
		dict: dictionary of "old" words
		folder: folder to search for new words
	Returns:
		Integer
	Raises:
		None
	"""
	global tokens
	
	tokens = 0
	news = 0

	# check number of new words
	for root, dirs, files in os.walk(folder):
		for file in files:
			words = tokenize(folder + "/" + file)
			for word in words:
				tokens += 1
				if word not in dict:
					news += 1
					dict[word] = 1

	# calculate percentage of new words
	return probability_new(news, tokens)


def main ():
	
	global tokens

	global types

	global word_types

	# total number of word types only appearing once
	uniques = 0

	# total number of new words in data_part2
	news = 0

	folder1 = "data_part1"
	folder2 = "data_part2"

	count_words (folder1)

	# Problem 1
	print "Problem 1:\nTotal word tokens in data_part1: {0}\nTotal of word types in data_part1: {1}\n".format(tokens, types)

	# count number of word types that appear exactly once
	uniques = count_unique (word_types)
	
	# Problem 2
	print "Problem 2:\nTotal word types that appear only once in data_part1: {0}\n".format(uniques)

	# Problem 3

	# use Good-Turing estimate to calculate the probability that the
	# next word sampled will be a new word type
	if tokens == 0:
		probability = 0
	else:
		probability = 100. * uniques / tokens
	print "Problem 3:\nProbability the next word is a new word type: {0}%\n".format(probability)

	# Problem 4

	probability = count_new (word_types, "data_part2")
	print "Problem 4:\nPercentage of new word types in data_part2: {0}%\n".format(probability)

	# Problem 5

	folders = ["data_part1", "data_part2"]
	
	# reinitialize values
	tokens = 0
	types = 0
	word_types = {}
	
	for folder in folders:
		count_words (folder)
	print "Problem 5:\nTotal word tokens in data_part1 and data_part2: {0}\nTotal of word types in data_part1 and data_part2: {1}\n".format(tokens, types)

	# Problem 6

	uniques = count_unique (word_types)
	print "Problem 6:\nTotal number of word types that only appear once in data_part1 and data_part2: {0}\n".format(uniques)

	# Problem 7

	# use Good-Turing estimate to calculate the probability that the
	# next word sampled will be a new word type
	if tokens == 0:
		probability = 0
	else:
		probability = 100. * uniques / tokens
	print "Problem 7:\nProbability the next word is a new word type: {0}%\n".format(probability)

	# Problem 8

	probability = count_new (word_types, "data_part3")
	print "Problem 8:\nPercentage of new word types in data_part3: {0}%\n".format(probability)

	# Problem 10

	folders = ["data_part1", "data_part2", "data_part3"]
	# reinitialize values
	tokens = 0
	types = 0
	word_types = {}

	# count words and frequencies
	for folder in folders:
		count_words (folder)
	
	# sort frequencies by ranking
	rank = sorted(word_types.values(), reverse = True)

	# x axis values
	xs = range(1, len(rank) + 1)

	# y axis values
	ys = rank

	# convert values to logarithms for the scale
	for i in range(len(xs)):
		xs[i] = log(xs[i])
	for i in range(len(ys)):
		ys[i] = log(ys[i])

	# fit a line through the points - thanks to http://docs.scipy.org/
	x = np.array(xs)

	y = np.array(ys)

	A = np.vstack([x, np.ones(len(x))]).T
	m, c = np.linalg.lstsq(A, y)[0]


	# initialize graph
	plt.clf()
	plt.title('Frequency distribution')
	plt.xlabel('Logarithm of the ranking')
	plt.ylabel('Logarithm of the frequency')

	p1, = plt.plot(xs, ys, '.')
	p2, = plt.plot(x,  m*x + c, color='r')
	plt.axis([0, max(max(xs), -c/m), 0, max(max(ys), c)])
	plt.legend((p1,p2,), ('Word Type','Zipf\'s Law'), 'upper right')
	
	savefig('graph.pdf')
	plt.show() # show the figure

if __name__ == "__main__":
	main()