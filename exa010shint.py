# An example "show interfaces on steroids" to manipulate the output of "sh int status" an
# return something a little bit more useful.
#
# Authors: Sergio Valqui
# Created : 2015/12/
# Modified : 2016/

import getpass
import netdef

gs_DeviceName = input('DeviceName: ')
gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()
gs_EnablePass = getpass.getpass("Enabled Password: ")

switch1 = netdef.NetworkDevice(gs_DeviceName, gs_UserName, gs_password, gs_EnablePass)

print('getting sh ver...')
switch1.show_version()
print(switch1.ShowVersion)

switch1.show_module()
print(switch1.ShowModule)

print('Populating vlans...')
switch1.populate_vlans()

print('Populating interfaces...')
switch1.populate_interfaces()


for i in switch1.ShowInterfacesStatus:
    if len(i) > 0:
        gs_interface = i.split()[0]
        if gs_interface in switch1.Interfaces.keys():
            gs_formated_interface = gs_interface
            gs_formated_description = switch1.Interfaces[gs_interface].Interfacedescription
            gs_formated_status = switch1.Interfaces[gs_interface].LineProtol

            gs_line_to_print = ''


            print(gs_interface)

