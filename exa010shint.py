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

# Working with the IOS version, getting it and presenting a brief.
print("getting sh ver...")
switch1.show_version()

for line in switch1.ShowVersionBrief:
    print(line)

print(switch1.SystemUpTime)
print()

# for 6x00 platform.
switch1.show_module()
if len(switch1.ShowModule) > 0:
    if switch1.ShowModule[0].find("^") < 0:
        for line in switch1.ShowModule:
            print(line)

# Working with Vlans, getting them and presenting a brief.
print("Populating vlans...")
switch1.populate_vlans()
vlansordered = list(switch1.Vlans.keys())
vlansordered.sort()
for vlankey in vlansordered:
    line = netconfigparser.format_str_space([(switch1.Vlans[vlankey][0], 'r', 7),
                                                          (switch1.Vlans[vlankey][1], 'l', 32),
                                                          (switch1.Vlans[vlankey][2], 'l', 11)])
    print(line)


# Working with interfaces details, getting details from interfaces and producing a report;
# we will use 'show interface status' as a base and add fields to the default output.
print('Populating interfaces...')
switch1.populate_interfaces()

number_interfaces = 0
number_interface_used = 0
up_time_Short = netconfigparser.uptime_to_short(switch1.SystemUpTime)

for line_int_status in switch1.ShowInterfacesStatus:
    if len(line_int_status) > 0:
        interface_short = line_int_status.split()[0]
        if interface_short in switch1.Interfaces.keys():
            interface = interface_short
            description = switch1.Interfaces[interface_short].InterfaceDescription
            status = switch1.Interfaces[interface_short].LineProtocol.split()[-1]
            vlan = switch1.Interfaces[interface_short].AccessModeVlan
            voice = switch1.Interfaces[interface_short].VoiceVlan
            inttype = switch1.Interfaces[interface_short].Type
            if inttype == "10/100/1000BaseTX":
                number_interfaces += 1
            packetsIn = switch1.Interfaces[interface_short].PacketsInput
            packetsOut = switch1.Interfaces[interface_short].PacketsOutput
            if packetsIn or packetsOut > 0:
                used = 'Yes'
                number_interface_used += 1
            else:
                used = 'No'
            lastclearing = switch1.Interfaces[interface_short].LastClearing
            if lastclearing == 'never':
                lastclearing = up_time_Short
            line = netconfigparser.format_str_space([(interface, 'l', 12),
                                                     (description, 'l', 15),
                                                     (status, 'r', 12),
                                                     (vlan, 'r', 8),
                                                     (voice, 'l', 8),
                                                     (inttype, 'l', 20),
                                                     (used, 'l', 4),
                                                     (lastclearing, 'r', 15)
                                                     ])

            print(line)
print("Number of interfaces 10/100/1000BaseTX: ", number_interfaces)
print("Interfaces 10/100/1000BaseTX in use: ", number_interface_used)
print("Percentage use: {:2.0%}".format(number_interface_used/number_interfaces))

switch1.disconnect()
