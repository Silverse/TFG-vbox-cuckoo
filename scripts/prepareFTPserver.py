#!/usr/bin/python

# File: prepareFTPserver.py
# Jose Carlos Ramirez
# TFG Unizar

# Creates a fixed vsftpd server, allowing anonymous download.
# Needs to be run as SuperUser.
# Argument 1: server's listening IP address 
# Argument 2: server's listening port

import os
import re
import sys
import time



def main(srv_ip, srv_port, path_logs):
	allowed_options=["listen=", "anonymous_enable=", "dirmessage_enable=", "use_localtime=", "xferlog_enable=", "connect_from_port_20=", "listen_address=", "listen_port="]
	line_written=False
	ip_written=False
	port_written=False			
			
	#Opening the file for reading and writting
	conf_file=open('/etc/vsftpd.conf', 'r')
	tmp_file=open(path_logs+'/vsftpd-tmp.conf', 'w')

	line=conf_file.readline()
	while line!="":
		for option in allowed_options:
			try:
				re.search(option, line).group(0)
				if option=="listen_address=":
					tmp_file.write(option+srv_ip+"\n")
					ip_written=True				
				elif option=="listen_port=":
					tmp_file.write(option+srv_port+"\n")
					port_written=True			
				else:
					tmp_file.write(option+"YES\n")
				line_written=True
				break

			except: #if the search fails, it's because there's not such a string
				pass
		if not line_written:
			tmp_file.write(line)
		line=conf_file.readline()
		line_written=False
	# If the @IP and port wasn't there
	if not ip_written:
		tmp_file.write("# Listen settings\n")
		tmp_file.write("listen_address="+srv_ip+"\n")
	if not port_written:
		tmp_file.write("listen_port="+srv_port+"\n")

	conf_file.close()
	tmp_file.close()

	
	os.system('sudo mv '+path_logs+'/'+'vsftpd-tmp.conf /etc/vsftpd.conf')
	os.system('sudo chown -R root:root /etc/vsftpd.conf') #If it's not owned by root, it won't run properly
	
	return
