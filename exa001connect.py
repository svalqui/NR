# An example a connection to a network device
# return something a little bit more useful.
#  Genesis of connecting to a network devices
# #
# Authors: Sergio Valqui
# Created : 2017/02
# Modified : 2017/02

import getpass
from datetime import datetime
from netmiko import ConnectHandler
import telnetlib

device_name = input('DeviceName or IP: ')
user_name = getpass.getpass("Username: ")
password = getpass.getpass()

# Using telnetlib

print("Connecting to: ", device_name, " using telnetlib")
telnet_connection = telnetlib.Telnet(device_name)

telnet_connection.read_until(b"Username: ")
telnet_connection.write(user_name.encode('ascii') + b"\n")
if password:
    telnet_connection.read_until(b"Password: ")
    telnet_connection.write(password.encode('ascii') + b"\n")

telnet_connection.write(b"sh ver\n")
telnet_connection.write(b"exit\n")

print(telnet_connection.read_all().decode('ascii'))

telnet_connection.close()

# Using Netmiko

Net_Device = {
    'device_type': device_type,
    'ip': device_name,
    'username': user_name,
    'password': password,
}

Device_Connection = ConnectHandler(**self.Cisco_Device)


# Reference http://stackoverflow.com/questions/19671936/telnet-cisco-switch-using-python
# https://docs.python.org/3.3/library/telnetlib.html