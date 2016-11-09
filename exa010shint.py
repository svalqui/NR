# An example "show interfaces on steroids" to manipulate the output of "sh int status" and
# return something a little bit more useful.
#
# Authors: Sergio Valqui
# Created : 2015/12/
# Modified : 2016/08

import getpass

from networktangents import cisconet

device_name = input('DeviceName: ')
user_name = getpass.getpass("Username: ")
password = getpass.getpass()
enable_pass = getpass.getpass("Enabled Password: ")

network_device_1 = cisconet.Device(device_name, user_name, password, enable_pass)
network_device_1.show_int_steroids()

