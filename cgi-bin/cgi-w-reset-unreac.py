#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgitb
import cgi
import sys
import datetime
import cisconetworkdevice as cisnetdev
import lib.restapi.ciscoprimeapi as cispriapi

date_format = "%a %b %d %H:%M:%S %Y"
cgitb.enable()
form = cgi.FieldStorage()
user = form.getvalue('user')
password = form.getvalue('password')
enable_password = form.getvalue('enablepassword')
list_ap_cdp = []
list_ap_no_cdp = []
list_devices = []
dict_devices_interfaces = {}

print("Content-Type: text/html;charset=utf-8\n")
print("<pre>")

class_cisco_prime = cpriapi.CiscoPrimeApi(user, password)
list_ap_cdp, list_ap_no_cdp = class_cisco_prime.list_unreachable_neighbors()

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

print("---")
print(datetime.datetime.today().strftime(date_format))
print(sys.version)
print("Hasta la vista baby...............")
print("</pre>")






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