"""
	Homerwork 4 - Problem 1(b)
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import string

def main ():
	file = open("p1b.txt", "w")

	# accept space and close file
	file.write("0 1 <spc>\n1\n")
	file.close()

if __name__ == "__main__":
	main()
