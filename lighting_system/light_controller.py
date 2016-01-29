from globals import *
from common import *
from threading import *
import time
from Queue import Queue


class LightController(object):
    """
    Used to actuate the light and shade.
    """
    def __init__(self):
        super(LightController, self).__init__()

    def set_light(self, value):
        pass

    def set_shade(self, value):
        pass


class LightCommandInput(Thread):
    """
    Used to receive commands from a remote user.
    """
    def __init__(self, targets):
        super(LightCommandInput, self).__init__()
        # Stores a queue of received commands
        self.command_queue = Queue()
        # A dictionary mapping command names to their python functions
        self.command_targets = targets
        self.configs = Config(CONFIG_FILE)

    def run(self):
        # Create the listening server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Bind the listening server to the correct light port
            self.server.bind(("", self.configs.HABITAT_LIGHTING_SYSTEM_PORT))
            self.server.listen(0)
        except:
            logger.error("Unable to create server.")

        # Wait and listen for commands to come in
        logger.debug("Starting")
        while True:
            # Receive the incoming connection
            sock, addr = self.server.accept()
            # Start a new thread to handle the command
            t = Thread(target=self.receive_and_store, args=(sock, addr))
            t.start()

    def receive_and_store(self, socket, addr):
        """
        Takes an incoming socket and either stores the command
        to the command queue, or performs another action based
        on the command.
        :param socket: The incoming socket connection.
        :param addr: The address of the incoming socket connection.
        :return:
        """

        # Create the incoming connection
        conn = IncomingConnection(addr, socket)
        # Receive the data from the connection
        data = conn.recv_data()
        if not data:
            logger.warning("Invalid data received")
            return

        # Get the type of data
        transfer_type = data[0]

        # Do an appropriate action based on the type of data
        if transfer_type == COMMAND_TRANSFER:
            command_string = data[1]
            command = data[1].split(" ")[0]
            command_object = Command(command_string, "00:00:00", self.command_targets[command])
            self.command_queue.put(command_object)
            logger.debug("LightCommandInput: Command added to queue -> " + data[1])

        elif transfer_type == FILE_TRANSFER:
            logger.warning("File transfer started")
            pass


class LightSystem(Thread):
    """
    Main Controller for the lighting/shading system. Implemented
    as a state machine. This class handles all of the inputs and
    outputs of the system.
    """
    IDLE_STATE = "IDLE"
    MANUAL_STATE = "MANUAL"
    SET_SHADE_STATE = "SET_SHADE"
    SET_LIGHT_STATE = "SET_LIGHT"
    EXIT_STATE = "EXIT"
    LIGHT_PERIOD_CONTROL_CYCLE = 0.050

    def __init__(self, config_filename=CONFIG_FILE, control_period=LIGHT_PERIOD_CONTROL_CYCLE):
        super(LightSystem, self).__init__()

        # The current state of the system
        self.current_state = LightSystem.IDLE_STATE

        # The control period of the system
        self.control_period = control_period

        # The controller to actuate the system
        self.controller = LightController()
        self.command_targets = {"light": self.controller.set_light,
                                "shade": self.controller.set_shade,
                                "manual": self.set_manual_mode}

        # The sensor inputs
        # Todo: Make this a global object
        self.sensors = Sensors()

        # The command inputs
        self.command_input = LightCommandInput(self.command_targets)

        self.configs = Config(config_filename)

    def run(self):
        """
        Runs the state machine.
        Returns in the EXIT state.
        """
        # Start the thread to receive commands
        self.command_input.start()

        # The next time to execute a state
        self.next_time = time.time() + self.control_period
        
        # Run forever!
        logger.debug("Starting")
        while True:
            # Wait for the next control cycle
            if time.time() < self.next_time:
                time.sleep(0.001)
                continue
            else:  # Set the next execution time
                self.next_time += self.control_period

            # Execute the state!
            if self.current_state == LightSystem.IDLE_STATE:
                self.idle_state()
            elif self.current_state == LightSystem.MANUAL_STATE:
                self.manual_state()
            elif self.current_state == LightSystem.SET_LIGHT_STATE:
                self.set_light_state()
            elif self.current_state == LightSystem.SET_SHADE_STATE:
                self.set_shade_state()
            elif self.current_state == LightSystem.EXIT_STATE:
                return

    def idle_state(self):
        pass

    def manual_state(self):
        pass

    def set_light_state(self):
        pass

    def set_shade_state(self):
        pass

    def set_manual_mode(self):
        pass


def main():
    if len(sys.argv) != 3:
        print "Usage: lighting_command.py <config file> <control period>"
        exit()

    config_filename = sys.argv[1]
    control_period = float(sys.argv[2])
    ls = LightSystem(control_period=control_period, config_filename=config_filename)
    ls.start()

if __name__ == "__main__":
    main()