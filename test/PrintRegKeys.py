# Print all the registry keys of a windows system

import _winreg

def traverse(root, key, h_keys):
    hKey = _winreg.OpenKey(root, key)
    try:
        i = 0
        while True:
            strFullSubKey = ""
            try:
                strSubKey = _winreg.EnumKey(hKey, i)
                if (key != ""):
                    strFullSubKey = key + "\\" + strSubKey
                else:
                    strFullSubKey = strSubKey
            except WindowsError:
                hKey.Close()
                return
            traverse(root, strFullSubKey, h_keys)
            h_keys.append(strFullSubKey)
            i += 1

    except  WindowsError:
        hKey.Close()
global h_keys
h_keys = list()

HIVES = {
    "HKEY_LOCAL_MACHINE" : _winreg.HKEY_LOCAL_MACHINE,
    "HKEY_CURRENT_USER" : _winreg.HKEY_CURRENT_USER,
    "HKEY_CLASSES_ROOT" : _winreg.HKEY_CLASSES_ROOT,
    "HKEY_USERS" : _winreg.HKEY_USERS,
    "HKEY_CURRENT_CONFIG" : _winreg.HKEY_CURRENT_CONFIG
}
f=open('regkeys.txt','w+')
for h in HIVES:
    traverse (HIVES[h],"",h_keys)
    for h in h_keys:
        f.write(h+'\r\n')

f.close()



f=open('regkeys.txt', 'r')
f2=open('out.txt', 'w+')
line=f.readline()
line=line.upper()
while line!='':
	line=f.readline()
	line=line.upper()
	try:
		re.search('VBOX', line).group(0)
		f2.write(line)
	except:
		pass
	try:
		re.search('VIRTUAL', line).group(0)
		f2.write(line)
	except:
		pass
	try:
		re.search('VIRTUALBOX', line).group(0)
		f2.write(line)
	except:
		pass
f.close()
f2.close()
exit()
