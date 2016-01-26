from globals import *
from common import *
PROMPT = "light-console>"

# Todo: Read form configuration file
HABITAT_CONNECTION = ("localhost", 9000)


class LightConsole(object):
    """

    """

    def __init__(self):
        self.done = False
        logging.debug("LightControl: Initialized")

    def run(self):
        """
        Begins the execution of the main console.
        """
        logging.debug("LightControl: Starting")
        while not self.done:
            input_str = raw_input(PROMPT)
            input_str = input_str.strip()
            self.evaluate(input_str)
        logging.debug("LightControl: Exiting")

    def send_command(self, msg):
        """
        Creates a connection with the remote habitat and sends the command
        :param msg: The command to send
        :return:
        """
        c = OutgoingConnection(HABITAT_CONNECTION, open=True)
        c.send_msg(msg)
        c.close()

    def send_file(self, filename):
        """
        Sends a file to the remote habitat
        :param filename:
        :return:
        """

    def evaluate(self, input_str):
        """
        Verifies the input from the user, and sends the result to the remote
        light_controller program.
        :param input_str: The command enetered by the user.
        :return: True if a valid command was sent successfully.
        """
        # Split up the command into the individual tokens
        toks = input_str.split(" ")

        # Make sure there are a valid amount of tokens in the command
        if len(toks) <= 0:
            self.unrecognized(input_str)
            return False

        command = toks[0]

        if command in ["e", "exit"]:
            self.done = True

        elif command in ["light"]:
            return self.send_light_command(toks[1::])

        elif command in ["shade"]:
            return self.send_shade_command(toks[1::])

        elif command in ["manual"]:
            return self.send_manual_command(toks[1::])

        elif command in ["upload"]:
            pass

        elif command in ["status"]:
            pass

        else:
            self.unrecognized(command)
            return False

    def send_light_command(self, args):
        """
        Verify the input and send to remote location.
        :param args: the arguments for the light command
        :return: True if successfully sent.
        """

        if len(args) != 1:
            print "Invalid number of arguments for 'light' command"
            return False

        try:
            value = float(args[0])
            if not 0.0 <= value <= 1.0:
                print "Argument must be between 0.0 and 1.0"
                return False
        except ValueError:
            print "Invalid argument type"
            return False
        self.send_command("light %f" % value)

    def send_shade_command(self, args):
        """
        Verify the input and send to remote location.
        :param args: the arguments for the shade command
        :return: True if successfully sent.
        """

        if len(args) != 1:
            print "Invalid number of arguments for 'shade' command"
            return False

        try:
            value = float(args[0])
            if not 0.0 <= value <= 1.0:
                print "Argument must be between 0.0 and 1.0"
                return False
        except ValueError:
            print "Invalid argument type"
            return False
        self.send_command("shade %f" % value)

    def send_manual_command(self, args):
        """
        Verify the input and send to remote location.
        :param args: the arguments for the manual command
        :return: True if successfully sent.
        """

        if len(args) != 1:
            print "Invalid number of arguments for 'manual' command"
            return False

        if args[0] not in ["on", "off"]:
            print "Argument must of 'on' or 'off'"
            return False
        else:
            return self.send_command("manual %s" % args[0])

    def unrecognized(self, command):
        print "Unrecognized command: " + command


def main():
    lc = LightConsole()
    lc.run()

if __name__ == "__main__":
    main()
