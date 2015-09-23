#!/usr/bin/python

import os
import subprocess
import re
import time


def checkVM(name):
	global last_out
	
	_in=False
	os.system('vboxmanage list -l vms | grep -e ^Name: -e ^State > hi.txt')
	_f=open('hi.txt', 'r')	
	dump=_f.read().split('\n')
	_f.close()
	os.system('rm hi.txt')
	
	for d in dump:		
		if _in:
			out=d[17:].split('(')[0][:-1]	
			if out!=last_out:
				print out
				last_out=out
			return out		
		try:
			re.search(name, d).group()
			_in=True
		except:
			pass
	return ''		

def main():
	sel=raw_input('Select raw or hard: ')
	global last_out
	last_out=''
	
	if sel=='raw':
		name='test_raw'
		path='raw'
		
	elif sel=='hard':
		name='test_fixed'
		path='hardened'
		
	print name	
	
	for _file in range(100)[87:]:		
		while (checkVM(name)!='powered off')&(checkVM(name)!='saved'):
			pass
			
		os.system('vboxmanage snapshot '+name+' restorecurrent')		
		os.system('python /media/cuckoo/Data/test/'+path+'/requirements/cuckoo/utils/submit.py /media/cuckoo/Data/test/SAMPLES!!/samples/s_'+str(_file)+'.exe')
		time.sleep(10)
		
	return
	
	
main()
exit()
