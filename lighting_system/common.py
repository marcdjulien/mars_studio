import datetime
import time
import socket
import sys
from globals import logger

COMMAND_TRANSFER = "a"
FILE_TRANSFER = "b"
CHUNK_SIZE = 65536

class SocketCreationException(Exception):
    pass


class Connection(object):
    """

    """
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
    """

    """
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
    """

    """
    def recv_data(self):
        """

        :return: A list containing the data type, and information.
                 If a command is transferred, the command will be in the data.
                 If a file transfer is transferred, the socket will be in the data.
        """
        transfer_type = self.sock.recv(1)
        # Return the command
        if transfer_type == COMMAND_TRANSFER:
            command = self.sock.recv(CHUNK_SIZE)
            return [transfer_type, command]
        # Return the socket to the connection
        elif transfer_type == FILE_TRANSFER:
            return [transfer_type, self.sock]


class InvalidCommandError(Exception):
    """
    Raised when there is an invalid command.
    """
    def __init__(self, command):
        self.msg = "Invalid command: " + command

class Sensors(object):
    pass

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


class Config(object):
    def __init__(self, config_filename):
        self.config_filename = config_filename
        self.config = {}
        try:
            self.read_config()
        except Exception, e:
            logger.warning("Unable to parse config file: "+e.message)
            sys.exit()

    def read_config(self):
        # Store the cast functions for easy access later
        converter = {"string": str,
                     "int": int,
                     "float": float}
        # Open config file
        with open(self.config_filename, "r") as f:
            for line in f:
                line = line.split("#")[0].strip().split()
                if len(line) == 0:
                    continue
                if len(line) != 3:
                    raise Exception("Invalid line in configs:"+line)
                # Parse the line
                data_type = line[0]
                name = line[1]
                if data_type != "list":
                    # Convert to appropriate data type
                    value = converter[data_type](line[2])
                else:
                    value = line[2].split(",")
                # Store in the dictionary
                self.config[name] = value
        print self.config

    def __getattr__(self, item):
        if self.config.has_key(item):
            return self.config[item]
        else:
            raise AttributeError