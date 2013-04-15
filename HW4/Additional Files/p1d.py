"""
	Homerwork 4 - Problem 1(d)
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import string

def main ():
	file = open("p1d.txt", "w")

	# loop non-a letters back to their current state
	for letter in string.ascii_uppercase[1:] + string.ascii_lowercase[1:]:
		file.write("0 0 %c\n" %letter)
		file.write("1 1 %c\n" %letter)
	
	# move a from state 0 to 1
	file.write("0 1 a\n")
	file.write("1")
	file.close()

if __name__ == "__main__":
	main()
