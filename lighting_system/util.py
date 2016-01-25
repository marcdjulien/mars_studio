from globals import *
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