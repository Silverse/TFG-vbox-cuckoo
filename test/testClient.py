
import socket

_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

f=open('cosa.txt','w+')

f.write('Hi, world')
_sock.sendto('Hi, world!', ('192.168.56.1', 50001))
f.write('wolololo')
_sock.sendto('wolololo', ('192.168.56.1', 50001))
f.write('Bye, server!')
_sock.sendto('Bye, server!', ('192.168.56.1', 50001))

f.close()
_sock.close()

exit()
