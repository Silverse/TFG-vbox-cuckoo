#!/usr/bin/python
import os
import re
import time
import pyautogui
import glob

path_src=os.getcwd()+'/sources/'
path_smp=os.getcwd()+'/samples/'

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'   
    
def getTable(file_name, start, end):
	_file=open(path_src+file_name, 'r')
	inside=False
	table=''
	line=_file.readline()
	while line!='':
		if inside:
			table+=line			
		try:
			re.search(start,line).group(0)
			inside=True
		except:
			try:
				re.search(end, line).group(0)
				inside=False
			except:
				pass
		line=_file.readline()		
	_file.close()
	_file=open(path_src+'TABLE '+file_name, 'w')
	_file.write(table)
	_file.close()
	return
def getRows(file_name,patron):
	new_row=False
	rows=[]
	r=''
	_file=open(file_name, 'r')
	_file.readline() #header
	_file.readline() #header
	line=_file.readline()
	while line!='':
		try:
			re.search(patron, line).group(0)
			new_row=True
		except:
			new_row=False
		if new_row:
			rows.append(r)
			r=''
		else:
			r+=line
		line=_file.readline()
	_file.close()
	
	return	rows
	
def main():	
	url='http://malc0de.com/database/index.php?&search=US&page='
	total_pages=500#7859
	op=raw_input(" 1) Download HTMLs\n 2) Process HTMLs\n 3) Both\n--> ")
	time.sleep(2)
	if (op=='1')|(op=='3'):
		print "Downloading HTMLs"
		for n in range(total_pages)[402::]:			
			os.system('firefox "'+url+str(n)+'"')
			time.sleep(2)
			pyautogui.rightClick(900,400)
			for i in range(3):
				pyautogui.press('down')
			pyautogui.press('enter')
			pyautogui.press('rigth')
			_path=path_src+str(n)
			for i in _path.split('/'):
				pyautogui.keyDown('shift')  
				pyautogui.press('/')
				pyautogui.keyUp('shift') 
				pyautogui.typewrite(i) 
			pyautogui.press('enter')
			while not os.path.exists(path_src+str(n)+'.html'): #wait until it's saved
				pass
			#close windows	
			#os.system('''wmctrl -ic "$(wmctrl -l | grep 'Mozilla Firefox' | tail -1 | awk '{ print $1 }')"''')
			#time.sleep(1)
			#os.system('firefox &')			
	if (op=='2')|(op=='3'):
		print "Processing HTMLs"
		for n in range(total_pages)[1:]:
			file_name=str(n)+'.html'
			table=getTable(file_name, '<table class="prettytable">', '</table>')
			rows=getRows(path_src+'TABLE '+file_name, '<tr')
			for r in rows:
				link=''
				link_split=r.split('<td>')[2].split('</td>')[0].split('<br>')
				for l in link_split:
					link+=l
				name=link.split('/')[-1]
				try:
					re.match('([A-Za-z0-9*+.?_\-$%#@() ]+).exe', name).group(0)
					if not os.path.exists(path_smp+name):
						print bcolors.OKGREEN+"\nNew "+name+bcolors.ENDC
						os.system('wget --tries=1 --connect-timeout=5 -P '+path_smp+' '+link)
					else:
						print bcolors.FAIL+"Exists "+name+bcolors.ENDC
				except:
					pass
	
	#Postprocssing
	for i in glob.glob('*'):
		try:
			re.search('.exe', i).group(0)		
		except:
			os.system('sudo rm '+str(i))
	n=0
	for i in glob.glob('*'):
			os.system('sudo mv '+str(i)+' s_'+str(n)+'.exe')
			n+=1
			
	return
			
			

main()
exit(1)
