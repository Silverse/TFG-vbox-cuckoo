#!/usr/bin/python

# File: fakeBrowsing.py
# Edited: 11/08/2015
# Jose Carlos Ramirez
# TFG Unizar

# Should be run inside the Guest.  The pre-build IE does not open nothing

import os
import subprocess
import time

# Get current date
proc=subprocess.Popen(["date", '/t'], stdout=subprocess.PIPE, shell=True)
(_stdout, _stderr)=proc.communicate()
date=_stdout[:-2].split('/') #day/month/year, in my system, taking out \r\n
int_date=[int(date[0]),int(date[1]),int(date[2])]

# Get current time
proc=subprocess.Popen(["time", '/t'], stdout=subprocess.PIPE, shell=True)
(_stdout, _stderr)=proc.communicate()
_time=_stdout[:-2].split(':') #hours:minutes taking out \r\n
int_time=[int(_time[0]),int(_time[1])]


web_list=["https://www.facebook.com/", "https://www.twitter.com", "https://login.live.com", "https://www.google.es/search?q=busqueda+de+ejemplo"]

open_IE="start /d "" firefox.exe "#+URL
close_all_IE="TASKKILL /F /IM firefox.exe /T \r\n"

time_list=[]
new_time=[1,2]
for i in range(3):
	if int_time[0]-i < 0: 
		new_time[0]=23
	else:
		new_time[0]=int_time[0]-i
	if int_time[1]-i < 0:
		new_time[1]=59
	else: 
		new_time[1]=int_time[1]-i		
	time_list.append(str(new_time[0])+':'+str(new_time[1]))

date_list=[]
new_date=[1,2,3]
for i in range(3):
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
		new_time[1]=12		
	else:
		new_date[1]=int_date[1]-i	
	date_list.append(str(new_date[0])+'/'+str(new_date[1])+'/'+str(int_date[2]))

# Every time it changes the time, it opens all the websites, and closes them
for date in date_list[::-1]:
        print date
	os.system("date "+date+"\r\n")
	for _time in time_list:
		os.system('time '+_time+'\r\n') 
		for web in web_list:
			os.system(open_IE+web+'\r\n')
			time.sleep(1)
		os.system(close_all_IE)
	
# Go back to the original one
os.system('time '+time_list[0]+'\r\n')
os.system("date "+date_list[0]+"\r\n")

		
exit()
