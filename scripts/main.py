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
import random

# Values
RAM="2000"
HDD="70000"
nCores="3"
file_output="/tmp/newVM.log"
host_ip="192.168.58.1" 
default_host_ip="192.168.56.1"
guest_ip="192.168.58.25" #default 192.168.56.101
guest_primary_dns="208.67.222.222"
ftp_port="21"

path_req=os.path.abspath('..')+'/requirements'
path_cuckoo=os.path.abspath('..')+'/requirements/cuckoo'
path_bin=os.path.abspath('..')+'/bin'
path_scripts=s.path.abspath('..')+'/scripts'
# Current one is /TFG-scripts
log_name="main.log"

#################### Functions ###################
# Check if there is a folder named requirements and if its weight is over a minimum
def checkIns(folder=path_req): 
	folder_size = 0
	for (path, dirs, files) in os.walk(folder):
		for _file in files:
			filename = os.path.join(path, _file)
			folder_size += os.path.getsize(filename)
	folder_size/=(1024*1024.0)
	if folder_size < 100: #Less than 100 Mb, +- the weight of a new yara+ssdeep+cuckoo
		return False
	if not os.path.isdir(path_req):
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
def newGuestIP(default=guest_ip):
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
	tmp_file=open('/tmp/'+system+'-tmp.conf', 'w+')
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
	tmp_file=open('/tmp/'+system+'-tmp.conf', 'r')

	new_content=tmp_file.read()
	conf_file.write(new_content)

	conf_file.close()
	tmp_file.close()
	return	

#################################################

# If the output file exists and it was created by a different user, the script won't be able to interact with it (permission denied)
proc=subprocess.Popen(["ls", '/tmp/'], stdout=subprocess.PIPE)
(_stdout, _stderr)=proc.communicate()
try:
	re.search(file_output[4:], _stdout).group(0)
	os.system('sudo rm '+file_output) 
except: #does not exists
	pass

## Wellcome
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

## Menu
menu=["\t-1) Install the dependancies and Cuckoo", 
		"\t-2) Create a new fixed VM",
		"\t-3) List the Cuckoo's VM", 
		"\t-4) Run Cuckoo and the webserver (localhost:8080)", 
		"\t-5) Close" ]
close=False

while not close:
	# Print menu
	if checkIns():
		marked=False
	else:	
		marked=True
	print "\t###################### Menu ################"
	for op in menu:
		if not marked:
			print op+" [DONE]"
			marked=True
		else:
			print op
	selection=int(raw_input("Option's number: "))

	# Installation
	if selection == 1: 
		# New user
		if raw_input(' -Do you have a user ready for cuckoo usage? (Y/N): ').upper()=='Y':
			user_name=raw_input('\t-Please write the user name: ')
			proc=subprocess.Popen(["whoami"], stdout=subprocess.PIPE)
			(_stdout, _stderr)=proc.communicate()
			if _stdout[:-1] != user_name:
				print "You are not logged as this user. Please change it and run the script again"
				exit(1)
		else:
			user_name=raw_input('\t-Please chose a user name: ')
			os.system('''
				sudo adduser  -gecos "" '''+user_name+'''
				sudo usermod -G vboxusers '''+user_name+'''
				sudo usermod -g sudo '''+user_name+
				 '''\n''')
			print '\n\t-Created: '+user_name+' part of vboxusers and superusers\n-Run the script using the new user.'
			exit(1)	
		
		# Install cuckoo and dependencies
		if checkIns():
			if raw_input(" -The requirements folder seems to exist. Do you want to continue? (Y/N): ").upper()=='Y':
				print "\n [*] Installing Cuckoo, dependancies, and side programs"
				os.system('python requirements.py '+host_ip)
		else:
			print "\n [*] Installing Cuckoo, dependancies, and side programs"
			os.system('python requirements.py '+host_ip)	
	# New VM
	elif selection == 2: 
		if checkIns(): #Check if (probably) the dependancies are installed
			vm_name="'"+raw_input("\n -Write the name of your VM: ")+"'"
			absolute_path=raw_input(" -Please, write down the absolute path of the ISO file of the OS: \n\t")
			snap_name=raw_input(" -Please chose a snapshot's name: ")
			
			# Gets an usable guest's IP
			host_ip=newGuestIP()
			
			# AntiVMdetect execution
			os.system("sudo python antivmdetect.py "+vm_name+" "+guest_ip+" "+host_ip+" "+guest_primary_dns)

			# FTP, default @IP
			print "\n [*] Preparing the FTP server (default @IP)"			
			os.system('sudo service vsftpd stop') # Service's down!
			os.system("sudo python prepareFTPserver.py "+default_host_ip+" "+ftp_port)			
			os.system('sudo service vsftpd start > '+log_name) # Service's Up!			
			#Sometimes it does not end in running state, not sure why so... Check!
			_file=open(log_name, 'r')
			line=_file.readline()
			try:
				re.search('pre-start', line).group(0)
				print "WARNING: vsftp did not started properly, restart it manually in other terminal"
			except:
				pass
			_file.close()
			os.system('rm outTest.txt')
			
			os.system('sudo cp '+path_req+'/cuckoo/agent/agent.py /srv/ftp')
			os.system('sudo cp '+path_bin+'/mouseAct.exe /srv/ftp')

			# VM creation
			print "\n [*] Creating a VirtualBox's VM named "+vm_name
			os.system('python newVM-simple.py '+RAM+' '+HDD+' '+nCores+' '+file_output+' '+host_ip+' '+guest_ip+' '+guest_primary_dns+' '+ftp_port+' '+vm_name+' '+absolute_path+' '+snap_name+' '+default_host_ip)

			# FTP, current @IP
			print "\n [*] Preparing the FTP server (current @IP)"
			os.system('sudo service vsftpd stop') # Service is down!
			os.system("sudo python prepareFTPserver.py "+host_ip+" "+ftp_port)
			os.system('sudo service vsftpd start > '+log_name) # Service is Up!		
			#Sometimes it does not end in running state, not sure why so... Check!
			_file=open(log_name, 'r')
			line=_file.readline()
			try:
				re.search('pre-start', line).group(0)
				print "WARNING: vsftp did not started properly, restart it manually in other terminal"
			except:
				pass
			_file.close()
			os.system('rm outTest.txt')

			# Cuckoo modifications for the new VM
			tag_list=raw_input('\n [*] The Cuckoo configuration will be modified to suit the VM\nWrite down a list of tags for cuckoo to add to this VM profile. Separated with white spaces (e.g: windows_xp office_2003 flash_1.2): ')
			os.system('python cuckooMods.py '+host_ip+' '+guest_ip+' '+vm_name+' '+snap_name+' '+tag_list)

		else:
			print " The requirements does not seems to be installed, please install them"
	# List Cuckoo's vms
	elif selection == 3: 
		if checkIns():
			vms=getVMlist()
			if vms == '':
				print 'No VMs in the conf file'
			else:
				print getVMlist()
		else:
			print " The requirements does not seems to be installed, please install them"
	# Run
	elif selection == 4: 
		if checkIns():
			missing_vms=checkVMs()
			if missing_vms != []:
				print "WARNING: Some of the VMs listed in Cuckoo's conf file are not in VirtualBox anymore "+str(missing_vms)+" and the file will be sanitized"
				if raw_input("\tContinue? (Y/N): ").upper()=='Y':
					for vm in missing_vms:
						eraseVM(vm[1:-1]) #taking out the quotes
			#Cuckoo
			os.system('''gnome-terminal --tab -e "/bin/bash -c 'python '''+path_req+'''/cuckoo/cuckoo.py; exec /bin/bash -i'"''')
			#Web interface
			os.system('''gnome-terminal --tab -e "/bin/bash -c 'python '''+path_req+'''/cuckoo/utils/web.py -H localhost -p 8080; exec /bin/bash -i'"''')
		else:
			print " The requirements does not seems to be installed, please install them"
	# Exit
	else: 
		close=True
		print "	Goodbye!"
	print '\n'

exit(0)
