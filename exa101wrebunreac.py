# Copyright 2019 by Sergio Valqui. All rights reserved.
# Reboot all interfaces where a WAP is in disassociated state.
# wrebunreac.py Wireless reboot unreachable
#
# Authors: Sergio Valqui
# Created : 2016/09
# Modified : 2016/09

import getpass
import lib.restapi.ciscoprimeapi as cpriapi
from networktangents import cisconet
import sys

url_prime = "https://" + input("URL Prime https://")
user_name = getpass.getpass("Username: ")
password = getpass.getpass()

list_ap_cdp = []
list_ap_no_cdp = []

class_cisco_prime = cpriapi.CiscoPrimeApi(user_name, password, url_prime)

list_ap_cdp, list_ap_no_cdp = class_cisco_prime.list_unreachable_neighbors()

list_devices = []
dict_devices_interfaces = {}

print("ready for resetting:")
for device_name in list_ap_cdp:
    print(device_name)
    if device_name[1] not in list_devices:
        list_devices.append(device_name[1])
    list_devices.sort()
    if device_name[1] not in dict_devices_interfaces:
        dict_devices_interfaces[device_name[1]] = []
    dict_devices_interfaces[device_name[1]].append(device_name[2])

print()

for device_name in list_devices:
    print("  ", device_name, " :", dict_devices_interfaces[device_name])

enable_password = getpass.getpass("Enable Password :")

for device_name in list_devices:
    print("Connecting to :", device_name)
    connected = False

    try:
        network_device = cisconet.Device(device_name, user_name, password, enable_password)
        connected = True
    except ValueError:
        line_log = "Could NOT connect to: " + network_device + " Possible empty/unknown character in file"
        print(line_log)
    except:
        line_log = "Error: "
        print(line_log, sys.exc_info()[0])
        print(line_log, sys.exc_info()[1])
        print(line_log, sys.exc_info()[2], "\n")

    if connected:
        print("Resetting :", dict_devices_interfaces[device_name])
        network_device.reset_interfaces(dict_devices_interfaces[device_name])
        network_device.disconnect()
        print("  finished with: ", device_name, "\n")


