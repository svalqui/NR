# An example "show interfaces on steroids" to manipulate the output of "sh int status" and
# return something a little bit more useful.
#
# Authors: Sergio Valqui
# Created : 2015/12/
# Modified : 2016/

import getpass
import netdef
import netconfigparser

gs_DeviceName = input('DeviceName: ')
gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()
gs_EnablePass = getpass.getpass("Enabled Password: ")

switch1 = netdef.NetworkDevice(gs_DeviceName, gs_UserName, gs_password, gs_EnablePass)

print('getting sh ver...')
switch1.show_version()
print(netconfigparser.line_from_text("IOS Software", switch1.ShowVersion))
print(netconfigparser.line_from_text("uptime is", switch1.ShowVersion))
print(netconfigparser.line_from_text("bytes of memory", switch1.ShowVersion))
print(netconfigparser.line_from_text("bytes of physical memory", switch1.ShowVersion))

switch1.show_module()
if len(switch1.ShowModule) > 0:
    if switch1.ShowModule[0].find("^") < 0:
        print(switch1.ShowModule)

print('Populating vlans...')
switch1.populate_vlans()
vlansordered = list(switch1.Vlans.keys())
vlansordered.sort()
for vlankey in vlansordered:
    line_to_print = netconfigparser.format_string_spacing([(switch1.Vlans[vlankey][0], 'r',7),
                                                          (switch1.Vlans[vlankey][1], 'l',32),
                                                          (switch1.Vlans[vlankey][2], 'l',11),])
    print(line_to_print)

print('Populating interfaces...')
switch1.populate_interfaces()
print(switch1.ShowInterfacesStatus)

for i in switch1.ShowInterfacesStatus:
    if len(i) > 0:
        gs_interface = i.split()[0]
        if gs_interface in switch1.Interfaces.keys():
            gs_formated_interface = gs_interface
            gs_formated_description = switch1.Interfaces[gs_interface].InterfaceDescription
            gs_formated_status = switch1.Interfaces[gs_interface].LineProtocol

            gs_line_to_print = ''

            print(gs_interface)

