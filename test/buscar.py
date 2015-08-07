#!/usr/bin/python

import re

f=open('regkeys.txt', 'r')
f2=open('out.txt', 'w+')
line=f.readline()
line=line.upper()
while line!='':
	line=f.readline()
	line=line.upper()
	try:
		re.search('VBOX', line).group(0)
		f2.write(line)
	except:
		pass
	try:
		re.search('VIRTUAL', line).group(0)
		f2.write(line)
	except:
		pass
	try:
		re.search('VIRTUALBOX', line).group(0)
		f2.write(line)
	except:
		pass
f.close()
f2.close()
exit()
