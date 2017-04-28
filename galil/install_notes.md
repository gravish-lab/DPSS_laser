

# First install gclib 

http://www.galil.com/sw/pub/all/doc/gclib/html/pi.html

# Next install python bindings

http://www.galil.com/sw/pub/all/doc/gclib/html/python.html

# Configure network

Add this to /etc/dhcpcd.conf

'''
interface eth0

static ip_address=192.168.1.50/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
'''

# Install and configure ps3 controller

https://github.com/RetroPie/RetroPie-Setup

In the setup go to manage packages and install the ps3 package. Then go to the setup instructions and pair the ps controller. Press the PS button while plugged into USB and then will be done.


