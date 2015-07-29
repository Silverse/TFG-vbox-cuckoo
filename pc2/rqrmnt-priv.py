#!/usr/bin/python

# File: rqrmnt-priv.py
# Edited: 29/07/2015
# Jose Carlos Ramirez
# TFG Unizar

# Section of the requirements.py file that should be run with elevated privileges
# Needs to be run as SuperUser.

import os
import re

header_comment="#Cuckoo IPtables rules, written by requirements.py. Jose Carlos's TFG"
iptables_rules=["sudo iptables -A FORWARD -o eth0 -i vboxnet0 -s 192.168.56.0/24 -m conntrack --ctstate NEW -j ACCEPT","sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT","sudo iptables -A POSTROUTING -t nat -j MASQUERADE","sudo sysctl -w net.ipv4.ip_forward=1" ]

os.system('sudo chmod 755 /etc/rc.local') #Make sure that it's executable
#Opening the file for reading and writting
startup_file=open('/etc/rc.local', 'r+')
tmp_file=open('/tmp/rc.local_tmp', 'w+')
rules_written=False

line=startup_file.readline()
while line!="":
	try:
		re.search(header_comment, line).group(0)
		for rule in iptables_rules: #If the comment is found
			line=startup_file.readline()
			tmp_file.write(rule+'\n')
		rules_written=True
	except: #If the search fails, it's because there's not such a string
		tmp_file.write(line)		
	line=startup_file.readline()

if not rules_written:
	tmp_file.write(header_comment+'\n')
	for rule in iptables_rules:
		tmp_file.write(rule+'\n')
tmp_file.write("\nexit 0") #Always add it at the end

startup_file.close()
tmp_file.close()
#Open truncate file, we are going to fill it with the tmp one
startup_file=open('/etc/rc.local', 'w')
tmp_file=open('/tmp/rc.local_tmp', 'r')
new_content=tmp_file.read()
startup_file.write(new_content)
startup_file.close()
tmp_file.close()

exit()
