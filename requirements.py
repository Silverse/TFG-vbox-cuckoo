#!/usr/bin/python

# File: requirements.py
# Edited: 23/07/2015
# Jose Carlos Ramirez
# TFG Unizar
# Dowload or install the requirements of the VM or Cuckoo

import os

os.system('sudo apt-get update')
### Guest
## Python
os.system('wget -P /srv/ftp http://python.org/ftp/python/2.7.10/python-2.7.10.msi')
#os.system('sudo cp python-2.7.10.msi /srv/ftp')
## Python Imaging Library
os.system('wget -P /srv/ftp http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe')
#os.system('sudo cp PIL-1.1.7.win32-py2.7.exe /srv/ftp')

### Host
os.system('''sudo mkdir requirements
sudo chmod 755 requirements
cd requirements
''')

package_list="python-bson python-sqlalchemy python-dpkt python-jinja2 python-magic python-pymongo python-gridfs python-bottle python-pefile python-chardet volatility"
os.system('sudo apt-get install '+package_list)

## Pydeep
# Ssdeep from source
os.system('''
	sudo apt-get install python-pip -y
	sudo apt-get install build-essential git python-dev -y
	wget http://sourceforge.net/projects/ssdeep/files/ssdeep-2.12/ssdeep-2.12.tar.gz/download -O ssdeep.tar.gz
	tar -xf ssdeep.tar.gz
	cd ssdeep-2.12
	./configure 
	make 
	sudo make install
	cd ..
	''') #Executing'ssdeep -V' for checking '2.12'
# Pydeep via pip
os.system('sudo apt-get install python-pip -y')
os.system('sudo pip install pydeep') #Executing 'pip show pydeep' for checking 'version:0.2'

## Yara
os.system('sudo apt-get install build-essential git python-dev libjansson-dev libmagic-dev libtool eclipse-cdt-autotools -y')
os.system('''
	wget https://github.com/plusvic/yara/archive/v3.4.0.tar.gz
	tar -zxf v3.4.0.tar.gz
	cd yara-3.4.0/
	./bootstrap.sh
	./configure --enable-cuckoo --enable-magic
	make
	sudo make install
	''')
# Yara python
os.system('''
	cd yara-python
	python setup.py build
	sudo python setup.py install
	cd ..
	''')

## Configure TCPdump
os.system('''sudo apt-get install tcpdump
sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
sudo apt-get install libcap2-bin
''')

## IPtables stuff
header_comment="#Cuckoo IPtables rules, written by requirements.py. Jose Carlos's TFG"
iptables_rules=["sudo iptables -A FORWARD -o eth0 -i vboxnet0 -s 192.168.56.0/24 -m conntrack --ctstate NEW -j ACCEPT","sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT","sudo iptables -A POSTROUTING -t nat -j MASQUERADE","sudo sysctl -w net.ipv4.ip_forward=1" ]

os.system('chmod 755 /etc/rc.local') #Make sure that it's executable
#Opening the file for reading and writting
startup_file=open('/etc/rc.local', 'r+')
tmp_file=open('/tmp/rc.local_tmp', 'w+')

line=startup_file.readline()
rules_written=False
while line!="exit 0\n":
	try:
		re.search(header_string, line).group(0)
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

#Install cuckoo
os.system('''sudo wget http://downloads.cuckoosandbox.org/cuckoo-current.tar.gz
sudo tar -xf cuckoo-current.tar.gz
sudo cp cuckoo/agent/agent.py /srv/ftp
''')



exit()

