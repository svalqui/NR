# An example a connection to a network device
# return something a little bit more useful.
#  Genesis of connecting to a network devices
# #
# Authors: Sergio Valqui
# Created : 2017/02
# Modified : 2017/09

import getpass
from netmiko import ConnectHandler
import time
import telnetlib

# Device Name, Username and pwd

device_name = input('DeviceName or IP: ')
user_name = getpass.getpass("Username: ")
password = getpass.getpass()

# Using telnetlib

print("\n***Using telnetlib***\n")

print("Connecting to: ", device_name, " using telnetlib")
telnet_connection = telnetlib.Telnet(device_name)

telnet_connection.read_until(b"Username: ")
telnet_connection.write(user_name.encode('ascii') + b"\n")
#print("Passing username")
if password:
    telnet_connection.read_until(b"Password: ")
    telnet_connection.write(password.encode('ascii') + b"\n")
#    print("Passing pw")
#    print(telnet_connection.read_all().decode('ascii'))

value = telnet_connection.expect([b'>', b'Authentication '], 15)

if value[0] == 0:
    print("Logged in ", device_name)
    telnet_connection.write(b"terminal length 0\n")
    telnet_connection.write(b"sh ver\n")
    time.sleep(2)
    telnet_connection.write(b"exit\n")
    print(telnet_connection.read_all().decode('ascii'))

elif value[0] == 1:
    print("Authentication failure")

telnet_connection.close()

# Using Netmiko

print("\n***Using netmiko***\n")

network_device = {
    'device_type': 'cisco_ios',
    'ip': device_name,
    'username': user_name,
    'password': password,
}

device_connection = ConnectHandler(**network_device)

output = device_connection.send_command("sh ver")
print(output)

# Credits Disclaimer
# The below sites/articles/code has been used totally, partially or as reference
#
# http://stackoverflow.com/questions/19671936/telnet-cisco-switch-using-python
# https://docs.python.org/3.3/library/telnetlib.html
# https://github.com/ktbyers/netmiko