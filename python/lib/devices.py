import time
import numpy as np
import config as config
import socket

# importing the module
import logging

class LEDController:
    def __init__(self):
        pass

    def show(self, pixels):
        """
        pixels: numpy.ndarray
            2D array containing RGB pixel values for each of the LEDs.
            The shape of the array is (3, n_pixels), where n_pixels is the
            number of LEDs that the device has.
            The array is formatted as shown below. There are three rows
            (axis 0) which represent the red, green, and blue color channels.
            Each column (axis 1) contains the red, green, and blue color values
            for a single pixel:
                np.array([ [r0, ..., rN], [g0, ..., gN], [b0, ..., bN]])
            Each value brightness value is an integer between 0 and 255.
        """

        raise NotImplementedError('Show() was not implemented')

    def test(self, n_pixels):
        pixels = np.zeros((3, n_pixels))
        pixels[0][0] = 255
        pixels[1][1] = 255
        pixels[2][2] = 255
        print('Starting LED strip test.')
        print('Press CTRL+C to stop the test at any time.')
        print('You should see a scrolling red, green, and blue pixel.')
        while True:
            self.show(pixels)
            pixels = np.roll(pixels, 1, axis=1)
            time.sleep(0.2)


class ESP8266(LEDController):
    def __init__(self, ip, port=7778):
        """Initialize object for communicating with as ESP8266
        Parameters
        ----------
        ip: str, optional
            The IP address of the ESP8266 on the network. This must exactly
            match the IP address of your ESP8266 device, unless using
            the auto-detect feature.
        port: int, optional
            The port number to use when sending data to the ESP8266. This
            must exactly match the port number in the ESP8266's firmware.
        """
        super().__init__()
        try:
            self._ip = socket.gethostbyname(ip)
        except:
            self._ip = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)


    def show(self, pixels):
        """Sends UDP packets to ESP8266 to update LED strip values
        The ESP8266 will receive and decode the packets to determine what values
        to display on the LED strip. The communication protocol supports LED strips
        with a maximum of 256 LEDs.
        The packet encoding scheme is:
            |i|r|g|b|
        where
            i (0 to 255): Index of LED to change (zero-based)
            r (0 to 255): Red value of LED
            g (0 to 255): Green value of LED
            b (0 to 255): Blue value of LED
        """

        message = pixels.T.clip(0, config.settings["configuration"]["maxBrightness"]).astype(
            np.uint8).ravel().tostring()
        try:
            self._sock.sendto(message, (self._ip, self._port))
        except Exception as Argument:
            logging.exception("Error occured while printing GeeksforGeeks")




