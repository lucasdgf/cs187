"""
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import re
from math import log
from operator import itemgetter

def classify (training, test):
	"""
	Takes two file names: the training and test data. The function reads
	the file and calculates the conditional probability of each class in it,
	and then reads the testing data to identify what class each speech belongs to

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
		
		# identify the possible classes and check how many
		# documents fall under each of those classes

		word = re.match(r'[\w]+', line).group()
		if word not in classes:
			classes[word] = 1
			terms[word] = {}
			tokens[word] = 0
		else:
			classes[word] += 1
		total += 1

		# adding terms to each class's dictionaries and
		# counting the number of occurrences of each term

		new = re.findall(r'[a-z,A-Z]+', line)
		for term in new:
			if term != word:
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
		correct[category] = 0
		all[category] = 0

	# test each of the speeches

	for line in file:

		total_tests += 1

		# new is the list of all terms in the speech

		word = re.match(r'[\w]+', line).group()
		new = re.findall(r'[a-z,A-Z]+', line)
		new.remove(word)

		# calculate the a posteriori probability for each class

		max = {}

		for category in classes:
			
			# Pr(c)
			prob = log(classes[category]/total)

			# Pr(Bi = bi|c)
			for term in new:

				# calculate Pr(Bi = true|c)
				if term not in terms[category]:
					terms[category][term] = 0
				prob += log((1. + terms[category][term])/(tokens[category] + len(dic)))
			max[category] = prob
		result = sorted(max.items(), key=itemgetter(1), reverse=True)[0][0]
		if result == word:
			total_correct += 1
			correct[word] += 1
		all[word] += 1

	print "Accuracy of prediction: %f" %(total_correct/total_tests)
	print "Accuracy by class c:"

	for category in classes:
		print "\t%s %f" %(category.lower(), correct[category]/all[category])

def main ():
	classify ("state_of_union_train_positional.txt", "state_of_union_test_positional.txt")

if __name__ == "__main__":
	main()