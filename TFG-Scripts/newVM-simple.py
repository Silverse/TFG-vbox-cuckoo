#!/usr/bin/python

# File: newVM.py
# Edited: 19/07/2015
# Jose Carlos Ramirez
# TFG Unizar

# Creates a fixed VM with the required initial settings

# Prerequisites: python-dmidecode, cd-drive, acpidump, vsftpd: apt-get install python-dmidecode libcdio-utils acpidump vsftpd

# Calls to antivmdetect.py, prepareFTPserver.py, requirements.py and cuckooMods.py
# DO NOT RUN THIS AS SUPERUSER it will create the VM file inside /root
# Argumento 1: RAM memory in MegaBytes
# Argumento 2: HDD's size in MegaBytes
# Argumento 3: Number of processors
# Argumento 4: Name of the temporary output file
# Argumento 5: Host @IP
# Argumento 6: Guest @IP
# Argumento 7: Guest's primary DNS @IP
# Argumento 8: FTP port
# Argumento 9: Personal folder's path



import os
import textwrap
import re
import sys
import subprocess

# Values
RAM=str(sys.argv[1])
HDD=str(sys.argv[2])
nCores=str(sys.argv[3])
file_outPut=str(sys.argv[4])
host_ip=str(sys.argv[5])
guest_ip=str(sys.argv[6])
guest_primary_dns=str(sys.argv[7])
ftp_port=str(sys.argv[8])
vm_name=str(sys.argv[9])
absolute_path=str(sys.argv[10])
snap_name=str(sys.argv[11])

######## Functions ##############################
def checkOutP (file_name=file_outPut, target='vboxnet0'):
	file=open(file_name, 'r')
	text=file.read()
	file.close()
	try:
		re.search(target, text).group(0)
		return True
	except:
		return False
##################################################

# This piece of code sould be in main.py, but the "\ " is not passed correctly as an argument, so it doesn't work in that way
proc=subprocess.Popen(["whoami"], stdout=subprocess.PIPE)#, shell=True) if we wanted to use pipes between process and things like that
(_stdout, _stderr)=proc.communicate()
personal_folder="/home/"+_stdout[0:len(_stdout)-1]+'/VirtualBox\ VMs' #taking the \n out

# VM creation
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
raw_input("	-If you have not copied the chosen files to the ftp folder, please do it now (/srv/ftp). Press ENTER when ready:")

#### AntiVM Detect execution
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
	-Drag all your files to the Guest's file system
	-Install Python and PIL, then run vboxmods.bat and finally agent.py"""
raw_input("Press ENTER to continue:")

# Taking the snapshot
os.system('vboxmanage snapshot '+vm_name+' take '+snap_name+' --pause')

print "Now the VM will close, press ENTER when ready:"
raw_input()
# Shutting down the VM
os.system("vboxmanage controlvm "+vm_name+" poweroff 2> "+file_outPut)
# Check if the instruccion has been finished
while not checkOutP(target='100%'):
	pass
# Removing install media
os.system('vboxmanage modifyvm '+vm_name+' --dvd none > '+file_outPut)
# Restoring the vm state
os.system('vboxmanage snapshot '+vm_name+' restorecurrent > '+file_outPut)

print textwrap.dedent("""
  __________________________________
 |FIXED VM READY FOR CUKOO USAGE.
 |SPECIFICATIONS:   
 |	NAME: """+vm_name+"""             
 |	RAM: """+RAM+"""		
 |	HDD: """+HDD+"""		
 |	CPU CORES:"""+nCores+"""		
 |	NETWORK: HOST-ONLY		
 |	OS: WINDOWS XP 	
 |	SNAPSHOT: """+snap_name+"""	
 |___________________________________
	""")

exit()
