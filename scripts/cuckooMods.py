#!/usr/bin/python

# File: cuckoMods.py
# Jose Carlos Ramirez
# TFG Unizar

# Modify the necesary cuckoo files to make it work with our VM
# Argument 1: Host's @IP
# Argument 2: Guest's @IP
# Argument 3: VM's name
# Argument 4: Snapshot of the VM that is gonna be used
# Argument 5: List of tags separated by commas (a,b,c,d,e)

import sys
import subprocess
import re
import os

def main(host_ip, guest_ip, vm_name, snapshot_name, tag_string, path_cuckoo, path_logs):
	results_port="2042"
	
	##### cuckoo.conf #####
	options_list=[["machinery = ","virtualbox"],["memory_dump = ","on"],["ip = ",host_ip],["port = ",results_port]]
	line_written=False
	ip_written=False
	port_written=False

	#Opening the file for reading and writting
	conf_file=open(path_cuckoo+'/conf/cuckoo.conf', 'r')
	tmp_file=open(path_logs+'/cuckoo-tmp.conf', 'w')

	line=conf_file.readline()
	while line!="":
		for option in options_list:
			try:	
				re.search(option[0], line).group(0)
				tmp_file.write(option[0]+option[1]+'\n')
				line_written=True
				break

			except: #if the search fails, it's because there's not such a string
				pass	

		if not line_written:
			tmp_file.write(line)
		line=conf_file.readline()
		line_written=False

	conf_file.close()
	tmp_file.close()

	os.system('sudo mv '+path_logs+'/cuckoo-tmp.conf '+path_cuckoo+'/conf/cuckoo.conf')


	##### auxiliary.conf #####
	proc=subprocess.Popen(["whereis", "tcpdump"], stdout=subprocess.PIPE)#, shell=True) if we wanted to use pipes between process and things like that
	(_stdout, _stderr)=proc.communicate()
	tcpdump_path=_stdout.split()[1] #0 is tcpdumo, and 2...
	#otherModule_options
	sniffer_options=["sniffer",["enabled = ","yes"],["tcpdump = ",tcpdump_path],["interface = ","vboxnet0"],["#bpf = ","not arp"]]
	#Opening the file for reading and writting
	tmp_file=open(path_logs+'/auxiliary-tmp.conf', 'w')
	
	#Sniffer
	for option in sniffer_options:
		if option=="sniffer": #First one
			tmp_file.write('['+option+']\n') 	
		else:
			tmp_file.write(option[0]+option[1]+'\n')
	#Other module
	'''
	for option in otherModule_options:
		if option=="otherModule" #First one
			tmp_file.write('['+option[0]+']\n') #just option is enough, [0] just in case
		else:
			tmp_file.write(option[0]+option[1]+'\n')
	'''
	tmp_file.close()
	os.system('sudo mv '+path_logs+'/auxiliary-tmp.conf '+path_cuckoo+'/conf/auxiliary.conf')


	##### virtualbox.conf #####
	proc=subprocess.Popen(["whereis", "vboxmanage"], stdout=subprocess.PIPE)#, shell=True) if we wanted to use pipes between process and things like that
	(_stdout, _stderr)=proc.communicate()
	vbmn_path=_stdout.split()[1] #0 is tcpdumo, and 2...
	block_found=False
	line_written=False
	inside_cuckoo1=False
	#Opening the file for reading and writting
	conf_file=open(path_cuckoo+'/conf/virtualbox.conf', 'r') 
	tmp_file=open(path_logs+'/vbox-tmp.conf', 'w')
	options_list=[["mode = ","gui"], ["path = ",vbmn_path],["machines = ",vm_name]]
	optionsVM_list=[["label = ",vm_name],["platform = ","windows"],["ip = ", guest_ip],["snapshot = ", snapshot_name],["tags = ", tag_string]]

	#Adding the desired options
	line=conf_file.readline()
	while line!="":
		# General options
		for option in options_list:		
			try:
				re.search(option[0], line).group(0)
				if option[0]=="machines = ":
					try:										
						re.search(option[1], line).group(0) #if the VM is named 'machines' or '=' or something like that, this will fail	
					except: #if the vm name is not found on the current list
						try: #it cuckoo1 is on the list, first we have to take it out and then add the new one
							re.search('cuckoo1', line).group(0)
							splitted=line[:-1].split(',') #taking \n out
							option[0]=option[0]+option[1]
							for machine in splitted[1:]:#taking "machines = cuckoo1" out
								option[0]=option[0]+','+machine
							tmp_file.write(option[0]+'\n')
							line_written=True
						except: #if there are other machines already in the list but not cuckoo1, just add the new one
							option[0]=line[:-1]
							tmp_file.write(option[0]+','+option[1]+'\n')
							line_written=True												
				else:
					tmp_file.write(option[0]+option[1]+'\n')
					line_written=True
				break
			except: #if the search fails, it's because there's not such a string
				pass
		# Commenting the example conf, "cuckoo1"
		try:
			re.search('\[cuckoo1]', line).group(0) #escaping the first [, if not it will be taken as a set
			inside_cuckoo1=True	
			try: #In case it's already commented
				re.search('#', line).group(0) 	
			except: #If it's not, it have to be commented
				tmp_file.write('#'+line)
				line_written=True			
		except:
			pass	
		if inside_cuckoo1:
			for option in optionsVM_list[:3]: # The other options are commented by default
				try:
					re.search(option[0], line).group(0)
					try: #In case it's already commented
						re.search('#', line).group(0) 	
					except: #If it's not, it have to be commented
						tmp_file.write('#'+line)	
						line_written=True
					# When the last option is found, nothing more have to be commented	
					if option[0] == "ip = ":
						inside_cuckoo1=False		
				except:
					pass			
		# Search for the current machine's block
		try: 
			re.search('\['+vm_name+']', line).group(0) #escaping the first [, if not it will be taken as a set
			block_found=True
			tmp_file.write(line) #block's name
			for option in optionsVM_list:
				tmp_file.write(option[0]+option[1]+'\n')

			#Read until the next VM block is found, [vm_2name]
			line=conf_file.readline()		
			while line!="": #if it's the last one, it will end before finding the next
				try:	
					re.match("\[([0-9A-Za-z. ]*)]\n", line).group(0) # [something]\n will match, escaping the first [, if not it will be taken as a set
					break
				except:
					pass
				line=conf_file.readline()
			# line_written is not True because we have read until the next block (or end) that should be written			
		except:
			pass
		
		if not line_written:
			tmp_file.write(line)
		line=conf_file.readline()
		line_written=False

	if not block_found:
		tmp_file.write('\n['+vm_name+']\n')
		for option in optionsVM_list:
			tmp_file.write(option[0]+option[1]+'\n')
			
	conf_file.close()
	tmp_file.close()
	os.system('sudo mv '+path_logs+'/vbox-tmp.conf '+path_cuckoo+'/conf/virtualbox.conf')

	##### reporting.conf #####
	block_found=False
	line_written=False
	#Opening the file for reading and writting
	conf_file=open(path_cuckoo+'/conf/reporting.conf', 'r') 
	tmp_file=open(path_logs+'/reporting-tmp.conf', 'w')
	options_list=[["enabled = ","yes\n"]]

	line=conf_file.readline()
	while line!="":
		try:
			re.search('\[reporthtml]', line).group(0)
			block_found=True
		except: 
			pass
		for option in options_list:	
			if block_found:
				try:
					re.search(option[0], line).group(0)
					tmp_file.write(option[0]+option[1])
					line_written=True
					block_found=False
				except:
					pass
		if not line_written:
			tmp_file.write(line)
		line_written=False
		line=conf_file.readline()
		
	conf_file.close()
	tmp_file.close()	
	os.system('sudo mv '+path_logs+'/reporting-tmp.conf '+path_cuckoo+'/conf/reporting.conf')
	
	########## human.py #######
	# We want to use our own mouse movements and random clicks	
	conf_file=open(path_cuckoo+'/analyzer/windows/modules/auxiliary/human.py', 'r') 
	tmp_file=open(path_logs+'/human-tmp.py', 'w')
	line=conf_file.readline()
	
	while line != '':
		try:
			re.search('click_mouse()', line).group(0)
			try:
				re.search(':', line).group(0)
			except:
				line='#'+line
		except:
			pass
		try:
			re.search('move_mouse()', line).group(0)
			try:
				re.search(':', line).group(0)
			except:
				line='#'+line
		except:
			pass		
		tmp_file.write(line)						
		line=conf_file.readline()
	
	conf_file.close()
	tmp_file.close()	
	os.system('sudo mv '+path_logs+'/human-tmp.py '+path_cuckoo+'/analyzer/windows/modules/auxiliary/human.py')
	
	return
