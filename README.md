#TFG: VirtualBox + Cuckoo hardening against evesive malware
## What is this?
This is my Bachelor Degree's Thesis/Project (shortened as TFG in spanish) of the Telecommunication Engineering degree (Major in Telematic) of the University of Zaragoza, Spain.

## What are the guide-lines?
A study of the most common techniques used by evasive malware in order to detect if the sample is being analyzed. Then a set of measures will be chosen and implemented as Python scripts (this is the point of the repository). Finally the system will be tested against different tools and real malware with evasive behavior.

## What it does for now
Tested on Ubuntu 14.04 LTS, VirtualBox 4.3.10 and Cuckoo 1.2.
Creates a user in the system for Cuckoo usage.
Creates a Vbox VM with proper configuration (network, system and so on).
Configures a vsftpd server to be used in the VM.
Applies the @nsmfoo 's antivmdetection measures (in and out of the VM) except the DSDT table because my laptop have too many cores to fit the Vbox maximum (the lines are commented but not erased) and other automated measures like changing the default IP's, disabling firewalls, etc.
Downloads and installs all the prerequisites of Cuckoo and antivmdetection (Not truly tested yet).
Modifies cuckoo's configuration files to work with the system.

## Last PaFish's (@a0rtega) analysis output
[pafish] Start
[pafish] Windows version: 5.1 build 2600
[pafish] CPU vendor: GenuineIntel
[pafish] CPU VM traced by checking the difference between CPU timestamp counters (rdtsc)
[pafish] CPU VM traced by checking the difference between CPU timestamp counters (rdtsc) forcing VM exit
[pafish] Sandbox traced using mouse activity
[pafish] VirtualBox device identifiers traced using WMI
[pafish] Cuckoo hooks information structure traced in the TLS
[pafish] End
