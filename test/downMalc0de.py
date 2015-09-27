#!/usr/bin/python
import os
import re
import time
import cookielib
import urllib
import urllib2
import pyautogui
import glob

path_smp=os.getcwd()+'/samples/'
os.system('mkdir '+path_smp)

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'      
	
def toHTML(filename, data):
	out_file=open(filename, 'w')
	out_file.write(data) 
	out_file.close()	
	#os.system('start firefox.exe '+filename)
	return
	
def startsLogin(url):
	cookieJar = cookielib.CookieJar()
	try:
		cookie_handler= urllib2.HTTPCookieProcessor(cookieJar)
		# If this is not added, the credentials will be send in clear text
		https_handler=urllib2.HTTPSHandler() 
		opener=urllib2.build_opener(cookie_handler, https_handler) #returns an OpenerDirector
		# Necessary for HTS
		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0)')] 	
	except urllib2.HTTPError as e:
		print('HTTPError :',e.code,url)
	except urllib2.URLError as e:
		print('URLError :',e.reason,url)
				
	return opener 

def sendPost(opener,url):
		
	return opener.open(url)    
    
def getTable(response, start, end):
	inside=False
	table=''
	
	line_list=response.split('\n')	
	for line in line_list:
		if inside:
			table+=line+'\n'				
		try:
			re.search(start,line).group(0)
			inside=True
		except:
			try:
				re.search(end, line).group(0)
				inside=False
			except:
				pass		
	return table
	
def getRows(table, patron):
	new_row_bool=False
	row_list=[]
	new_row=''

	for line in table.split('\n')[2:]: #first two lines is header
		try:
			re.search(patron, line).group(0)
			new_row_bool=True
		except:
			new_row_bool=False
		if new_row_bool:
			row_list.append(new_row)
			new_row=''
		else:
			new_row+=line
			
	return	row_list
	
def main():	
	url='http://malc0de.com/database/index.php?&search=US&page='
	total_pages=7859
	n_files=0
	n_total_files=0
	
	print " Starts working!"	
	
	for n in range(total_pages)[2:]:	
		n_files=0
		login_url=url+str(n)
		
		print bcolors.OKGREEN+"\n Downloading HTML "+str(n)+bcolors.ENDC	
		# Get in the site
		opener=startsLogin(login_url)
		response=sendPost(opener, login_url).read()
		#toHTML(path_smp+str(n)+'.html',response)			
			
		print bcolors.OKGREEN+" Process HTML "+str(n)+bcolors.ENDC
		table=getTable(response, "<table class='prettytable'>", '</table>')
		row_list=getRows(table, '<tr')
		for row in row_list:
			link=''
			link_split=row.split('<td>')[2].split('</td>')[0].split('<br/>')
			for l in link_split:
				link+=l
			name=link.split('/')[-1]
			
			try:
				re.match('([A-Za-z0-9*+.?_\-$%#@() ]+).exe', name).group(0)
				if not os.path.exists(path_smp+name):					
					os.system('wget --tries=1 --connect-timeout=5 -P '+path_smp+' '+link+' > /dev/null 2>&1')
					if os.path.exists(path_smp+name):
						print bcolors.OKGREEN+"\tNew "+bcolors.ENDC+name
						n_files+=1
						n_total_files+=1
				else:
					print bcolors.FAIL+"\tExists "+bcolors.ENDC+name
					pass
			except:
				pass			
		print " Files from this page "+str(n_files)+", total files "+bcolors.OKGREEN+str(n_total_files)+bcolors.ENDC
		'''
		#Postprocssing
		for i in glob.glob(path_smp+'*'):
			try:
				re.search('.exe', i).group(0)		
			except:
				os.system('sudo rm '+str(i))
		n=0
		for i in glob.glob(path_smp+'*'):
				os.system('sudo mv '+str(i)+' s_'+str(n)+'.exe')
				n+=1
		# check if "file <file>" returns PE32 executable
		'''	
	return
			
			

main()
exit(1)
