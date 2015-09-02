# File: fakeBrowsing.py
# Jose Carlos Ramirez
# TFG Unizar

# To be run inside the Guest.  Guide the user during the in-guest operations

import os

import fakeBrowsing

def main():	
	_quit=True
	while not _quit:
		print """\tWellcome to your in-guest guide
		1) This is the first time that I run the guide.
		2) I already rebooted the system and this is the second time I am running it."""
		selection=raw_input(" Your selection: ")
		
		if selection=='1':
			_quit=True
			vm_name=raw_input("\tType the name of your VM: ")
			print "\tFirst we will install"
			os.system('PIL-1.1.7.win32-py2.7.exe')
			raw_input(" Press ENTER when finished")
			print "\tThen Firefox"
			os.system('"Firefox Setup 40.0.2.exe"')
			raw_input(" Press ENTER when finished")
			print "\tIn guest modifications of the Windows XP OS"
			os.system('vboxmods-'+vm_name+'.bat')
			raw_input(" Press ENTER when finished")
			raw_input("\tNow install all the extra software that you want. Then press ENTER.")
			
		
		elif selection=='2':
			_quit=True
			vm_name=raw_input("\tType the name of your VM: ")
			print "\tIn guest modifications of the Windows XP OS"
			os.system('vboxmods-'+vm_name+'.bat')
			raw_input(" Press ENTER when finished")		
			print "\tFaking internet browsing and creating random files"
			fakeBrowsing.main()	
			raw_input("\tRunning agent.pyw manually. Then press ENTER")
			print "\tRunning the humanMimic AHK module"
			os.system('start cmd /c humanMimic.exe')
			raw_input("\n\tThis is the finall step. To trigger the humanMimic module you have to press the windows key + 'a'. Be ready, after that should inmediatly continue with the instruccions out of the VM!")
								
		else:
			print " Invalid input!"
			_quit=False
			
	return
		
			
main()
exit()