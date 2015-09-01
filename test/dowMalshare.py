#!/usr/bin/python

import os

api_key='2dc7f8d97879445c1af7f4cce3b9f9063c8f9e5b0fe541964568302ad5f98051'
url='http://malshare.com/api.php?api_key='+api_key+'&action=details&hash='+_hash
hash_list=[]
hash_file_name=''
hash_file=open(hash_file_name,'r')
sources_list=[]
current_hash=hash_file.readline()
while current_hash!='':
	hash_list.append(current_hash)
	current_hash=hash_file.readline()

for _hash in hash_list:
	url='http://malshare.com/api.php?api_key='+api_key+'&action=details&hash='+_hash
	#get source form html
	
for source in source_list:	
	os.system('wget '+source)

