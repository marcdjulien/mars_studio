# Send UDP broadcast packets

import sys, time
from socket import *

BROADCASTING_PORT = int(sys.argv[2])
BROADCASTING_ADDRESS = sys.argv[1]

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((BROADCASTING_ADDRESS, BROADCASTING_PORT))

print "Running..."
while True:
    data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
    print "Received:", data