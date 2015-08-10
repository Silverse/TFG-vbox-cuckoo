#!/usr/bin/python

# File: antivmdetect.py
# Edited: 19/07/2015
# Jose Carlos Ramirez
# TFG Unizar

# Author of the original script: Mikael,@nsmfoo - blog.prowling.nu
# Tested on Ubuntu 14.04 LTS, using several brands of computers and types..but there is not guarantee that it will work anyway
# Prerequisites: python-dmidecode, cd-drive and acpidump: apt-get install python-dmidecode libcdio-utils acpidump

# Small modifications by Jose Carlos Ramirez for BcS Thesis. 
# Needs to be run as SuperUser.
# Argument 1: VM's name
# Argument 2: Guest's @IP
# Argument 3: Host's @IP
# Argument 4: Guest's primary DNS server


# Import stuff
import commands
import os.path
import dmidecode
import random
import uuid
import re
import time
import sys
import os


# Welcome
print '\n--- AntiVMdetect by Mikael, @nsmfoo (modified by Jose Carlos R.) ---'
print '[*] Creating VirtualBox modifications ..'

##################### Functions ################
def serial_randomize(start=0, string_length=10):
    rand = str(uuid.uuid4())
    rand = rand.upper()
    rand = re.sub('-', '', rand)
    return rand[start:string_length]

###############################################

vm_name='"'+str(sys.argv[1])+'"'
guest_ip=str(sys.argv[2])
host_ip=str(sys.argv[3])
guest_primary_dns=str(sys.argv[4])

dmi_info = {}

for v in dmidecode.bios().values():
    if type(v) == dict and v['dmi_type'] == 0:
        dmi_info['DmiBIOSVendor'] = v['data']['Vendor']
        dmi_info['DmiBIOSReleaseDate'] = v['data']['Relase Date']
        dmi_info['DmiBIOSVersion'] = v['data']['Version']
        biosversion = v['data']['BIOS Revision']

try:
    dmi_info['DmiBIOSReleaseMajor'], dmi_info['DmiBIOSReleaseMinor'] = biosversion.split('.', 1)
except:
    dmi_info['DmiBIOSReleaseMajor'] = '** No value to retrieve **'
    dmi_info['DmiBIOSReleaseMinor'] = '** No value to retrieve **'

# python-dmidecode does not currently reveal all values .. this is plan B
dmi_firmware = commands.getoutput("dmidecode -t0")
try:
    dmi_info['DmiBIOSFirmwareMajor'], dmi_info['DmiBIOSFirmwareMinor'] = re.search(
        "Firmware Revision: ([0-9A-Za-z. ]*)", dmi_firmware).group(1).split('.', 1)
except:
    dmi_info['DmiBIOSFirmwareMajor'] = '** No value to retrieve **'
    dmi_info['DmiBIOSFirmwareMinor'] = '** No value to retrieve **'

for v in dmidecode.baseboard().values():
    if type(v) == dict and v['dmi_type'] == 2:
        serial_number = v['data']['Serial Number']
        dmi_info['DmiBoardVersion'] = v['data']['Version']
        dmi_info['DmiBoardProduct'] = v['data']['Product Name']
        dmi_info['DmiBoardVendor'] = v['data']['Manufacturer']

# This is hopefully not the best solution ..
try:
    s_number = []
    if serial_number:
        # Get position
        if '/' in serial_number:
            for slash in re.finditer('/', serial_number):
                s_number.append(slash.start(0))
                # Remove / from string
                new_serial = re.sub('/', '', serial_number)
                new_serial = serial_randomize(0, len(new_serial))
            # Add / again
            for char in s_number:
                new_serial = new_serial[:char] + '/' + new_serial[char:]
        else:
            new_serial = serial_randomize(0, len(serial_number))
    else:
        new_serial = "** No value to retrieve **"
except:
    new_serial = "** No value to retrieve **"

dmi_info['DmiBoardSerial'] = new_serial

# python-dmidecode does not reveal all values .. this is plan B
dmi_board = commands.getoutput("dmidecode -t2")
try:
    asset_tag = re.search("Asset Tag: ([0-9A-Za-z ]*)", dmi_board).group(1)
except:
    asset_tag = '** No value to retrieve **'

dmi_info['DmiBoardAssetTag'] = asset_tag

try:
    loc_chassis = re.search("Location In Chassis: ([0-9A-Za-z ]*)", dmi_board).group(1)
except:
    loc_chassis = '** No value to retrieve **'

dmi_info['DmiBoardLocInChass'] = loc_chassis

# Based on the list from http://www.dmtf.org/sites/default/files/standards/documents/DSP0134_3.0.0.pdf
board_dict = {'Unknown': 1, 'Other': 2, 'Server Blade': 3, 'Connectivity Switch': 4, 'System Management Module': 5,
              'Processor Module': 6, 'I/O Module': 7, 'Memory Module': 8, 'Daughter board': 9, 'Motherboard': 10,
              'Processor/Memory Module': 11, 'Processor/IO Module': 12, 'Interconnect board': 13}
try:
    board_type = re.search("Type: ([0-9A-Za-z ]+)", dmi_board).group(1)
    board_type = str(board_dict.get(board_type))
except:
    board_type = '** No value to retrieve **'

dmi_info['DmiBoardBoardType'] = board_type

for v in dmidecode.system().values():
    if type(v) == dict and v['dmi_type'] == 1:
        dmi_info['DmiSystemSKU'] = v['data']['SKU Number']
        system_family = v['data']['Family']
        system_serial = v['data']['Serial Number']
        dmi_info['DmiSystemVersion'] = "string:" + v['data']['Version']
        dmi_info['DmiSystemProduct'] = v['data']['Product Name']
        dmi_info['DmiSystemVendor'] = v['data']['Manufacturer']

if not system_family:
    dmi_info['DmiSystemFamily'] = "Not Specified"
else:
    dmi_info['DmiSystemFamily'] = system_family

# Create a new UUID
newuuid = str(uuid.uuid4())
dmi_info['DmiSystemUuid'] = newuuid.upper()
# Create a new system serial number
dmi_info['DmiSystemSerial'] = (serial_randomize(0, len(system_serial)))

for v in dmidecode.chassis().values():
    dmi_info['DmiChassisVendor'] = v['data']['Manufacturer']
    chassi_serial = v['data']['Serial Number']
    dmi_info['DmiChassisVersion'] = v['data']['Version']
    dmi_info['DmiChassisType'] = v['data']['Type']

# Based on the list from http://www.dmtf.org/sites/default/files/standards/documents/DSP0134_3.0.0.pdf
chassi_dict = {'Other': 1, 'Unknown': 2, 'Desktop': 3, 'Low Profile Desktop': 4, 'Pizza Box': 5, 'Mini Tower': 6,
               'Tower': 7, 'Portable': 8, 'Laptop': 9, 'Notebook': 10, 'Hand Held': 11, 'Docking Station': 12,
               'All in One': 13, 'Sub Notebook': 14, 'Space-saving': 15, 'Lunch Box': 16, 'Main Server Chassis': 17,
               'Expansion Chassis': 18, 'SubChassis': 19, 'Bus Expansion Chassis': 20, 'Peripheral Chassis': 21}
dmi_info['DmiChassisType'] = str(chassi_dict.get(dmi_info['DmiChassisType']))
# python-dmidecode does not reveal all values .. this is plan B
chassi = commands.getoutput("dmidecode -t3")
try:
    dmi_info['DmiChassisAssetTag'] = re.search("Asset Tag: ([0-9A-Za-z ]*)", chassi).group(1)
except:
    dmi_info['DmiChassisAssetTag'] = '** No value to retrieve **'

# Create a new chassi serial number
dmi_info['DmiChassisSerial'] = (serial_randomize(0, len(chassi_serial)))

for v in dmidecode.processor().values():
    dmi_info['DmiProcVersion'] = v['data']['Version']
    dmi_info['DmiProcManufacturer'] = v['data']['Manufacturer']['Vendor']
# OEM strings
try:
    for v in dmidecode.type(11).values():
        oem_ver = v['data']['Strings']['3']
        oem_rev = v['data']['Strings']['2']
except:
    pass
try:
    dmi_info['DmiOEMVBoxVer'] = oem_ver
    dmi_info['DmiOEMVBoxRev'] = oem_rev
except:
    dmi_info['DmiOEMVBoxVer'] = '** No value to retrieve **'
    dmi_info['DmiOEMVBoxRev'] = '** No value to retrieve **'

# Write all data collected so far to file
file_name="vboxmods.sh"

logfile = file('/tmp/'+file_name, 'w+')
logfile.write('# Generated on: ' + time.strftime("%H:%M:%S") + '\n')

for k, v in sorted(dmi_info.iteritems()):
    if '** No value to retrieve **' in v:
        logfile.write('# VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/pcbios/0/Config/' + k + '\t' + v + '\n')
    else:
        logfile.write('VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/pcbios/0/Config/' + k + '\t\'' + v + '\'\n')
# Disk information
disk_dmi = {}
try:
    if os.path.exists("/dev/sda"):
        # Disk serial
        disk_serial = commands.getoutput(
            "hdparm -i /dev/sda | grep -o 'SerialNo=[A-Za-z0-9_\+\/ .\"-]*' | awk -F= '{print $2}'")
        disk_dmi['SerialNumber'] = (serial_randomize(0, len(disk_serial)))
        # Check for HP Legacy RAID
    elif os.path.exists("/dev/cciss/c0d0"):
        # Needs smartctl to be able to get the correct information
        if os.path.exists("/usr/sbin/smartctl"):
            hp_old_raid = commands.getoutput("smartctl -d cciss,1 -i /dev/cciss/c0d0")
            disk_serial = re.search("Serial number:([0-9A-Za-z ]*)", hp_old_raid).group(1).replace(" ", "")
            disk_dmi['SerialNumber'] = (serial_randomize(0, len(disk_serial)))
        else:
            print "Install smartmontools: apt-get install smartmontools"
except OSError:
    print "Haz RAID?"
    print commands.getoutput("lspci | grep -i raid")

# Disk firmeware rev
try:
    if os.path.exists("/dev/sda"):
        disk_fwrev = commands.getoutput(
            "hdparm -i /dev/sda | grep -o 'FwRev=[A-Za-z0-9_\+\/ .\"-]*' | awk -F= '{print $2}'")
        disk_dmi['FirmwareRevision'] = disk_fwrev
    elif os.path.exists("/dev/cciss/c0d0"):
        # Needs smartctl to be able to get the correct information
        if os.path.exists("/usr/sbin/smartctl"):
            hp_old_raid = commands.getoutput("smartctl -d cciss,1 -i /dev/cciss/c0d0")
            disk_dmi['FirmwareRevision'] = re.search("Revision:([0-9A-Za-z ]*)", hp_old_raid).group(1).replace(" ", "")
        else:
            print "Install smartmontools: apt-get install smartmontools"
except OSError:
    print "Haz RAID?"
    print commands.getoutput("lspci | grep -i raid")

# Disk Model number
try:
    if os.path.exists("/dev/sda"):
        disk_modelno = commands.getoutput(
            "hdparm -i /dev/sda | grep -o 'Model=[A-Za-z0-9_\+\/ .\"-]*' | awk -F= '{print $2}'")
        disk_dmi['ModelNumber'] = disk_modelno
    elif os.path.exists("/dev/cciss/c0d0"):
        # Needs smartctl to be able to get the correct information
        if os.path.exists("/usr/sbin/smartctl"):
            hp_old_raid = commands.getoutput("smartctl -d cciss,1 -i /dev/cciss/c0d0")
            disk_dmi['ModelNumber'] = re.search("Product:([0-9A-Za-z ]*)", hp_old_raid).group(1).replace(" ", "")
        else:
            print "Install smartmontools: apt-get install smartmontools"
except OSError:
    print "Haz RAID?"
    print commands.getoutput("lspci | grep -i raid")

# Write more things to file
for k, v in disk_dmi.iteritems():
    if '** No value to retrieve **' in v:
        logfile.write('# VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/piix3ide/0/Config/PrimaryMaster/' + k + '\t' + v + '\n')
    else:
        logfile.write('VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/piix3ide/0/Config/PrimaryMaster/' + k + '\t\'' + v + '\'\n')

# CD-ROM information
cdrom_dmi = {}
if os.path.islink('/dev/cdrom'):
    # CD-ROM serial
    cdrom_serial = commands.getoutput(
        "hdparm -i /dev/cdrom | grep -o 'SerialNo=[A-Za-z0-9_\+\/ .\"-]*' | awk -F= '{print $2}'")
    if cdrom_serial:
        cdrom_dmi['ATAPISerialNumber'] = (serial_randomize(0, len(cdrom_serial)))
    else:
        cdrom_dmi['ATAPISerialNumber'] = "** No value to retrieve **"

    # CD-ROM firmeware rev
    cdrom_fwrev = commands.getoutput("cd-drive | grep Revision | grep  ':' | awk {' print $3 \" \" $4'}")
    cdrom_dmi['ATAPIRevision'] = cdrom_fwrev.replace(" ", "")

    # CD-ROM Model numberA-Za-z0-9_\+\/ .\"-
    cdrom_modelno = commands.getoutput("cd-drive | grep Model | grep  ':' | awk {' print $3 \" \" $4'}")
    cdrom_dmi['ATAPIProductId'] = cdrom_modelno

    # CD-ROM Vendor
    cdrom_vendor = commands.getoutput("cd-drive | grep Vendor | grep  ':' | awk {' print $3 '}")
    cdrom_dmi['ATAPIVendorId'] = cdrom_vendor
else:
    logfile.write('# No CD-ROM detected: ** No values to retrieve **\n')

# And some more
for k, v in cdrom_dmi.iteritems():
    if '** No value to retrieve **' in v:
        logfile.write('# VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/piix3ide/0/Config/SecondaryMaster/' + k + '\t' + v + '\n')
    else:
        logfile.write('VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/piix3ide/0/Config/SecondaryMaster/' + k + '\t\'' + v + '\'\n')

# Get the DSDT image
#os.system("dd if=/sys/firmware/acpi/tables/DSDT of=DSDT.bin >/dev/null 2>&1")
# Write to file
# Da un error de que la tabla ACPI es mayor de 64KB, aunque lo comente, si luego ejecuto el batch dentro del Guest, pasa las pruebas
#logfile.write('VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/acpi/0/Config/CustomTable\t\'' + os.getcwd() + '/DSDT.bin\'\n')

acpi_misc = commands.getoutput('acpidump -s | grep DSDT | grep -o "\(([A-Za-z0-9].*)\)" | tr -d "()"')
acpi_list = acpi_misc.split(' ')
acpi_list = filter(None, acpi_list)

logfile.write('VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/acpi/0/Config/AcpiOemId\t\'' + acpi_list[1] + '\'\n')
logfile.write('VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/acpi/0/Config/AcpiCreatorId\t\'' + acpi_list[4] + '\'\n')
logfile.write('VBoxManage setextradata '+vm_name+' VBoxInternal/Devices/acpi/0/Config/AcpiCreatorRev\t\'' + acpi_list[5] + '\'\n')

# Randomize MAC address, based on onboard interface MAC
mac_seed1 = ':'.join(re.findall('..', '%012x' % uuid.getnode()))[0:9]
big_mac1 = mac_seed1 + "%02x:%02x:%02x" % (
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255),
)
le_big_mac1 = re.sub(':', '', big_mac1)

# The last thing!
logfile.write('VBoxManage modifyvm '+vm_name+' --macaddress1\t' + le_big_mac1 +'\n')
# Done!
logfile.close()

print '	Finished: A template shell script has been created named:', file_name
print '\n[*] Creating guest based modification file (to be run inside the guest)'

# Write all data to file
file_name2="vboxmods.bat"
logfile = file('/srv/ftp/'+file_name2, 'w+')

manu = acpi_list[1]

# DSDT
logfile.write('@reg copy HKLM\HARDWARE\ACPI\DSDT\VBOX__ HKLM\HARDWARE\ACPI\DSDT\\' + manu + ' /s /f\n\n')
logfile.write('@reg delete HKLM\HARDWARE\ACPI\DSDT\VBOX__ /f\n\n')

logfile.write('@reg copy HKEY_LOCAL_MACHINE\HARDWARE\ACPI\DSDT\\' + manu + '\VBOXBIOS HKEY_LOCAL_MACHINE\HARDWARE\ACPI\DSDT\\' + manu + '\\' + acpi_list[2] + '___' + ' /s /f\n\n')
logfile.write('@reg delete HKEY_LOCAL_MACHINE\HARDWARE\ACPI\DSDT\\' + manu + '\VBOXBIOS /f\n\n')

logfile.write('@reg copy HKEY_LOCAL_MACHINE\HARDWARE\ACPI\DSDT\\' + manu + '\\' + acpi_list[2] + '___\\00000002 HKEY_LOCAL_MACHINE\HARDWARE\ACPI\DSDT\\' + manu + '\\' + acpi_list[2] + '___\\' + acpi_list[3] + ' /s /f\n\n')
logfile.write('@reg delete HKEY_LOCAL_MACHINE\HARDWARE\ACPI\DSDT\\' + manu + '\\' + acpi_list[2] + '___\\00000002 /f\n')

# FADT
logfile.write('@reg copy HKEY_LOCAL_MACHINE\HARDWARE\ACPI\FADT\\' + manu + '\VBOXFACP HKEY_LOCAL_MACHINE\HARDWARE\ACPI\FADT\\' + manu + '\\' + acpi_list[2] + '___  /s /f\n\n')
logfile.write('@reg delete HKEY_LOCAL_MACHINE\HARDWARE\ACPI\FADT\\' + manu + '\VBOXFACP /f\n')
logfile.write('@reg copy HKEY_LOCAL_MACHINE\HARDWARE\ACPI\FADT\\' + manu + '\\' + acpi_list[2] + '___\\00000001 HKEY_LOCAL_MACHINE\HARDWARE\ACPI\FADT\\' + manu + '\\' + acpi_list[2] + '___\\' + acpi_list[3] + ' /s /f\n\n')
logfile.write('@reg delete HKEY_LOCAL_MACHINE\HARDWARE\ACPI\FADT\\' + manu + '\\' + acpi_list[2] + '___\\00000001 /f\n\n')

# RSDT
logfile.write('@reg copy HKEY_LOCAL_MACHINE\HARDWARE\ACPI\RSDT\\' + manu + '\VBOXRSDT HKEY_LOCAL_MACHINE\HARDWARE\ACPI\RSDT\\' + manu + '\\' + acpi_list[2] + '___  /s /f\r\n')
logfile.write('@reg delete HKEY_LOCAL_MACHINE\HARDWARE\ACPI\RSDT\\' + manu + '\VBOXRSDT /f\r\n')
logfile.write('@reg copy HKEY_LOCAL_MACHINE\HARDWARE\ACPI\RSDT\\' + manu + '\\' + acpi_list[2] + '___\\00000001 HKEY_LOCAL_MACHINE\HARDWARE\ACPI\RSDT\\' + manu + '\\' + acpi_list[2] + '___\\' + acpi_list[3] + ' /s /f\r\n')
logfile.write('@reg delete HKEY_LOCAL_MACHINE\HARDWARE\ACPI\RSDT\\' + manu + '\\' + acpi_list[2] + '___\\00000001 /f\r\n')


# SystemBiosVersion - TODO: get real values
logfile.write('@reg add HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System /v SystemBiosVersion /t REG_MULTI_SZ /d "' + acpi_list[1] + ' - ' + acpi_list[0] + '" /f\n\n')
# VideoBiosVersion - TODO: get real values
logfile.write('@reg add HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System /v VideoBiosVersion /t REG_MULTI_SZ /d "' + acpi_list[0] + '" /f\n')
# SystemBiosDate
d_month, d_day, d_year = dmi_info['DmiBIOSReleaseDate'].split('/')

if len(d_year) > 2:
    d_year = d_year[:2]

logfile.write('@reg add HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System /v SystemBiosDate /t REG_MULTI_SZ /d "' + d_month + '/' + d_day + '/' + d_year + '" /f\n')


# Prevent WMI identification
logfile.write('@reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\PlugPlay /v Start /t REG_MULTI_SZ /d "4" /f\r\n')
#The system have to be rebooted for this to work, don't know why

# FW, Updates, IP and DNS settings
logfile.write('netsh firewall set opmode disable\n')

logfile.write('@reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update" /v AUOptions /t REG_DWORD /d 1 /f\n')

shortScript='''
	@echo off

	set _enabled=Habilitado
	set _dedicated=Dedicado

	for /f "tokens=1,2,3*" %%i in ('netsh int show interface') do (
		if %%i equ %_enabled% (
			if %%j equ %_dedicated% (
				netsh int ip set address "%%k %%l" static '''+guest_ip+''' 255.255.255.0 '''+host_ip+''' 1
				netsh int ip set dns "%%k %%l" static '''+guest_primary_dns+'''
		   	 )
		)
	)
	ipconfig /flushdns

	:EOF'''
logfile.write(shortScript+'\n')

logfile.close()
print '	Finished: A Windows batch file has been created named:', file_name2

exit()
