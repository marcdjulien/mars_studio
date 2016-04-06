"""
This package contains all common utilities used by the programs.
"""
import logging
from logging import handlers
import sys

# Set up logger
COMMENT_DELIMITER = "#"
LOGGER_FILENAME = ".log"
LOG_FORMAT_STRING = '[%(processName)s:%(funcName)s][%(asctime)s][%(levelname)s]%(message)s'
LOG_FORMAT = logging.Formatter(LOG_FORMAT_STRING)

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

_ch = logging.StreamHandler(sys.stdout)
_ch.setFormatter(LOG_FORMAT)
logger.addHandler(_ch)

_fh = logging.handlers.RotatingFileHandler(LOGGER_FILENAME, maxBytes=(1048576*5), backupCount=7)
_fh.setFormatter(LOG_FORMAT)
logger.addHandler(_fh)

class Config(object):
    """
    Static Configuration class that reads in the configuration of the network, system, and
    sensors at runtime. Edit the .sensor_config files and .system_config files to alter
    the configurations.
    """
    sensors = []
    config = {}

    @staticmethod
    def parse_line(line):
        # Remove comment
        line = line.split("#")[0]
        line = line.strip()
        if len(line) == 0:
            return []
        else:   # Get tokens
            return line.split()

    @classmethod
    def init(cls, sensor_filename, network_filename):
        cls.sensor_filename = sensor_filename
        cls.network_filename = network_filename

        # 1. Read in sensor configuration file
        with open(cls.sensor_filename, "r") as f:
            for line in f:
                toks = Config.parse_line(line)
                if len(toks) == 0:
                    continue
                elif len(toks) != 4:
                    raise Exception("Invalid line:"+line)
                cls.sensors.append(Sensor(*toks))

        # 2. Read in network configuration file
        with open(cls.network_filename, "r") as f:
            for line in f:
                toks = Config.parse_line(line)
                if len(toks) == 0:
                    continue
                elif len(toks) != 2:
                    raise Exception("Invalid line:"+line)
                cls.config[toks[0]] = toks[1]

    @classmethod
    def get(cls, attribute):
        if cls.config.has_key(attribute):
            return cls.config[attribute]
        else:
            raise AttributeError

class Sensor(object):
    """
    Sensor class used to represent the sensors within the system.
    """
    def __init__(self, sensor_name, photon_id, udp_port, api_uri):
        self.sensor_name = sensor_name
        self.udp_port = int(udp_port)
        self.api_uri = api_uri
        self.photon_id = photon_id

    def __str__(self):
        return "({}, {}, {}, {})".format(self.sensor_name, self.photon_id, self.udp_port, self.api_uri)
