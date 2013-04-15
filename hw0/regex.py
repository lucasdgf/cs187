## search for pattern 'iii' in string piiig

import re

match = re.search(r'iii', 'piiig')
print match.group()

match = re.search(r'..g', 'piiig')
print match.group()

match = re.search(r'\d\w', 'l0cas!')
print match.group()

match = re.search(r'pi+', 'piiigpigpiiiiiiiiiiiiig')
print match.group()

match = re.search(r'\d\s*\d\s*\d', 'cc1 2          3xx')
print match.group()

match = re.search(r'iii', 'piiig')
print match.group()

str = 'ldgf@msn.com, lucas, lucasdgf@gmail.com,'
match = re.findall(r'[\w\.-]+@[\w\.-]+', str)
for email in match:
	print email