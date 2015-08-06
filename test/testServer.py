#!/usr/bin/python


import socket
import threading
import os


def UDPserver():
	_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	_sock.bind( ('192.168.56.1',50001) )
	print 'Binded'

	for i in range(3):
		print 'Receiving UDP'
		(data, address)=_sock.recvfrom(32)
		print str(address)+': '+str(data)

	_sock.close()
	return

def TCPserver():
	_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	_sock.bind( ('192.168.56.1',50002) )
	_sock.listen(1)
	(clt_sock, address)=_sock.accept()
	for i in range(3):
		print 'Receiving TCP'
		data=clt_sock.recv(32)
		print str(address)+': '+str(data)
	_sock.close()
	clt_sock.close()
	return

def main():
	thread_list=[]
	thread_list.append( threading.Thread(None, UDPserver(), None, None) )
	thread_list.append( threading.Thread(None, TCPserver(), None, None) )
	for thread in thread_list:
		thread.start()
	
	return

main()
os.system('python testServer.py')
exit()
