import datetime
import time


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
    def __init__(self, command_string, command_time):
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

    def __str__(self):
        return self.command_string

    @staticmethod
    def sort(command1, command2):
        a = command1.time_object
        b = command2.time_object
        a_seconds = datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).seconds
        b_seconds = datetime.timedelta(hours=b.tm_hour, minutes=b.tm_min, seconds=b.tm_sec).seconds
        return a_seconds - b_seconds
