"""
	Homerwork 4 - Problem 
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import string

def main ():
	file = open("p4.txt", "w")

	letters = string.ascii_lowercase
	# encode message
	for i in range(26):
		file.write("0 0 %c %c\n" %(letters[i], letters[(i + 13) % 26]))
	
	# space encodes to space
	file.write("0 0 <spc> <spc>\n")
	file.write("0")
	file.close()

if __name__ == "__main__":
	main()