"""
	Assignment 3 		Word Segmentation via
				  		the TANGO Algorithm 
				  		
	Coded with love by	Lucas Freitas '15
						Harvard University
"""

import sys
import re
import matplotlib.pyplot as plt
from pylab import *

class Text:
	"""
	Attributes:
	input_file: 	name of the file that contains the original text (string)
	output_file:	name of the file that we want to output after segmentation (string)
	original_text:	list of lines of the original initialized text (list of strings)
	spaces_removed:	list of lines of the original text with spaces omitted (list of strings)
	max_n:			maximum length of n-gram in the TANGO algorithm (integer)
	ngrams:			dictionary of n-grams indexed by n-gram length - dic[i]
					is the dictionary of all n-grams of length i (dictionary)
	unsegmented:	list of lines to be segmented using TANGO algorithm
	tota_votes:		list of total votes for each boundary calculated by the TANGO algorithm
	threshold:		threshold parameter for TANGO algorithm
	segmented:		list of lines of the segmented text using the TANGO algorithm
	precision:		precision of the segmentation algorithm
	recall:			recall for the segmentation algorithm
	"""

	def __init__(self, input, output, max_n, threshold):
		"""
		Initialize a text type with its attributes

		Args:
			None
		Returns:
			None
		Raises:
			In case of IOError, prints error and exits
		"""
		self.input_file = input
		self.output_file = output
		self.original_text = self.open_input()
		self.max_n = max_n
		self.spaces_removed = [line.replace(" ", "").replace("\n", "")for line in self.original_text]
		self.ngrams = self.count_ngrams()
		self.unsegmented = self.spaces_removed
		self.threshold = threshold
		self.spaces_list = []
		self.spaces_answer = self.answerkey()
		self.segmented = self.segment()
		self.precision, self.recall = self.precision_recall()

	def open_input (self):
		"""
		Try to open and return text in input

		Args:
			None
		Returns:
			List of strings
		Raises:
			Raises:
			In case of IOError, prints error and exits
		"""

		try:
			input = open(self.input_file, 'r')
		except IOError:
			print "IOError: could not open", self.input_file
			sys.exit()

		return input.readlines()

	def count_ngrams (self):
		"""
		Generates a dictionary that contains one dictionary
		for each ngram size using the corpus of the text without
		spaces. The dictionary for each ngram size then stores
		ngrams with that specific size and their frequencies.
		The function then returns the complete dictionary.

		Args:
			text: list of lines to be processed
		Returns:
			None
		Raises:
			None
		"""

		# intialize ngrams dictionary
		ngrams = {}

		# initialize dictionaries for each ngram size
		for i in range (1, self.max_n + 1):
			ngrams[i] = {}

		# build dictionary considering each line in text
		for line in self.spaces_removed:
			# for each ngram size
			for k in range(1, self.max_n + 1):
				# add all ngrams of that size to the dictionary
				for i in range (0, len(line) - k + 1):
					ngrams[k][line[i : i + k]] = ngrams[k].get(line[i : i + k], 0) + 1
		# return dictionary
		return ngrams

	def answerkey (self):
		"""
		Generates a list of lists, each of the sublists corresponding
		to one line, and being a list of booleans, each boolean
		representing whether its index in the list is also the index
		of a boudary in the original text.

		Example: if the original text is "CS187 is awesome", its
		answerkey would be:

		[[False, False, False, False, True, False, True, False,
		False, False, False, False, False]]

		Args:
			None
		Returns:
			List of lists of booleans
		Raises:
			None
		"""
		spaces_list = []
		for i in range(len(self.original_text)):
			counter = 0
			list = []
			for l in range (len(self.spaces_removed[i])):
				if self.original_text[i][counter + 1] == " ":
					list.append(True)
					# jump over next character, since we can't have
					# contiguous space in our text
					counter += 2
				else:
					counter += 1
					list.append(False)
			spaces_list.append(list)
		return spaces_list

	def segment (self):
		"""
		Takes list of strings to be segmented and attempts to segment
		every line using the TANGO algorithm, saving result to a file
		with name self.output_file, and returning the list of segmented
		lines

		Args:
			None
		Returns:
			List of strings
		Raises:
			In case of IOError, prints error and exits
		"""

		try:
			out = open(self.output_file, 'w')
		except IOError:
			print "IOError: could not open", self.output_file
			sys.exit()

		# list of segmented lines
		segmented = []

		# list of booleans for whether each position is a boundary
		boundaries = []

		# attempt segmentation in every line
		self.iterative_tango()	

		# attempt segmentation in every line
		for line in self.unsegmented:
			new, list = self.add_spaces(line, self.threshold)
			# add segmented line to output file and list to be returned
			out.write(new)
			segmented.append(new)
			# add list of booleans to boundaries
			boundaries.append(list)

		# close output file
		out.close()

		# assign boundaries to the attribute spaces_list
		self.spaces_list = boundaries

		return segmented

	def iterative_tango (self):
		"""
		Iterates over all lines and all their possible
		boundaries and calculates the tango total vote for
		each each boundary of each line

		Args:
			None
		Returns:
			None
		Raises:
			None
		"""

		# dictionary for all total votes
		total_votes = {}

		for line in self.unsegmented:
			votes = {}
			# calculate the total vote for each boundary k in line
			for k in range(1, len(line)):
				votes[k] = self.total_vote(line, k)
			total_votes[line] = votes

		self.total_votes = total_votes

	def total_vote (self, line, k):
		"""
		Calculates total vote for a specific boundary
		using the TANGO algorithm

		Args:
			line: string to be segmented
			k: boundary to consider
		Returns:
			Float
		Raises:
			None
		"""

		# dictionary for all k votes
		v_k = {}

		# consider n-grams for n from 1 to max_n
		for n in range (1, self.max_n + 1):
			v_k[n] = self.tango(line, k, n)

		# normalize votes and return
		return sum(v_k.values()) / len(v_k)

	def tango (self, line, k, n):
		"""
		Calculates the total vote for a specific boundary
		and ngram size using the TANGO algorithm and padding

		Args:
			line: string to be segmented
			k: boundary to consider
			n: ngram size
		Returns:
			Float
		Raises:
			None
		"""

		vote = 0.

		# length of the string that we want to consider
		length = len(line)

		# strings on the left and right of bondary k
		left = line[max(0, k - n) : k]
		right = line[k : min(length, k + n)]

		# frequencies associated with left and right
		left_value = self.ngrams[len(left)][left]
		right_value = self.ngrams[len(right)][right]

		# all straddling n-grams with j characters
		# for TANGO, we want 1 <= j <= n - 1
		for j in range(1, n):
			# test left side
			stride = line[max(0, k - n + j) : min(length, k + j)]
			stride_value = self.ngrams[len(stride)][stride]
			vote += left_value > stride_value

			# test right side
			stride = line[min(length, k + j) : min(length, k + n + j)]
			if stride:
				stride_value = self.ngrams[len(stride)][stride]
				vote += right_value > stride_value
						
		# normalize vote
		if n > 1:
			vote /= (2 * n - 2)
		
		return vote

	def add_spaces (self, line, threshold):
		"""
		Adds spaces to line to complete segmentation based
		on the votes that each boundary location receives
		with the TANGO algorithm

		Args:
			line: string to be segmented
			threshold: threshold for the TANGO algorithm
		Returns:
			Tuple of string and list of booleans
		Raises:
			None
		"""

		num_spaces = 0
		# list of booleans to later compare to self.answer
		list = []

		# total votes for that line
		votes = self.total_votes[line]

		for l in range (1, len(line)):
			# decide on setting boundary in location l
			if l - 1 and l + 1 in votes:
				if (votes[l] > votes[l - 1] and votes[l] > votes[l + 1]) or votes[l] >= threshold:
					line = line[0 : l + num_spaces] + " " + line[l + num_spaces : len(line)]
					num_spaces += 1
					list.append(True)
				else:
					list.append(False)
			else:
				if votes[l] >= threshold:
					line = line[0 : l + num_spaces] + " " + line[l + num_spaces : len(line)]
					num_spaces += 1
					list.append(True)
				else:
					list.append(False)
		
		return line + "\n", list

	def precision_recall (self):
		"""
		Calculates the precision and recall of our TANGO implementation

		Args:
			None
		Returns:
			Tuple of floats
		Raises:
			None
		"""
		# true positive, false positives, and false negatives
		tp = 0.
		fp = 0.
		fn = 0.

		for i in range(len(self.spaces_list)):
			for j in range(len(self.spaces_list[i])):
				if self.spaces_list[i][j]:
					if self.spaces_answer[i][j]:
						tp += 1
					else:
						fp +=1
				else:
					if self.spaces_answer[i][j]:
						fn += 1

		if tp + fp:
			precision = tp / (tp + fp)
		else:
			precision = 0

		if tp + fn:
			recall = tp / (tp + fn)
		else:
			recall = 0

		return precision, recall

	def plot_graph (self):
		"""
		Plots precision versus recall for our TANGO implementation
		for threshold values from 0 to 1, with increments of 0.05

		Args:
			None
		Returns:
			None
		Raises:
			None
		"""
		
		# initial threshold
		threshold = 0

		# x axis values
		xs = []
		# y axis values
		ys = []

		while threshold <= 1:
			# list of booleans for whether each position is a boundary
			boundaries = []

			for line in self.unsegmented:
				text, list = self.add_spaces(line, threshold)
				boundaries.append(list)

			self.spaces_list = boundaries

			precision, recall = self.precision_recall()
			ys.append (precision)
			xs.append (recall)

			threshold += 0.05

		# initialize graph
		plt.clf()
		plt.title('Precision versus Recall for TANGO algorithm')
		plt.xlabel('Recall')
		plt.ylabel('Precision')

		p1, = plt.plot(xs, ys, '.')

		plt.axis([min(xs) - 0.05, max(xs) + 0.05, min(ys) - 0.05, max(ys) + 0.05])
	
		savefig('graph.pdf')
		plt.show() # show the figure

def parseArgs(args):
  	"""
	Parses arguments vector, looking for switches of the form -key {optional value}.
  	For example:
    parseArgs([ 'main.py', '-n', '-p', 5 ]) = { '-n':True, '-p':5 }

    Credit:
    	Thank you, CS181, for the code for parsing arguments
	Args:
		args: arguments passed to the program when running it
	Returns:
		Dictionary
	Raises:
		None
	"""
  
	args_map = {}
	curkey = None
	for i in xrange(1, len(args)):
		if args[i][0] == '-':
			args_map[args[i]] = True
			curkey = args[i]
		else:
			assert curkey
			args_map[curkey] = args[i]
			curkey = None
	return args_map

def main ():
	# parse command-line arguments
	args = parseArgs(sys.argv)

	# assign values based on arguments
	input = args["-f"]
	output = args["-p"]
	max_n = int(args["-n"])
	threshold = float(args["-t"])

	# create text structure, and then segment text
	text = Text(input, output, max_n, threshold)

	# print precision, recall and number of prediction lines used
	print "precision %.5f\nrecall %.5f" % (text.precision, text.recall)
	print "\n%d prediction lines used for evaluation" %len(text.original_text)
	
	# plot graph
	text.plot_graph()

if __name__ == "__main__":
	main()