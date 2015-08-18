#!/usr/bin/python
#-*-coding: 850-*-

# File: main.py
# Jose Carlos Ramirez
# TFG Unizar

# General management and run every other script

import os
import subprocess
import re
import random
import textwrap
import sys
# Importing the rest of the files
sys.path.insert(0, 'scripts')
import requirements
import prepareFTPserver
import cuckooMods
import newVM

path_req=os.path.abspath('')+'/requirements'
path_cuckoo=os.path.abspath('')+'/requirements/cuckoo'
path_bin=os.path.abspath('')+'/bin'
path_scripts=os.path.abspath('')+'/scripts'
path_logs=os.path.abspath('')+'/logs'
log_name="main.log"
	
class bcolors:
    HEADER = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


	
#################### Functions ###################
# Check if there is a folder named requirements and if its weight is over a minimum
def checkIns(folder): 
	folder_size = 0
	for (path, dirs, files) in os.walk(folder):
		for _file in files:
			filename = os.path.join(path, _file)
			folder_size += os.path.getsize(filename)
	folder_size/=(1024*1024.0)
	if folder_size < 100: #Less than 100 Mb, +- the weight of a new yara+ssdeep+cuckoo
		return False
	if not os.path.isdir(folder):
		return False
	return True
# Returns the info about the VMs in the cuckoo conf file
def getVMlist(system='virtualbox'):
	output=""
	inBlock=False
	_file=open(path_req+'/cuckoo/conf/'+system+'.conf', 'r') #The first line of the doc should be [virtualbox]
	line=_file.readline() #take first line out
	line=_file.readline()	
	while line!="":		
		# Check if new block
		try:
			re.match('\[([0-9A-Za-z. ]*)]\n', line).group(0) # [something]\n will match
			inBlock=True
		except:
			pass
		if inBlock:
			output+='\t'+line #take out the extra \n
		line=_file.readline()
	return	output
# Returns a non used guest IP
def newGuestIP(default):
	ip_found=False
	vm_list=getVMlist()
	try:
		ip_list=re.findall('ip = [0-9 .]*', vm_list)
		ip_list=[element.split()[2] for element in ip_list]
		# Suposing all of them are in the 192.168.58.0 net
		last_byte=[int(element.split('.')[3]) for element in ip_list]
		while not ip_found:
			try:
				value=random.randint(2,255)
				re.search(value, last_byte)
			except:
				ip='192.168.58.'+str(value)
				ip_found=True		
		return ip
	except:
		return default
# Check if all the vms in the conf files exists
def checkVMs():
	missing_vms=[]
	cuckoo_vms=re.findall("\[([0-9A-Za-z. ]*)]\n",getVMlist())
	proc=subprocess.Popen(['vboxmanage', 'list', 'vms'], stdout=subprocess.PIPE)
	(_stdout, _stderr)=proc.communicate()
	for vm in cuckoo_vms:
		try:
			re.search('"'+vm+'"', _stdout).group(0) #It is possible to find a match with the UUID but... not likely. The quotes are for avoiding a match of 'test' with 'test32'
		except:
			missing_vms.append('"'+vm+'"')	
	return missing_vms		
# Erase a vm profile form cuckoo's conf files
def eraseVM(vm_name, system='virtualbox'):
	block_found=False
	#Opening the file for reading and writting
	conf_file=open(path_cuckoo+'/conf/'+system+'.conf', 'r') 
	tmp_file=open(path_logs+'/'+system+'-tmp.conf', 'w+')
	#The first line of the doc should be [virtualbox]
	line=conf_file.readline() #take first line out
	tmp_file.write(line)
	
	line=conf_file.readline()
	while line!="":
		try:
			re.search('machines = ',line).group(0)
			vms=line.split()[2].split(',')
			line="machines = "
			for vm in vms:
				if vm != vm_name:
					line+=vm
			line+='\n'
		except:
			pass
		if block_found:
			try: #Check if a new block is found				
				re.match('\[([0-9A-Za-z. ]*)]\n', line).group(0) # [something]\n will match
				block_found=False
			except:
				pass
		try: #Check if the target block is found
			re.search('\['+vm_name+']',line).group(0)
			block_found=True
		except:
			pass			
		if not block_found:
			tmp_file.write(line)
		line=conf_file.readline()

	conf_file.close()
	tmp_file.close()

	# Open truncate file, we are going to fill it with the tmp one
	conf_file=open(path_cuckoo+'/conf/'+system+'.conf', 'w') 
	tmp_file=open(path_logs+'/'+system+'-tmp.conf', 'r')

	new_content=tmp_file.read()
	conf_file.write(new_content)

	conf_file.close()
	tmp_file.close()
	return	
# Check if vboxnet0 is up or down
def checkVif():
	in_IF=False
	proc=subprocess.Popen(["vboxmanage", 'list',  'hostonlyifs'], stdout=subprocess.PIPE)
	(_stdout, _stderr)=proc.communicate()
	splitted=_stdout.split('\n')
	for field in splitted:
			try:
				re.search('Name:', field).group(0)
				in_IF=False
				re.search(' vboxnet0', field).group(0) #without the blank space it does not work because it caches other field
				in_IF=True
			except:
					pass
			if in_IF:
				try:
					re.search('Status:', field).group(0)
					status=field.split()[1]
				except:
					pass
	#This should start it in case it is down
	return status=="Up"
#################################################
def main():
	# Values
	RAM="2000"
	HDD="70000"
	nCores="3"
	file_output=path_logs+"/newVM.log"
	host_ip="192.168.58.1" 
	default_host_ip="192.168.56.1"
	guest_ip="192.168.58.25" #default 192.168.56.101
	guest_primary_dns="208.67.222.222"
	ftp_port="21"
	
	##Folders
	os.system('mkdir '+path_req)
	os.system('mkdir '+path_logs)
	## Wellcome
	print textwrap.dedent(bcolors.HEADER+"""
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
	"""+bcolors.ENDC)

	## Menu
	_quit=False
	menu=["\t-1) Install the dependancies and Cuckoo", 
			"\t-2) Create a new fixed VM",
			"\t-3) List the Cuckoo's VM", 
			"\t-4) Run Cuckoo and the webserver (localhost:8080)", 
			"\t-5) Close" ]	
	while not _quit:
		# Print menu
		print "\t###################### Menu ################"
		# Show in the menu if the installation is done or not
		if checkIns(path_req): 
			marked=False
		else:	
			marked=True			
		for op in menu:
			if not marked:
				print op+bcolors.OKGREEN + " [DONE]"+bcolors.ENDC
				marked=True
			else:
				print op
		try:
			selection=int(raw_input("Option's number: "))
			# Installation
			if selection == 1: 
				# New user
				if raw_input(' -Do you have a user ready for cuckoo usage? (Y/N): ').upper()=='Y':
					user_name=raw_input('\t-Please write the user name: ')
					proc=subprocess.Popen(["whoami"], stdout=subprocess.PIPE)
					(_stdout, _stderr)=proc.communicate()
					if _stdout[:-1] != user_name:
						print bcolors.FAIL + "You are not logged as this user. Please change it and run the script again"+bcolors.ENDC
						exit(1)
				else:
					user_name=raw_input('\t-Please chose a user name: ')
					os.system('''
						sudo adduser  -gecos "" '''+user_name+'''
						sudo usermod -G vboxusers '''+user_name+'''
						sudo usermod -g sudo '''+user_name+
						 '''\n''')
					print bcolors.OKGREEN + '\n\t-Created:'+bcolors.ENDC+user_name+' part of vboxusers and superusers\n-Run the script using the new user.'
					exit(1)	
				
				# Install cuckoo and dependencies
				if checkIns(path_req):
					if raw_input(bcolors.WARNING+" -The requirements folder seems to exist. Do you want to continue? (Y/N): "+bcolors.ENDC).upper()=='Y':
						print bcolors.OKGREEN + "\n [*]"+bcolors.ENDC+" Installing Cuckoo, dependancies, and side programs"
						requirements.main(host_ip, path_req, path_logs)
				else:
					print bcolors.OKGREEN + "\n [*]"+bcolors.ENDC+" Installing Cuckoo, dependancies, and side programs"
					requirements.main(host_ip, path_req, path_logs)
			# New VM
			elif selection == 2: 
				if checkIns(path_req): #Check if (probably) the dependancies are installed
					vm_name=raw_input("\n -Write the name of your VM: ")
					absolute_path=raw_input(" -Please, write down the absolute path of the ISO file of the OS: \n\t")
					snap_name=raw_input(" -Please chose a snapshot's name: ").replace(' ', '_')
					
					# Gets an usable guest's IP
					host_ip=newGuestIP(guest_ip)
					
					# AntiVMdetect execution
					#antivmdetect.main(vm_name, guest_ip, host_ip, guest_primary_dns) it need to be run as superuser so...
					os.system('sudo '+path_scripts+'/antivmdetect.py "'+vm_name+'" '+guest_ip+' '+host_ip+' '+guest_primary_dns+' '+path_logs)

					# FTP, default @IP
					print bcolors.OKGREEN + "\n [*]"+bcolors.ENDC+" Preparing the FTP server (default @IP)"			
					os.system('sudo service vsftpd stop') # Service's down!
					prepareFTPserver.main(default_host_ip, ftp_port, path_logs)		
					os.system('sudo service vsftpd start > '+log_name) # Service's Up!			
					#Sometimes it does not end in running state, not sure why so... Check!
					_file=open(log_name, 'r')
					line=_file.readline()
					try:
						re.search('pre-start', line).group(0)
						print bcolors.WARNING+"WARNING: vsftp did not started properly, restart it manually in other terminal"+bcolors.ENDC
					except:
						pass
					_file.close()
					os.system('rm '+log_name)
					
					os.system('sudo cp '+path_req+'/cuckoo/agent/agent.py /srv/ftp/agent.pyw') #Hidden window
					#os.system('sudo cp '+path_bin+'/agent.exe /srv/ftp/agent.exe') #Should be...
					os.system('sudo cp '+path_bin+'/humanMimic.exe /srv/ftp')

					# VM creation
					print bcolors.OKGREEN + "\n [*]"+bcolors.ENDC+" Creating a VirtualBox's VM named "+vm_name
					newVM.main(RAM, HDD, nCores, file_output, host_ip, guest_ip, guest_primary_dns, 
								ftp_port, vm_name, absolute_path, snap_name, default_host_ip, path_logs)

					# FTP, current @IP
					print bcolors.OKGREEN + "\n [*]"+bcolors.ENDC+" Preparing the FTP server (current @IP)"
					os.system('sudo service vsftpd stop') # Service is down!
					prepareFTPserver.main(host_ip, ftp_port, path_logs)	
					os.system('sudo service vsftpd start > '+log_name) # Service is Up!		
					#Sometimes it does not end in running state, not sure why so... Check!
					_file=open(log_name, 'r')
					line=_file.readline()
					try:
						re.search('pre-start', line).group(0)
						print bcolors.WARNING+"WARNING: vsftp did not started properly, restart it manually in other terminal"+bcolors.ENDC
					except:
						pass
					_file.close()
					os.system('rm '+log_name)

					# Cuckoo modifications for the new VM
					tag_string=raw_input(bcolors.OKGREEN + "\n [*]"+bcolors.ENDC+' The Cuckoo configuration will be modified to suit the VM\nWrite down a list of tags for cuckoo to add to this VM profile. Separated with commas (e.g: windows_xp,office_2003,flash_1.2): ')
					cuckooMods.main(host_ip, guest_ip, vm_name, snap_name, tag_string, path_cuckoo, path_logs)  
				
				else:
					print bcolors.FAIL+" The requirements does not seems to be installed, please install them"+bcolors.ENDC
			# List Cuckoo's vms
			elif selection == 3: 
				if checkIns(path_req):
					vms=getVMlist()
					if vms == '':
						print bcolors.FAIL+'No VMs in the conf file'+bcolors.ENDC
					else:
						print getVMlist()
				else:
					print bcolors.FAIL+" The requirements does not seems to be installed, please install them"+bcolors.ENDC
			# Run
			elif selection == 4: 
				if checkIns(path_req):
					missing_vms=checkVMs()
					if missing_vms != []:
						print bcolors.WARNING+"WARNING: Some of the VMs listed in Cuckoo's conf file are not in VirtualBox anymore "+str(missing_vms)+" and the file will be sanitized"+bcolors.ENDC
						if raw_input("\tContinue? (Y/N): ").upper()=='Y':
							for vm in missing_vms:
								eraseVM(vm[1:-1]) #taking out the quotes
					while not checkVif():
						print bcolors.WARNING+"WARNING: The virtual interface is down. Please start a VM using VboxNet0, this will start the IF (you can turn that VM off whenever you want)"+bcolors.ENDC
						raw_input("Press ENTER when ready. ")
							
					#Cuckoo
					os.system('''gnome-terminal --tab -e "/bin/bash -c 'python '''+path_req+'''/cuckoo/cuckoo.py; exec /bin/bash -i'"''')
					#Web interface
					os.system('''gnome-terminal --tab -e "/bin/bash -c 'python '''+path_req+'''/cuckoo/utils/web.py -H localhost -p 8080; exec /bin/bash -i'"''')
				else:
					print bcolors.FAIL+" The requirements does not seems to be installed, please install them"+bcolors.ENDC
			# Exit
			elif selection == 5: 
				_quit=True
				print bcolors.OKGREEN+"	Goodbye!"+bcolors.ENDC
			# Input selection not in the options
			else: 
				print bcolors.FAIL+"Wrong input!"+bcolors.ENDC
			print '\n'
		except ValueError:
			print bcolors.FAIL+"Wrong input!\n"+bcolors.ENDC
	return

main()
exit(0)
