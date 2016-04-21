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

print("\ngoing to enabled mode...")
switch1.Device_Connection.enable()

# Working with the IOS version, getting it and presenting a brief.
print("getting sh ver...")
switch1.show_version()

for line in switch1.ShowVersionBrief:
    print(line)

print(switch1.SystemUpTime)
print()

print("getting show file systems....")
switch1.show_file_system()

File_System = netconfigparser.show_fs_to_space_free(switch1.Show_File_System)

for fs in File_System:
    print(fs)

switch1.disconnect()
