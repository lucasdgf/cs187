"""
	Homerwork 4 - Problem 1(a)
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import string

def main ():
	file = open("p1a.txt", "w")

	# accept all alphabetical letters
	for letter in string.ascii_uppercase + string.ascii_lowercase:
		file.write("0 1 %c\n" %letter)

	# accept space and close file
	file.write("0 1 <spc>\n")
	file.write("1")
	file.close()

if __name__ == "__main__":
	main()
