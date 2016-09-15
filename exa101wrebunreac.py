# Reboot all interfaces where a WAP is in disassociated state.
# wrebunreac.py Wireless reboot unreachable
#
# Authors: Sergio Valqui
# Created : 2016/09
# Modified : 2016/09

import getpass
import lib.restapi.ciscoprimeapi as cpriapi
from networktangents import cisconetworkdevice

user_name = getpass.getpass("Username: ")
password = getpass.getpass()

list_ap_cdp = []
list_ap_no_cdp = []

class_cisco_prime = cpriapi.CiscoPrimeApi(user_name, password)

list_ap_cdp, list_ap_no_cdp = class_cisco_prime.list_unreachable_neighbors()

list_devices = []
dict_devices_interfaces = {}

for item in list_ap_cdp:
    if item[1] not in list_devices:
        list_devices.append(item[1])
    list_devices.sort()
    if item[1] not in dict_devices_interfaces:
        dict_devices_interfaces[item[1]] = []
    dict_devices_interfaces[item[1]].append(item[2])

print("ready for resetting:")

for item in list_devices:
    print("  ", item, " :",dict_devices_interfaces[item])

enable_password = getpass.getpass("Enable Password :")

for item in list_devices:
    print("Connecting to :", item)
    network_device = cisconetworkdevice.CiscoNetworkDevice(item, user_name, password, enable_password)
    print("Resetting :", dict_devices_interfaces[item])
    network_device.reset_interfaces(dict_devices_interfaces[item])
    network_device.disconnect()
    print("  finished with: ", item)

