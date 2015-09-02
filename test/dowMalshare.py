#!/usr/bin/python

import os
import urllib
import urllib2
import cookielib
	
def getFile(opener,url):
	try:
		url_file=opener.open(url)
		full_doc=url_file.read()
		return full_doc
	except urllib2.HTTPError as e:
		print('HTTPError :',e.code,url)
	except urllib2.URLError as e:
		print('URLError :',e.reason,url)
		
	return ''

def startsLogin(url):
	cookieJar = cookielib.CookieJar()
	try:
		cookie_handler= urllib2.HTTPCookieProcessor(cookieJar)
		# If this is not added, the credentials will be send in clear text
		opener=urllib2.build_opener(cookie_handler) #returns an OpenerDirector
	except urllib2.HTTPError as e:
		print('HTTPError :',e.code,url)
	except urllib2.URLError as e:
		print('URLError :',e.reason,url)
				
	return opener
	
def getData(source,previous_str,end_word):
	data_starts = source.find(previous_str)+len(previous_str) # Returns the index where the data starts
	data_ends = source[data_starts:].find(end_word)
	
	data_string = source[data_starts:][:data_ends]		
	return data_string	
	
def main():	
	api_key='2dc7f8d97879445c1af7f4cce3b9f9063c8f9e5b0fe541964568302ad5f98051'
	hash_list=[]
	hash_file_name='file.txt'
	hash_file=open(hash_file_name,'r')
	sources_list=[]
	current_hash=hash_file.readline()
	while current_hash!='':
		hash_list.append(current_hash)
		current_hash=hash_file.readline()


	for _hash in hash_list:
		url='http://malshare.com/api.php?api_key='+api_key+'&action=details&hash='+_hash
		opener=startsLogin(url)
		html=getFile(opener, url)
		data=getData(html, '"SOURCES":["', '"]}')
		sources_list.append(data)
		
		#get source form html

	for source in sources_list:	
		os.system('wget '+source)

main()
exit()
