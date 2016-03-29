import sys
import time
from socket import *
from util import logger
from util import Config
import httplib
import json
import struct

PERIOD = 1.0

API_URL = "api.particle.io"


# noinspection PyBroadException
class PhotonCommunicator(object):
    """
    Uses the Photon Cloud API to communicate with the Photons and output the sensor readings
    to the appropriate UDP Ports.
    """

    def __init__(self):
        # Socket used to broadcast data
        self.bsocket = PhotonCommunicator.get_broadcast_socket()
        
        # Socket used to receive incoming packets from the Photon
        self.psocket = PhotonCommunicator.get_photon_socket()

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

    """
    Returns a socket configured to receive data from the Photon
    """
    @staticmethod
    def get_photon_socket():
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', int(Config.get("PHOTON_UDP_IN_PORT"))))
        return s

    def start(self):
        while True:
            start_time = time.time()

            try:
                #self.get_and_send_api()
                self.get_and_send_udp()
            except Exception, e:
                logger.warning("Error forwarding data")

            elapsed_time = time.time() - start_time
            logger.debug("get_and_send processing time {}".format(elapsed_time))

            # Wait before we execute the next round
            time.sleep(max(0, PERIOD - elapsed_time))

    def get_and_send_api(self):
        for sensor in Config.sensors:
            #1. Make Photon API request
            value = self.get_value(sensor)

            #2. Send via UDP Port
            self.send_value(sensor, value)

    def get_and_send_udp(self):
        #1. Get Sensor values from Photon
        data = self.get_values()
        #2. Send values
        for i in xrange(len(Config.sensors)):
            self.send_value(Config.sensors[i], data[i])

    """
    Makes a Photon API call to receive a Sensor Value
    """
    def get_value(self, sensor):
        http = httplib.HTTPSConnection(API_URL)
        http.request("GET", sensor.api_uri)
        response = http.getresponse()

        if response.status != 200:
            logger.warning("Error fetching sensor value")
            raise Exception
        else:
            data = json.loads(response.read())
            return float(data["result"])

    """
    Waits for a UDP Packet from the Photon containing all sensor values
    """
    def get_values(self):
        values = []
        data = self.psocket.recv(512)

        if len(data) != 6*4:
            logger.warning("Invalid packet format")
            raise Exception

        for i in xrange(6):
            value = struct.unpack("I", data[(i*4):(i+1)*4])
            values.append(value[0])
        return values

    """
    Sends a value to the Configure port for this sensor via UDP broadcast.
    """
    def send_value(self, sensor, value):
        self.bsocket.sendto(str(value), (Config.get("BROADCAST_IP"), sensor.udp_port))

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "usage: ./photon_communicator.py <sensor config file> <network config file>"

    # Initialize configuration
    Config.init(sys.argv[1], sys.argv[2])

    # Start
    logger.debug("Starting Photon Communicator")
    pc = PhotonCommunicator()
    pc.start()
