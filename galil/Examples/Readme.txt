This is the source code for the Galil Raspberry Pi Touchscreen HMI Demo and the RIO Datalogging Demo.

INSTALLATION NOTES:
========================
1. Install Raspbian Jessie by following the Raspberry Pi instructions:
https://www.raspberrypi.org/downloads/raspbian/

2. Write the image to an SD card.
https://www.raspberrypi.org/documentation/installation/installing-images/README.md

3. After booting up the Raspberry Pi, update the libraries:

sudo apt-get update

sudo apt-get upgrade

4. Install Galil gclib programming API on the Raspberry Pi:
http://www.galil.com/sw/pub/all/doc/gclib/html/pi.html

5. Install gclib Python wrapper on the Raspberry Pi:
http://www.galil.com/sw/pub/all/doc/gclib/html/python.html

6. Install Kivy by following the instructions on the Kivy website:
https://kivy.org/docs/installation/installation-rpi.html

7. Load the source files into a directory on the Raspberry Pi

8. Run the source files.

example:
python layout.py

