
import socket
import os
from ctypes import *

data=['Hi, world', 'wolololo', 'Bye, server!']
udp_connection=('192.168.56.1', 50001)
tcp_connection=('192.168.56.1', 50002)

# UDP"
_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

f=open('testClient.txt','w+')
for string in data:
	f.write("UDP"+ string)
	_sock.sendto("UDP"+string, udp_connection)


_sock.close()

# TCP
_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_sock.connect( tcp_connection )
for string in data:
	f.write("TCP"+ string)
	_sock.send("TCP"+string)


_sock.close()

f.close()

# windows API
f_handle=windll.kernel32.CreateFileA("testtest.txt", 0x10000000,0,0,4,0x80,0)
written_data = c_int(0)
windll.kernel32.WriteFile(f_handle, data[0], len(data[0]), byref(written_data),0)
windll.kernel32.CloseHandle(f_handle)

# Other
os.system('ping 192.168.56.1')
os.system('cd')
os.system('''
	dir
	cd "C:\Documents and settings"
	cd asdfghj
	cd Escritorio
	type agent.py
	''')

raw_input()
	
exit()
