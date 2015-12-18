
import getpass
import netdef

gs_DeviceName = input('DeviceName: ')
gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()
gs_EnablePass = getpass.getpass("Enabled Password: ")

switch1 = netdef.NetworkDevice(gs_DeviceName, gs_UserName, gs_password, gs_EnablePass)

for i in switch1.ShowInterfacesStatus:
    if len(i) > 0:
        gs_interface = i.split()[0]
        if gs_interface in switch1.Interfaces.keys():
            gs_formated_interface = gs_interface
            gs_formated_description = switch1.Interfaces[gs_interface].Interfacedescription
            gs_formated_status = switch1.Interfaces[gs_interface].LineProtol

            gs_line_to_print = ''


            print(gs_interface)

