#!/usr/bin/python

# File: newVM.py
# Edited: 19/07/2015
# Jose Carlos Ramirez
# TFG Unizar
# Creates a fixed VM with the required initial settings

# Prerequisites: python-dmidecode, cd-drive, acpidump, vsftpd: apt-get install python-dmidecode libcdio-utils acpidump vsftpd

# Calls to antivmdetect.py, prepareFTPserver.py, requirements.py and cuckooMods.py
# DO NOT RUN THIS AS SUPERUSER it will create the VM file inside /root
# If another user have a file with the same name as this ones in tmp, it could not create it

import os
import textwrap
import sys
import time
import re
import subprocess

# Values
RAM="2000"
HDD="70000"
nCores="3"
file_outPut="/tmp/newVM_output.txt"
host_ip="192.168.56.1"
guest_ip="192.168.56.101"
guest_primary_dns="208.67.222.222"
ftp_port="21"

######## Functions ##############################
def checkOutP (file_name='/tmp/newVM_output.txt', target='vboxnet0'):
	file=open(file_name, 'r')
	text=file.read()
	file.close()
	try:
		re.search(target, text).group(0)
		return True
	except:
		return False
##################################################
'''#Add user
  sudo adduser  -gecos "" ${CUCKOO_USER}
  sudo usermod -G vboxusers ${CUCKOO_USER}
sudo usermod -g sudo cuckoo
'''
 

# Wellcome
print textwrap.dedent("""\


	 _________________________________
	|CREATE FIXED VM FOR CUKOO USAGE
	|SPECIFICATIONS:                
	|	RAM: """+RAM+"""		
	|	HDD: """+HDD+"""		
	|	CPU CORES:"""+nCores+"""		
	|	NETWORK: HOST-ONLY		
	|	OS: WINDOWS XP 		
	|___________________________________
	""")
	
print "Wellcome! "
vm_name="'"+raw_input("	-Write the name of you VM: ")+"'"
absolute_path=raw_input("	-Please, write down the absolute path of the ISO file of the OS: ")

proc=subprocess.Popen(["whoami"], stdout=subprocess.PIPE)#, shell=True) if we wanted to use pipes between process and things like that
(_stdout, _stderr)=proc.communicate()
personal_folder="/home/"+_stdout[0:len(_stdout)-1]+"/VirtualBox\ VMs" #taking the \n out
print personal_folder

print "[*] Creating the VM named "+vm_name
os.system("VBoxManage createvm --name "+vm_name+" --register > "+file_outPut)
os.system("VBoxManage modifyvm "+vm_name+" --memory "+RAM+" --acpi on --ioapic on --boot1 dvd --cpus "+nCores+" --ostype  WindowsXP > "+file_outPut)

# If Vboxnet0 exists it only changes the @IP. If not, create it
os.system("vboxmanage list hostonlyifs > "+file_outPut)
if checkOutP():
	os.system("vboxmanage hostonlyif ipconfig vboxnet0 --ip "+host_ip+" 2> "+file_outPut)
else:	
	os.system("vboxmanage hostonlyif create ipconfig vboxnet0 --ip 192.168.56.1 2> "+file_outPut)
	#Check if the instruccion has been finished
	while not checkOutP(target='100%'):
		pass

os.system("vboxmanage modifyvm "+vm_name+" --nic1 hostonly --hostonlyadapter1 vboxnet0 > "+file_outPut) 

# Attach storage, add an IDE controller with a CD/DVD drive attached
os.system("VBoxManage storagectl "+vm_name+" --name 'IDE Controller' --add ide > "+file_outPut)
print "VBoxManage createhd --filename "+personal_folder+"/"+vm_name+".vdi --size "+HDD+" --format vdi > "+file_outPut
os.system("VBoxManage createhd --filename "+personal_folder+"/"+vm_name+".vdi --size "+HDD+" --format vdi > "+file_outPut)
os.system("VBoxManage storageattach "+vm_name+" --storagectl 'IDE Controller' --port 0 --device 0 --type hdd --medium  "+personal_folder+"/"+vm_name+".vdi > "+file_outPut)
os.system("VBoxManage storageattach "+vm_name+" --storagectl 'IDE Controller' --port 1 --device 0 --type dvddrive --medium "+absolute_path+" > "+file_outPut)

# FTP
print "[*] Preparing the FTP server"
os.system("sudo python prepareFTPserver.py "+host_ip+" "+ftp_port)
raw_input("	-If you have not copied the chosen files to the ftp folder, please do it now (/srv/ftp). Press ENTER when ready:")

#### AntiVM Detect execution
os.system("sudo python antivmdetect.py "+vm_name+" "+guest_ip+" "+host_ip+" "+guest_primary_dns)
# Executes the bash file
sh_file=open('/tmp/vboxmods.sh', 'r')
line=sh_file.readline()
while line!="":
	os.system(line)
	line=sh_file.readline()
####

# Installation
os.system("vboxmanage startvm "+vm_name)
raw_input("[*] Please follow the Guest OS installation until the end, then press ENTER:")
raw_input("	-Is the installation finished?")
print """
[*] Your guest OS is ON:
	-Open Internet explorer or the Windows file explorer
	-Type: ftp://anonymous:@"""+host_ip+""":"""+ftp_port+"""
	-Drag all your files to the Guest's file system"""
raw_input("Press ENTER to continue:")


snap_name=raw_input("	Please enter snapshot's name: ")
os.system('vboxmanage snapshot '+vm_name+' take '+snap_name+' --pause')


print "Now the VM will close, press ENTER when ready:"
raw_input()
# Shutting down the VM
os.system("vboxmanage controlvm "+vm_name+" poweroff 2> "+file_outPut)
# Check if the instruccion has been finished
while not checkOutP(target='100%'):
	pass

# Install cuckoo and dependencies
if raw_input(" Do you have Cuckoo and it's dependancies already installed?: (Y/N)").upper()!="Y":
	os.system('sudo python requirements.py | tee req_output.txt')

# Cuckoo modifications for the new VM
tag_list=raw_input('Write down a list of tags for cuckoo to add to this VM profile. Separated with commas (a,b,c,d): ')
os.system('sudo python cuckooMods.py '+host_ip+' '+guest_ip+' '+vm_name+' '+snap_name+' '+tag_list)

exit()
