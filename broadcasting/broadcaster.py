# Short example of how to send UDP broadcast packets

import sys, time
from socket import *

BROADCASTING_IP = '255.255.255.255'
PORT = int(sys.argv[1])
PERIOD = 0.001

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', 0))

print "Running..."
while True:
    data = repr(time.time()) + '\n'
    s.sendto(data, (BROADCASTING_IP, PORT))
    time.sleep(PERIOD)
