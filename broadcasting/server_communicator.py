import sys
import time
import threading
from socket import *
from util import logger
from util import Config
import httplib

POST_DATA_FORMAT = "photon_id={}&sensor_type={}&value={}&gathered_at={}"

class ServerCommunicator(object):
    """
    Listens to the data spit out by the PhotonCommunicator via UDP and
    forwards it to the remote web server via POST requests
    """

    def __init__(self):
        self.threads = []

        for sensor in Config.sensors:
            self.threads.append(DataPoster(sensor))

    def start(self):
        # Start the thread for each sensor
        logger.debug("Starting all DataPoster threads")
        for thread in self.threads:
            thread.start()

        # Wait fo rall threads to finish
        # In theory this should run forever
        for thread in self.threads:
            thread.join()

        logger.debug("All DataPoster Threads joined");


class DataPoster(threading.Thread):
    def __init__(self, sensor):
        super(DataPoster, self).__init__()
        self.sensor = sensor
        self.socket = self.get_socket(sensor)

    def get_socket(self, sensor):
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((Config.get("BROADCAST_RECEIVING_IP"), sensor.udp_port))
        return s

    def run(self):
        logger.debug("Start DataPoster: " + str(self.sensor))
        while True:
            # Wait for the next data point
            data = self.socket.recv(512)
            logger.debug("Received Data for "+str(self.sensor))

            # Validate by castings to a float
            try:
                data = float(data)
            except:
                logger.warning("Unable to cast value:"+str(data))
                continue

            # Post the value to the webserver
            try:
                self.post_data(data)
            except:
                logger.warning("Unable to POST data")

    def post_data(self, data):
        post_data = POST_DATA_FORMAT.format(self.sensor.photon_id,
                                            self.sensor.sensor_name,
                                            data,
                                            time.time())
        http = httplib.HTTPConnection(Config.get("WEBSERVER_POST_URL"))
        resp = http.request("POST", Config.get("WEBSERVER_POST_URI"), post_data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: ./server_communicator.py <sensor config file> <network config file>"

    # Initialize configuration
    Config.init(sys.argv[1], sys.argv[2])

    # Start
    logger.debug("Starting Server Communicator")
    sc = ServerCommunicator()
    sc.start()