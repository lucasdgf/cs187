"""
	Homerwork 4 - Problem 1(c)
	Coded with love by Lucas Freitas
	Harvard University Class of 2015 
"""

import string

def main ():
	file = open("p1c.txt", "w")

	# accept first uppercase letter
	for letter in string.ascii_uppercase:
		file.write("0 1 %c\n" %letter)

	# accepts following letters as lowercase
	for letter in string.ascii_lowercase:
		file.write("1 1 %c\n" %letter)

	file.write("1")
	file.close()

if __name__ == "__main__":
	main()
