"""
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import re
from math import log
from operator import itemgetter

# average accuracy of all runs
average_total = 0.
# average accuracy of all runs by class
average_classes = {}

def k_fold (training, test, k):
	"""
	Takes two file names: the training and test data and a constant k.
	Combines and shuffles the files using a helper function and then
	does 10-fold cross validation with them.

	Args:
		training: training data
		test: test data
		k: number of folds
	Returns:
		Tuple of two lists of strings
	Raises:
		None
	"""
	global average_total
	global average_classes

	data = shuffle (training, test)

	chunks = [data[i::k] for i in range(k)]
	
	for i in range(k):
		test = chunks[i]
		training = []
		for item in chunks:
			if item is not test:
				for elem in item:
					training.append(elem)
		classify (training, test)

	# print results
	print "Average accuracy of predictions: %f" %(average_total/k)
	print "Accuracy by class c:"

	for category in average_classes:
		print "\t%s %f" %(category.lower(), average_classes[category]/k)

def shuffle (training, test):
	"""
	Takes two file names: the training and test data. Combines the two
	and shuffles the data to then use the combined and shuffled data for
	k-fold cross-folding as a list of strings (lines)

	Args:
		training: training data
		test: test data 
	Returns:
		List of strings
	Raises:
		None
	"""
	import random

	# read files
	training = open(training, 'r').readlines()
	test = open(test, 'r').readlines()
	
	# merge them
	output = training + test
	
	# shuffle lines
	random.shuffle(output)

	return output

def classify (training, test):
	"""
	Takes two lists of string lines: the training and test data. The
	function calculates the conditional probability of each class in
	the training set and attempts to identify which class each speech
	belongs to using the multinomial method

	Args:
		training: training data
		test: test data 
	Returns:
		None
	Raises:
		None
	"""
	global average_total
	global average_classes
	
	# possible classes
	classes = {}
	# number of words in each class
	tokens = {}
	# terms in each class
	terms = {}
	# all the possible terms
	dic = []
	# total of speeches
	total = 0.

	for line in training:
		
		# set line to lower case
		line = line.lower()

		# get label and sublabel
		labels = re.match(r'([\w]+):([\w]+)', line)

		# get label alone
		word = labels.group(1)

		# delete the label and sublabel from the line
		line = line[len(labels.group()):]
		
		# identify the possible classes and check how many
		# documents fall under each of those classes

		if word not in classes:
			classes[word] = 1
			terms[word] = {}
			tokens[word] = 0
		else:
			classes[word] += 1
		total += 1

		# adding terms to each class's dictionaries and
		# counting the number of occurrences of each term

		old = list(set(re.findall(r'(\s)([\w\'\-]+|[\"\.!?,;:])', line.lower())))
		new = []
		for term in old:
			new.append(term[1]) 

		for term in new:
			tokens[word] += 1
			if term not in dic:
				dic.append(term)
			if term not in terms[word]:
				terms[word][term] = 1
			else:
				terms[word][term] += 1

	# test our model

	correct = {}
	all = {}
	total_tests = 0.
	total_correct = 0.

	# initialize dictionaries

	for category in classes:
		correct[category] = 0.
		all[category] = 0.

	# test each of the speeches

	for line in test:

		total_tests += 1

		# new is the list of all terms in the speech

		word = re.match(r'([\w]+):([\w]+)', line.lower()).group(1)
		old = list(set(re.findall(r'(\s)([\w\'\-]+|[\"\.!?,;:])', line.lower())))
		new = []
		for term in old:
			new.append(term[1])

		# calculate the a posteriori probability for each class

		max = {}

		for category in classes:
			
			# Pr(c)
			prob = log(classes[category]/total)

			# Pr(Bi = bi|c)
			for term in new:
				if term in dic:
					# calculate Pr(Bi = true|c)
					if term not in terms[category]:
						terms[category][term] = 0
					# add probability
					prob += log((1. + terms[category][term])/(tokens[category] + len(dic)))
			max[category] = prob

		result = sorted(max.items(), key=itemgetter(1), reverse=True)[0][0]

		# check if the prediction was right or not
		if result == word:
			total_correct += 1
			correct[word] += 1
		all[word] += 1

	# add accuracy to average at the end
	accuracy = total_correct/total_tests
	average_total += accuracy

	for category in classes:
		
		# add accuracy to average at the end
		accuracy = correct[category]/all[category]
		if category not in average_classes:
			average_classes[category] = accuracy
		else:
			average_classes[category] += accuracy

def main ():
	k_fold ("train_5500.label", "TREC_10.label", 10)

if __name__ == "__main__":
	main()