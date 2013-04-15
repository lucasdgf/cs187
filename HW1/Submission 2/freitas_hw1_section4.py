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
	reads the training set and calculates the conditional probability
	of each class in it, and then reads the testing data to identify
	what class each speech belongs to using the multinomial method

	Args:
		training: training data
		test: test data 
	Returns:
		None
	Raises:
		None
	"""

	file = open(training, 'r')
	
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

	for line in file:
		
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

	# print results
	print "Accuracy of prediction: %f" %(total_correct/total_tests)
	print "Accuracy by class c:"

	for category in classes:
		print "\t%s %f" %(category.lower(), correct[category]/all[category])

def main ():
	classify ("train_5500.label", "TREC_10.label")

if __name__ == "__main__":
	main()