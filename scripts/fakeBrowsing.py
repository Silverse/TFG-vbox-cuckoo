#!/usr/bin/python

# File: fakeBrowsing.py
# Jose Carlos Ramirez
# TFG Unizar

# To be run inside the Guest.  The pre-build IE does not open nothing
# Some info is for spanish

import os
import subprocess
import time
import random
import string

######################### Functions ####################
# Creates a certain number of files (random names) in each folder
def populateFolder(folder, n_files, name_size):
	file_list=[]
	name=''
	content=''
	for n in range(n_files):
		for i in range(name_size):
			name+=random.choice(string.ascii_letters+string.digits)  #random 
		file_list.append(name)
		name=''
			
	for file_name in file_list:
		size=random.randint(100,1000)
		for k in range(size):
			content+=random.choice(string.ascii_letters+string.digits) #random content
		_file=open(folder+"\\"+file_name, 'w')
		_file.write(content)
		_file.close()
	
	return
# Creates an ordered list of hour:minute
def timeList(n):
	# Get current time
	proc=subprocess.Popen(["time", '/t'], stdout=subprocess.PIPE, shell=True)
	(_stdout, _stderr)=proc.communicate()
	_time=_stdout[:-2].split(':') #hours:minutes taking out \r\n
	int_time=[int(_time[0]),int(_time[1])]
	# Populate list
	time_list=[]
	new_time=[1,2]
	for i in range(n):
		if int_time[0]-i < 0: 
			new_time[0]=23
		else:
			new_time[0]=int_time[0]-i
		if int_time[1]-i < 0:
			new_time[1]=59
		else: 
			new_time[1]=int_time[1]-i		
		time_list.append(str(new_time[0])+':'+str(new_time[1]))
	
	return time_list
# Creates an ordered list of day/month/year
def dateList(n):
	# Get current date
	proc=subprocess.Popen(["date", '/t'], stdout=subprocess.PIPE, shell=True)
	(_stdout, _stderr)=proc.communicate()
	date=_stdout[:-2].split('/') #day/month/year, in my system, taking out \r\n
	int_date=[int(date[0]),int(date[1]),int(date[2])]
	# Pupulate list
	date_list=[]
	new_date=[1,2,3]
	for i in range(n):
		if int_date[0]-i <= 0: #goes one month back
			new_date[0]=28
			if int_date[1]-1 <= 0: #goes one year back
				new_date[1]=12
				new_date[2]=int_date[2]-1
			else:
				new_date[1]=int_date[1]-1
		else:
			new_date[0]=int_date[0]-i
		if int_date[1]-i <= 0:
			new_date[1]=12		
		else:
			new_date[1]=int_date[1]-i	
		date_list.append(str(new_date[0])+'/'+str(new_date[1])+'/'+str(int_date[2]))
	
	return date_list
# Opens Firefox to visit some webs and then closes it, repear it each time of each date
def visitWeb(date_list, time_list, web_list):
	open_IE="start /d "" firefox.exe "#+URL
	close_all_IE="TASKKILL /F /IM firefox.exe /T \r\n"
	# Every time it changes the time, it opens all the websites, and closes them
	for date in date_list[::-1]:
		os.system("date "+date+"\r\n")
		for _time in time_list:
			os.system('time '+_time+'\r\n') 
			for web in web_list:
				os.system(open_IE+web+'\r\n')
				time.sleep(1)
			os.system(close_all_IE)
	
	return
#######################################################

def main():
	n_times=3
	n_files=10
	name_size=8
	
	personal_folder=os.getcwd()
	while personal_folder[len(personal_folder)-1] != '\\':
		personal_folder=personal_folder[:-1]

	folder_list=[personal_folder+"Cookies",
			personal_folder+"Mis Documentos",#my documents
			personal_folder+"Escritorio",#desktop
			'C:\\WINDOWS\Temp']
	web_list=["https://www.facebook.com/", 
			"https://www.twitter.com", 
			"https://login.live.com", 
			"https://www.google.es/search?q=busqueda+de+ejemplo"]
	
	# Fake browsing	
	date_list=dateList(n_times)
	time_list=timeList(n_times)
	visitWeb(date_list, time_list, web_list)
		
	# Go back to the original date/time
	os.system('time '+time_list[0]+'\r\n')
	os.system("date "+date_list[0]+"\r\n")

	# Populate files
	for folder in folder_list:
		populateFolder(folder, n_files, name_size)

	return
		
main()		
exit(0)
