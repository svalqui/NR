# An example series related to IOS upgrades
# .
#
# Authors: Sergio Valqui
# Created : 2016/04/
# Modified : 2016/

import getpass
import netdef
import netconfigparser

gs_DeviceName = input('DeviceName: ')
gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()
gs_EnablePass = getpass.getpass("Enabled Password: ")

switch1 = netdef.NetworkDevice(gs_DeviceName, gs_UserName, gs_password, gs_EnablePass)

# Working with the IOS version, getting it and presenting a brief.
print("getting sh ver...")
switch1.show_version()
print(netconfigparser.line_from_text("IOS Software", switch1.ShowVersion))
print(switch1.SystemUpTime)
print(netconfigparser.line_from_text("bytes of memory", switch1.ShowVersion))
print(netconfigparser.line_from_text("bytes of physical memory", switch1.ShowVersion))


switch1.disconnect()
