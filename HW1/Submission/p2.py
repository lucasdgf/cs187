"""
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import re

def conditional (filename):
	"""
	Takes a file name, reads the file and calculates the conditional
	probability of each class in it, printing them to standard output

	Args:
		filename: name of the file to be read
	Returns:
		None
	Raises:
		None
	"""

	file = open(filename, 'r')
	
	# possible classes
	classes = {}
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
		else:
			classes[word] += 1
		total += 1

		# adding terms to each class's dictionaries and
		# counting the number of occurrences of each term

		new = list(set(re.findall(r'[a-z,A-Z]+', line)))
		for term in new:
			if term != word:
				if term not in dic:
					dic.append(term)
				if term not in terms[word]:
					terms[word][term] = 1
				else:
					terms[word][term] += 1

	for word in terms:
		for term in dic:
			if term not in terms[word]:
				prob = 1./(classes[word] + len(classes))
			else:
				prob = (1. + terms[word][term])/(classes[word] + len(classes))
			print "Pr(%s|%s), %f" %(term, word, prob)

def main ():
	conditional ("state_of_union_train_positional.txt")

if __name__ == "__main__":
	main()
