from common import Command

def parse_light_control_file(filename):
    """
    Parses a .light_control and returns a list of Command objects sorted by time.
    :param filename: The filename to parse.
    :return: A list of Command objects.
    """
    commands = []
    with open(filename, "r") as f:
        for line in f:
            command = line.strip().split(COMMENT_DELIMITER)[0]
            toks = command.split(" ")
            if len(toks) >= 2:
                time = toks[0]
                command_string = " ".join(toks[1::])
                command = Command(command_string, time)
                commands.append(command)
            elif len(toks) == 1 and len(toks[0]) == 0:
                continue
            else:
                logging.error("Invalid line in light control file: %s"%(line))
                return []

    commands.sort(Command.sort)
    return commands



import socket
import sys
import threading
from common import IncomingConnection

def something(sock, addr):
    connection = IncomingConnection(addr, sock)
    connection.recv_data()

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 9000 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    threading.Thread(target=something, args=(conn, addr)).start()
s.close()