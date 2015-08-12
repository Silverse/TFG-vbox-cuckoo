#!/usr/bin/python
#-*-coding: 850-*-

# File: main.py
# Jose Carlos Ramirez
# TFG Unizar

# General management and run every other script
# Calls to: 

import os
import subprocess
import re

# Values
RAM="2000"
HDD="70000"
nCores="3"
file_output="/tmp/newVM_output.txt"
host_ip="192.168.58.1" 
default_host_ip="192.168.56.1"
guest_ip="192.168.58.25" #default 192.168.56.101
guest_primary_dns="208.67.222.222"
ftp_port="21"

#If the output file exists and it was created by a different user, the script won't be able to interact with it (permission denied)
proc=subprocess.Popen(["ls", '/tmp/'], stdout=subprocess.PIPE)#, shell=True) if we wanted to use pipes between process and things like that
(_stdout, _stderr)=proc.communicate()
try:
	comp_regex=re.compile(file_output[4:])
	re.search(comp_regex, _stdout).group(0)
	os.system('sudo rm '+file_output) 
except: #does not exists
	pass


print '''
	#############################################################
	####### TFG Ingeniría de Tecnologías y Servicios de   #######
	####### la Telecomunicación, telemática.	      #######
	####### Alumno: José Carlos Ramírez Vega, 628545      #######
	####### Tutor: Antonio Sanz Alcober		      #######
	####### Ponente: José Luis Salazar Riaño	      #######
	####### Título: Mejora de la detección de malware     #######
	####### mediante la modificación profunda de sistemas #######
	####### de sandboxing.				      #######
	#############################################################
'''

if raw_input(' -Do you have a user ready for cuckoo usage? (Y/N)').upper()=='Y':
	user_name=raw_input('	-Please write the user name: ')
else:
	user_name=raw_input('	-Please chose a user name: ')
	os.system('''
		sudo adduser  -gecos "" '''+user_name+'''
		sudo usermod -G vboxusers '''+user_name+'''
		sudo usermod -g sudo '''+user_name+
		 '''\n''')
	print '\n	-Created: '+user_name+' part of vboxusers and superusers'
	print '\n -Run again the script in the new user.'
	exit()

vm_name="'"+raw_input("\n -Write the name of your VM: ")+"'"
absolute_path=raw_input(" -Please, write down the absolute path of the ISO file of the OS: \n\t")
snap_name=raw_input(" -Please chose a snapshot's name: ")

# Install cuckoo and dependencies
print "\n [*] Installing Cuckoo, dependancies, and side programs"
os.system('python requirements.py '+host_ip)

# AntiVMdetect execution
os.system("sudo python antivmdetect.py "+vm_name+" "+guest_ip+" "+host_ip+" "+guest_primary_dns)

# FTP, default @IP
print "\n [*] Preparing the FTP server (default @IP)"
os.system("sudo python prepareFTPserver.py "+default_host_ip+" "+ftp_port)
os.system('sudo cp '+os.getcwd()+'/requirements/cuckoo/agent/agent.py /srv/ftp')
os.system('sudo service vsftpd restart')

# VM creation
print "\n [*] Creating a VirtualBox's VM named "+vm_name
os.system('python newVM-simple.py '+RAM+' '+HDD+' '+nCores+' '+file_output+' '+host_ip+' '+guest_ip+' '+guest_primary_dns+' '+ftp_port+' '+vm_name+' '+absolute_path+' '+snap_name+' '+default_host_ip)

# FTP, current @IP
print "\n [*] Preparing the FTP server (current @IP)"
os.system("sudo python prepareFTPserver.py "+host_ip+" "+ftp_port)

# Cuckoo modifications for the new VM
tag_list=raw_input(''''
 [*] The Cuckoo configuration will be modified to suit the VM
	Write down a list of tags for cuckoo to add to this VM profile. Separated with white spaces (e.g: windows_xp office_2003 flash_1.2): 
''')
os.system('python cuckooMods.py '+host_ip+' '+guest_ip+' '+vm_name+' '+snap_name+' '+tag_list)

print "\n [*] The end. "

exit()
