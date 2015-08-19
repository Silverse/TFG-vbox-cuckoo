#!/usr/bin/python

# File: newVM.py
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
# Argumento 9: VM's name
# Argumento 10: Personal folder's path
# Argumento 11: Snapshot's name
# Argumento 12: Default host's @IP


import os
import textwrap
import re
import sys
import subprocess

class bcolors:
    HEADER = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

######## Functions ####################
def checkOutP(file_name, target): 
	file=open(file_name, 'r')
	text=file.read()
	file.close()
	try:
		re.search(target, text).group(0)
		return True
	except:
		return False
#######################################
def main(RAM, HDD, nCores, file_outPut, host_ip, guest_ip, 
		guest_primary_dns, ftp_port, vm_name, absolute_path, snap_name, default_host_ip, path_logs):
	
	# This piece of code sould be in main.py, but the "\ " is not passed correctly as an argument, so it doesn't work in that way
	proc=subprocess.Popen(["whoami"], stdout=subprocess.PIPE)#, shell=True) if we wanted to use pipes between process and things like that
	(_stdout, _stderr)=proc.communicate()
	personal_folder="/home/"+_stdout[:-1]+'/VirtualBox\ VMs' #taking the \n out

	# VM creation
	os.system("VBoxManage createvm --name '"+vm_name+"' --register > "+file_outPut)
	os.system("VBoxManage modifyvm '"+vm_name+"' --memory "+RAM+" --acpi on --ioapic on --boot1 dvd --cpus "+nCores+" --ostype  WindowsXP > "+file_outPut)

	# If Vboxnet0 exists it only changes the @IP. If not, create it
	os.system("vboxmanage list hostonlyifs > "+file_outPut)
	if checkOutP(file_outPut, 'vboxnet0'): # The first time it's attached to the default address
		os.system("vboxmanage hostonlyif ipconfig vboxnet0 --ip "+default_host_ip+" 2> "+file_outPut)
	else:	
		os.system("vboxmanage hostonlyif create ipconfig vboxnet0 --ip "+host_ip+" 2> "+file_outPut)
		#Check if the instruccion has been finished
		while not checkOutP(file_outPut, '100%'):
			pass

	os.system("vboxmanage modifyvm '"+vm_name+"' --nic1 hostonly --hostonlyadapter1 vboxnet0 > "+file_outPut) 

	# Attach storage, add an IDE controller with a CD/DVD drive attached
	os.system("VBoxManage storagectl '"+vm_name+"' --name 'IDE Controller' --add ide > "+file_outPut)
	os.system("VBoxManage createhd --filename "+personal_folder+"/"+vm_name.replace(' ', '_')+".vdi --size "+HDD+" --format vdi > "+file_outPut)
	os.system("VBoxManage storageattach '"+vm_name+"' --storagectl 'IDE Controller' --port 0 --device 0 --type hdd --medium  "+personal_folder+"/"+vm_name.replace(' ', '_')+".vdi > "+file_outPut)
	os.system("VBoxManage storageattach '"+vm_name+"' --storagectl 'IDE Controller' --port 1 --device 0 --type dvddrive --medium "+absolute_path+" > "+file_outPut)

	#### AntiVM Detect execution
	# Executes the bash file
	sh_file=open(path_logs+'/vboxmods-'+vm_name.replace(' ', '_')+'.sh', 'r')
	line=sh_file.readline()
	while line!="":
		os.system(line)
		line=sh_file.readline()
	####
	# FTP warning
	raw_input("\n -If you have not copied the chosen files to the ftp folder, please do it now (/srv/ftp). Press ENTER when ready:")
	
	# FTP - needs the virtualIF up...
	os.system('sudo service vsftpd start > '+path_logs+'/ftp.log') # Service's Up!			
	#Sometimes it does not end in running state, not sure why so... Check!
	_file=open(path_logs+'/ftp.log', 'r')
	line=_file.readline()
	try:
		re.search('pre-start', line).group(0)
		print bcolors.WARNING+"WARNING: vsftp did not started properly"+bcolors.ENDC
	except:
		pass
	_file.close()
	os.system('rm '+path_logs+'/ftp.log')
	
	# Installation
	os.system("vboxmanage startvm '"+vm_name+"'")
	raw_input(bcolors.OKGREEN+"\n [*]"+bcolors.ENDC+" Please follow the Guest OS installation until the end, then press ENTER:")
	raw_input("	-Is the installation finished?")
	print bcolors.OKGREEN+' [*]'+bcolors.ENDC+""" Your guest OS is ON:
	- Open Internet explorer or the Windows file explorer
	- Type: ftp://anonymous:@"""+default_host_ip+""":"""+ftp_port+"""
	- Copy the CopyThisOne! folder to the Guest's file system
	- Copy and install all the extra-software you want
	- Install Python and PIL, then run vboxmods.bat."""
	raw_input(" Press ENTER to continue:")

	# Changed to the current @IP
	os.system("vboxmanage hostonlyif ipconfig vboxnet0 --ip "+host_ip+" 2> "+file_outPut)
	# Removing install media
	os.system('vboxmanage modifyvm "'+vm_name+'" --dvd none > '+file_outPut)

	#For WMI patch to work...
	# Rebooting the VM
	os.system("vboxmanage controlvm '"+vm_name+"' poweroff 2> "+file_outPut)
	os.system("vboxmanage startvm '"+vm_name+"'")
	raw_input("\t- Run vboxmods.bat again\n\t- Finally run fakeBrowsing.py (and wait) and agent.pyw\n\t- Just before continue, run humanMimic.exe\n Press ENTER to continue:")

	# Taking the snapshot
	os.system('vboxmanage snapshot "'+vm_name+'" take "'+snap_name+'" --pause')

	print " -Now the VM will close, press ENTER when ready:"
	raw_input()
	# Shutting down the VM
	os.system("vboxmanage controlvm '"+vm_name+"' poweroff 2> "+file_outPut)
	# Check if the instruccion has been finished
	while not checkOutP(file_outPut, '100%'):
		pass
	# Restoring the vm state
	os.system('vboxmanage snapshot "'+vm_name+'" restorecurrent > '+file_outPut)

	print textwrap.dedent(bcolors.OKGREEN+"""
	 __________________________________
	 |FIXED VM READY FOR CUKOO USAGE.
	 |SPECIFICATIONS:   
	 |	NAME: """+vm_name+"""             
	 |	RAM: """+RAM+"""		
	 |	HDD: """+HDD+"""		
	 |	CPU CORES:"""+nCores+"""		
	 |	NETWORK: HOST-ONLY ("""+host_ip+""")
	 |		-IP:"""+guest_ip+"""		
	 |	OS: WINDOWS XP 	
	 |	SNAPSHOT: """+snap_name+"""	
	 |___________________________________
		"""+bcolors.ENDC)
	return

