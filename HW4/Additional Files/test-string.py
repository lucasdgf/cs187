#!/usr/bin/env python

import sys
import os
import re

if len(sys.argv) < 2: 
	print "Usage: ./test-string.py <fst-filename>"
	sys.exit()
else:
	fst_name = sys.argv[1] 

pathToFSM = ""

more = True
testStr = ""
while (more == True): 
	testStr = raw_input("Please type a string to test: ")
	
	f = file("input.txt", "w")
	for i in range(len(testStr)):
		if testStr[i] == " ":
			f.write('%d\t%d\t<spc>\t<spc>\n' %(i, i+1))
		else:
			f.write('%d\t%d\t%s\t%s\n' %(i, i+1, testStr[i], testStr[i]))
	f.write("%s\n" %(i+1))
	f.close()
	
	os.system("fstcompile --isymbols=test.sym --osymbols=test.sym --keep_isymbols --keep_osymbols input.txt input.fst")
	os.system("fstcompose input.fst %s | fstproject --project_output - | fstshortestpath - | fsttopsort - | fstprint > test.out" %fst_name)
	
	temp = open('test.out')
	ret = temp.read()
	if (ret):
		print "String is accepted"
		#print ret
		ret = ret.split("\n")
		print "".join([x.split()[3] for x in ret[:-2]]).replace("<spc>", " ")
	else:
		print "String is rejected"

	# find out if the user wants to continue
	temp = raw_input("Please type y to test another string, n to exit: ")
	if (temp <> "y"): 
		more = False








	
