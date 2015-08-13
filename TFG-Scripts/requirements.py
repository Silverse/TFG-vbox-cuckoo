#!/usr/bin/python

# File: requirements.py
# Jose Carlos Ramirez
# TFG Unizar

# Dowload or install the requirements of the VM or Cuckoo.
# Calls rqrmnt-priv.py

import os
import sys

host_ip=str(sys.argv[1])

path_req=os.path.abspath('..')+'/requirements'

# Just in case
os.system('sudo apt-get update')

### Guest
## Python
os.system('sudo wget -P /srv/ftp http://python.org/ftp/python/2.7.10/python-2.7.10.msi')
## Python Imaging Library
os.system('sudo wget -P /srv/ftp http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe')

### Host
os.system('mkdir '+path_req)
package_list="python-bson python-sqlalchemy python-dpkt python-jinja2 python-magic python-pymongo python-gridfs python-bottle python-pefile python-chardet volatility"
os.system('sudo apt-get install '+package_list)

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

# Pydeep via pip
os.system('sudo apt-get install python-pip -y')
os.system('sudo pip install pydeep') #Executing 'pip show pydeep' for checking 'version:0.2'

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

# Yara python
os.system('''
	cd '''+path_req+'''/yara-3.4.0/yara-python
	python setup.py build
	sudo python setup.py install
	''')

## Configure TCPdump
os.system('''
	sudo apt-get install tcpdump
	sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
	sudo apt-get install libcap2-bin
	''')

## rc.local modifications
os.system('sudo python rqrmnt-priv.py '+host_ip) # Execution of the elevated-pivilege part of the script

os.system('''
	cd /etc
	./rc.local
	''')

## Install cuckoo
os.system('''
	cd '''+path_req+'''
	wget http://downloads.cuckoosandbox.org/cuckoo-current.tar.gz
	tar -xf cuckoo-current.tar.gz
	''')
# It's also possible to dowload for the repositorie, but it's not the stable version
# sudo git clone https://github.com/cuckoobox/cuckoo.git
# sudo chown -R cuckoo:vboxusers cuckoo

# Install python date-util (In some momment Cuckoo needed it, but maybe it was not necesary
os.system('sudo pip install python-dateutil')

## AntiVMdetect dependancies
os.system('sudo apt-get install python-dmidecode libcdio-utils acpidump\n')

exit()
