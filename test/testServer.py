#!/usr/bin/python


import socket

_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

_sock.bind( ('192.168.56.1',50001) )
print 'Binded'

for i in range(3):
	print 'Receiving'
	(data, addr)=_sock.recvfrom(32)
	print str(addr)+': '+str(data)

_sock.close()

exit()
