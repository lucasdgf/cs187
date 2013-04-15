"""
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import re
from math import log
from operator import itemgetter

def classify (training, test):
	"""
	Takes two file names: the training and test data. The function
	reads the training set and checks the most common label, guessing
	it for all of the labels of the test set

	Args:
		training: training data
		test: test data 
	Returns:
		None
	Raises:
		None
	"""

	file = open(training, 'r')
	
	# dictionary of classes
	classes = {}
	total = 0

	for line in file:
		
		# get label
		word = re.match(r'([\w]+):([\w]+)', line.lower()).group(1)
	
		# add label to classes dictionary
		if word not in classes:
			classes[word] = 1
		else:
			classes[word] += 1
		total += 1

	# most common class
	max = sorted(classes.items(), key=itemgetter(1), reverse=True)[0][0]

	# test our model
	file = open(test, 'r')
	correct = {}
	all = {}
	total_tests = 0.
	total_correct = 0.

	# initialize dictionaries
	for category in classes:
		correct[category] = 0.
		all[category] = 0.

	# test each of the speeches
	for line in file:
		total_tests += 1

		# label of the entry
		word = re.match(r'([\w]+):([\w]+)', line.lower()).group(1)
		if max == word:
			total_correct += 1
			correct[word] += 1
		all[word] += 1

	# print results
	print "Accuracy of prediction: %f" %(total_correct/total_tests)
	print "Accuracy by class c:"

	for category in classes:
		print "\t%s %f" %(category.lower(), correct[category]/all[category])

def main ():
	classify ("train_5500.label", "TREC_10.label")

if __name__ == "__main__":
	main()