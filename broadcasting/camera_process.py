"""
This code is in charge of taking pictures from the 4 cameras
and posting them to the webserver.
"""
import sys
from SimpleCV import Camera
from util import Config, logger
import time

PERIOD = 5.0

class CameraCapture(object):

    def __init__(self):
        self.n_cameras = int(Config.get("N_CAMERAS"))

        # Initialize the cameras
        self.cameras = []
        for i in xrange(self.n_cameras):
            try:
                self.cameras.append(Camera(camera_index = i))
            except:
                logger.warning("Error opening camera #"+str(i))
        
        self.n_cameras = len(self.cameras)

    def start(self):
        while True:
        try:
            # 1. Capture images from all cameras
            logger.debug("Capturing Images")
            images = self.get_images()
            # 2. Send them to the remote server
            logger.debug("Submitting Images")
            self.post_images(images)
        except:
            logger.warning("Unable to retrieve and send images")

            # Wait
            time.sleep(PERIOD)

    def get_images(self):
        images = []
        for cam in self.cameras:
            # Get Image from camera
            img = cam.getImage()
            images.append(img)
        return images

    def post_images(self, images):
        #Todo: Saving the images to disk until webserver is up and running
        for i in xrange(self.n_cameras):
            img = images[i]
            img.show()
            img.save("images/{}-{}.jpg".format(i, time.time()))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: ./camera_process.py <sensor_config> <network config file>"

    # Initialize configuration
    Config.init(sys.argv[1], sys.argv[2])

    # Start
    logger.debug("Starting Cameras Process")
    cc = CameraCapture()
    cc.start()
