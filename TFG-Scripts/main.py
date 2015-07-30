#!/usr/bin/python
#-*-coding: 850-*-

# File: main.py
# Edited: 19/07/2015
# Jose Carlos Ramirez
# TFG Unizar

# General management and run every other script
# Calls to: 

import os
import subprocess

# Values
RAM="2000"
HDD="70000"
nCores="3"
file_output="/tmp/newVM_output.txt"
host_ip="192.168.56.1"
guest_ip="192.168.56.101"
guest_primary_dns="208.67.222.222"
ftp_port="21"

'''
#Add user
  sudo adduser  -gecos "" ${CUCKOO_USER}
  sudo usermod -G vboxusers ${CUCKOO_USER}
sudo usermod -g sudo cuckoo
'''

os.system('sudo rm '+file_output) #If the file exists and it was created by a different user, the script won't be able to interact with it

print u'''
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
vm_name="'"+raw_input("	-Write the name of your VM: ")+"'"
absolute_path=raw_input("	-Please, write down the absolute path of the ISO file of the OS: ")
snap_name=raw_input("	-Please enter snapshot's name: ")

# Install cuckoo and dependencies
if raw_input("	-Do you have Cuckoo and it's dependancies already installed?: (Y/N)").upper()!="Y":
	print "[*] Installing Cuckoo, dependancies, and side programs"
	os.system('python requirements.py')

# AntiVMdetect execution
os.system("sudo python antivmdetect.py "+vm_name+" "+guest_ip+" "+host_ip+" "+guest_primary_dns)

# FTP
print "[*] Preparing the FTP server"
os.system("sudo python prepareFTPserver.py "+host_ip+" "+ftp_port)
os.system('sudo cp '+os.getcwd()+'/requirements/cuckoo/agent/agent.py /srv/ftp')

# VM creation
print "[*] Creating a VirtualBox's VM named "+vm_name
os.system('python newVM-simple.py '+RAM+' '+HDD+' '+nCores+' '+file_output+' '+host_ip+' '+guest_ip+' '+guest_primary_dns+' '+ftp_port+' '+vm_name+' '+absolute_path+' '+snap_name)

# Cuckoo modifications for the new VM
tag_list=raw_input(''''
[*] The Cuckoo configuration will be modified to suit the VM
	Write down a list of tags for cuckoo to add to this VM profile. Separated with white spaces (e.g: windows_xp office_2003 flash_1.2): 
''')
os.system('python cuckooMods.py '+host_ip+' '+guest_ip+' '+vm_name+' '+snap_name+' '+tag_list)

exit()
