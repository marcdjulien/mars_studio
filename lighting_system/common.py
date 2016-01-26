import datetime
import time
import socket

COMMAND_TRANSFER = "a"
FILE_TRANSFER = "b"
CHUNK_SIZE = 65536

class SocketCreationException(Exception):
    pass


class Connection(object):
    def __init__(self, address, sock=None, open=False):
        self.address = address
        self.sock = sock
        if open:
            self.open()

    def open(self):
        if not self.sock:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(self.address)
            self.sock = s

    def close(self):
        if not self.sock:
            raise SocketCreationException
        self.sock.close()


class OutgoingConnection(Connection):
    def send_msg(self, msg):
        if not self.sock:
            raise SocketCreationException
        self.sock.sendall(COMMAND_TRANSFER)
        self.sock.sendall(msg)

    def send_file(self, filename):
        if not self.sock:
            raise SocketCreationException

        f = open(filename, "rb")
        self.sock.sendall(FILE_TRANSFER)
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break  # EOF
            self.sock.sendall(chunk)
        f.close()


class IncomingConnection(Connection):
    def recv_data(self):
        transfer_type = self.sock.recv(1)
        if transfer_type == COMMAND_TRANSFER:
            print self.sock.recv(CHUNK_SIZE)
        elif transfer_type == FILE_TRANSFER:
            print "Incoming File Transfer"


class InvalidCommandError(Exception):
    """
    Raised when there is an invalid command.
    """
    def __init__(self, command):
        self.msg = "Invalid command: " + command


class Command(object):
    """
    Represents a command that can be executed.
    """
    def __init__(self, command_string, command_time, target):
        self. command_string = command_string

        toks = command_string.strip().split(" ")

        if len(toks) <= 0:
            raise InvalidCommandError(command_string)

        if len(toks) == 1:
            self.command = toks[0]

        if len(toks) > 1:
            self.args = toks[1::]

        self.time = command_time
        self.time_object = time.strptime(command_time, "%H:%M:%S")

        self.target = target

    def __str__(self):
        return self.command_string

    def execute(self):
        self.target(*self.args)

    @staticmethod
    def sort(command1, command2):
        a = command1.time_object
        b = command2.time_object
        a_seconds = datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).seconds
        b_seconds = datetime.timedelta(hours=b.tm_hour, minutes=b.tm_min, seconds=b.tm_sec).seconds
        return a_seconds - b_seconds
