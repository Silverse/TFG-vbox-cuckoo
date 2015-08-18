#!/usr/bin/python

# File: requirements.py
# Jose Carlos Ramirez
# TFG Unizar

# Dowload or install the requirements of the VM or Cuckoo.
# Calls rqrmnt-priv.py

import os
import sys
import re

class bcolors:
    HEADER = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
def main(host_ip, path_req, path_logs):
	# Just in case
	os.system('sudo apt-get update')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider
	### Guest
	## Python
	os.system('sudo wget -P /srv/ftp http://python.org/ftp/python/2.7.10/python-2.7.10.msi')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider
	## Python Imaging Library
	os.system('sudo wget -P /srv/ftp http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	### Host
	package_list="python-bson python-sqlalchemy python-dpkt python-jinja2 python-magic python-pymongo python-gridfs python-bottle python-pefile python-chardet volatility"
	os.system('sudo apt-get install '+package_list)
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	# Install python date-util (In some momment seemed Cuckoo needed it, but maybe it was not necesary)
	os.system('sudo pip install python-dateutil')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	## AntiVMdetect dependancies
	os.system('sudo apt-get install python-dmidecode libcdio-utils acpidump\n')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	## Pydeep
	# Ssdeep from source
	os.system('''
		sudo apt-get install python-pip -y
		sudo apt-get install build-essential git python-dev -y
		wget  http://sourceforge.net/projects/ssdeep/files/ssdeep-2.12/ssdeep-2.12.tar.gz/download -O '''+path_req+'''/ssdeep.tar.gz
		cd '''+path_req+'''
		tar -xf ssdeep.tar.gz
		cd ssdeep-2.12
		./configure 
		make 
		sudo make install
		''') #Executing'ssdeep -V' for checking '2.12'
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	# Pydeep via pip
	os.system('sudo apt-get install python-pip -y')
	os.system('sudo pip install pydeep') #Executing 'pip show pydeep' for checking 'version:0.2'
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	## Yara
	os.system('sudo apt-get install build-essential git python-dev libjansson-dev libmagic-dev libtool eclipse-cdt-autotools -y')
	os.system('''
		wget -P '''+path_req+''' https://github.com/plusvic/yara/archive/v3.4.0.tar.gz
		cd '''+path_req+'''
		tar -zxf v3.4.0.tar.gz
		cd yara-3.4.0/
		./bootstrap.sh
		./configure --enable-cuckoo --enable-magic
		make
		sudo make install
		''')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	# Yara python
	os.system('''
		cd '''+path_req+'''/yara-3.4.0/yara-python
		python setup.py build
		sudo python setup.py install
		''')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	## Configure TCPdump
	os.system('''
		sudo apt-get install tcpdump
		sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
		sudo apt-get install libcap2-bin
		''')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	## rc.local stuff	
	split_host=host_ip.split('.')
	host_net=split_host[0]+'.'+split_host[1]+'.'+split_host[2]+'.0/24'

	header_comment="#Cuckoo IPtables rules, written by requirements.py. Jose Carlos's TFG"
	iptables_rules=["sudo iptables -A FORWARD -o eth0 -i vboxnet0 -s "+host_net+" -m conntrack --ctstate NEW -j ACCEPT",
			"sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT",
			"sudo iptables -A POSTROUTING -t nat -j MASQUERADE",
			"sudo sysctl -w net.ipv4.ip_forward=1" ] #This one is not a rule, but it's neccesary to get vboxnet up at reboot

	os.system('sudo chmod 755 /etc/rc.local') #Makes sure that it's executable
	#Opening the file for reading and writting
	startup_file=open('/etc/rc.local', 'r')
	tmp_file=open(path_logs+'/'+'rc.local_tmp', 'w')
	rules_written=False

	line=startup_file.readline()
	while line!="":
		try:
			re.search(header_comment, line).group(0)
			tmp_file.write(header_comment+'\n')
			for rule in iptables_rules: #If the comment is found
				line=startup_file.readline()
				tmp_file.write(rule+'\n')
			rules_written=True
		except: #If the search allways fails, it's because there is no header comment
			try: #To not write the default 'exit 0' before the rules			
				re.search('exit 0',line).group(0)
				if rules_written: #in this case is the one written with the rules
					tmp_file.write(line)
			except:
				tmp_file.write(line)		
		line=startup_file.readline()

	if not rules_written:
		tmp_file.write(header_comment+'\n')
		for rule in iptables_rules:
			tmp_file.write(rule+'\n')
		tmp_file.write("\nexit 0") 

	startup_file.close()
	tmp_file.close()
	
	os.system('sudo mv '+path_logs+'/'+'rc.local_tmp /etc/rc.local')
	
	os.system('''
		cd /etc
		sudo ./rc.local
		cat rc.local
		''')
	print bcolors.OKGREEN+"\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n"+bcolors.ENDC #Divider

	## Install cuckoo
	os.system('''
		cd '''+path_req+'''
		wget http://downloads.cuckoosandbox.org/cuckoo-current.tar.gz
		tar -xf cuckoo-current.tar.gz
		''')
	# It's also possible to dowload for the repositorie, but it's not the stable version
	# sudo git clone https://github.com/cuckoobox/cuckoo.git
	# sudo chown -R cuckoo:vboxusers cuckoo
		
		
	return	
