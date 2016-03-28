import sys
import time
from socket import *
from util import logger
from util import Config
import httplib
import random

PERIOD = 1.0

class PhotonCommunicator(object):
    """
    Uses the Photon Cloud API to communicate with the Photons and output the sensor readings
    to the appropriate UDP Ports.
    """

    def __init__(self):
        self.socket = PhotonCommunicator.get_broadcast_socket()

    """
    Return a broadcast UDP Socket
    """
    @staticmethod
    def get_broadcast_socket():
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(('', 0))
        return s

    def start(self):
        while True:
            start_time = time.time()

            try:
                self.get_and_send()
            except Exception, e:
                print e.message

            elapsed_time = time.time() - start_time
            logger.debug("get_and_send processing time {}".format(elapsed_time))

            # Wait before we execute the next round
            time.sleep(max(0, PERIOD - elapsed_time))

    def get_and_send(self):
        for sensor in Config.sensors:
            #1. Make Photon API request
            value = self.get_value(sensor)

            #2. Send via UDP Port
            self.send_value(sensor, value)

    def get_value(self, sensor):
        return random.randint(0,9999)

    def send_value(self, sensor, value):
        self.socket.sendto(str(value), (Config.get("BROADCAST_IP"), sensor.udp_port))

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "usage: ./photon_communicator.py <sensor config file> <network config file>"

    # Initialize configuration
    Config.init(sys.argv[1], sys.argv[2])

    # Start
    logger.debug("Starting Photon Communicator")
    pc = PhotonCommunicator()
    pc.start()