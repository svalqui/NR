#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgitb
import cgi
import sys
import datetime
import cisconetworkdevice


date_format = "%a %b %d %H:%M:%S %Y"
cgitb.enable()
form = cgi.FieldStorage()
user = form.getvalue('user')
password = form.getvalue('password')
network_device = form.getvalue('networkdevice')
enable_password = form.getvalue('enablepassword')
print("Content-Type: text/html;charset=utf-8\n")
print("<pre>")
device1 = cisconetworkdevice.CiscoNetworkDevice(network_device, user, password, enable_password)
device1.show_int_steroids()
print("---")
print(datetime.datetime.today().strftime(date_format))
print(sys.version)
print("Hasta la vista baby...............")
print("</pre>")
