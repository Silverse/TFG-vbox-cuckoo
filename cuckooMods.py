#!/usr/bin/python

# File: cuckoMods.py
# Edited: 23/07/2015
# Jose Carlos Ramirez
# TFG Unizar
# Modify the necesary cuckoo files to make it work with our VM

# Argument 1: Host's @IP
# Argument 2: Guest's @IP
# Argument 3: VM's name
# Argument 4: Snapshot of the VM that is gonna be used
# Argument 5+: List of tags separated by white space (a b c d e)

import sys
import subprocess
import re

host_ip=sys.argv[1]
guest_ip=sys.argv[2]
vm_name=sys.argv[3]
snapshot_name=sys.argv[4]
tag_list=""
for arg in sys.argv[5::]:
	if arg==sys.argv[5]: #To avoid having a comma at the beggining
		tag_list=arg
	else:
		tag_list=tag_list+','+arg

##### cuckoo.conf #####
options_list=[["machinery = ","virtualbox"],["memory_dump = ","on"],["ip = ",host_ip],["port = ","2042"]]
line_written=False
ip_written=False
port_written=False

#Opening the file for reading and writting
conf_file=open('cuckoo/conf/cuckoo.conf', 'r+')
tmp_file=open('/tmp/cuckoo-tmp.conf', 'w+')

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

# Open truncate file, we are going to fill it with the tmp one
conf_file=open('cuckoo/conf/cuckoo2.conf', 'w') 
tmp_file=open('/tmp/cuckoo-tmp.conf', 'r')

new_content=tmp_file.read()
conf_file.write(new_content)

conf_file.close()
tmp_file.close()



##### auxiliary.conf #####
proc=subprocess.Popen(["whereis", "tcpdump"], stdout=subprocess.PIPE)#, shell=True) if we wanted to use pipes between process and things like that
(_stdout, _stderr)=proc.communicate()
tcpdump_path=_stdout.split()[1] #0 is tcpdumo, and 2...
#otherModule_options
sniffer_options=["sniffer",["enabled = ","yes"],["tcpdump = ",tcpdump_path],["interface = ","vboxnet0"],["#bpf = ","not arp"]]
#Opening the file for reading and writting
tmp_file=open('/tmp/auxiliary-tmp.conf', 'w+')
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
# Open truncate file, we are going to fill it with the tmp one
conf_file=open('cuckoo/conf/auxiliary2.conf', 'w') 
tmp_file=open('/tmp/auxiliary-tmp.conf', 'r')

new_content=tmp_file.read()
conf_file.write(new_content)

conf_file.close()
tmp_file.close()


##### virtualbox.conf #####
proc=subprocess.Popen(["whereis", "vboxmanage"], stdout=subprocess.PIPE)#, shell=True) if we wanted to use pipes between process and things like that
(_stdout, _stderr)=proc.communicate()
vbmn_path=_stdout.split()[1] #0 is tcpdumo, and 2...

#Opening the file for reading and writting
block_found=False
line_written=False
conf_file=open('cuckoo/conf/virtualbox.conf', 'r+') #cuckoo/conf/vbox2.conf cuckoo/conf/virtualbox.conf
tmp_file=open('/tmp/vbox-tmp.conf', 'w+')
options_list=[["mode = ","gui"], ["path = ",vbmn_path],["machines = ",vm_name]]
optionsVM_list=[["label = ",vm_name],["platform = ","windows"],["ip = ", guest_ip],["snapshot = ", snapshot_name],["tags = ", tag_list]]

line=conf_file.readline()
while line!="":
	print line
	for option in options_list:
		try:
			print option[0]
			re.search(option[0], line).group(0)
			print "found"
			if option[0]=="machines = ":
				try:										
					re.search(option[1], line).group(0) #if the VM is named 'machines' or '=' or something like that, this will fail
					tmp_file.write(line)	
				except: #if the vm name is not found on the current list
					option[0]=line[0:len(line)-1] #taking \n out
					tmp_file.write(option[0]+','+option[1]+'\n')
					print option[0]+','+option[1]+'\n'
			else:
				tmp_file.write(option[0]+option[1]+'\n')
			line_written=True
			break
		except: #if the search fails, it's because there's not such a string
			pass	
	try: #Search for the current machine's block
		re.search(vm_name+']', line).group(0) #If you add an opening [, it will think of it as a regular expresion
		block_found=True
		tmp_file.write(line) #block's name
		for option in optionsVM_list:
			tmp_file.write(option[0]+option[1]+'\n')

		#Read until the next VM block is found, [vm_2name]
		line=conf_file.readline()		
		while line!="": #if it's the last one, it will end before finding the next
			try:	
				re.match("([0-9A-Za-z. ]*)]\n", line).group(0) # something]\n will match
				break
			except:
				pass
			line=conf_file.readline()			
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

# Open truncate file, we are going to fill it with the tmp one
conf_file=open('cuckoo/conf/vbox2.conf', 'w') 
tmp_file=open('/tmp/vbox-tmp.conf', 'r')

new_content=tmp_file.read()
conf_file.write(new_content)

conf_file.close()
tmp_file.close()

exit()

