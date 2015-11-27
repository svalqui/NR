#
#
# Authors: Sergio Valqui
# Created : 2015/08/13
# Modified : 2015/0813



import getpass
import netdef

gs_DeviceName = input('DeviceName: ')
gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()
gs_EnablePass = getpass.getpass("Enabled Password: ")

switch1 = netdef.NetworkDevice(gs_DeviceName, gs_UserName, gs_password, gs_EnablePass)

fs_keyinput = ''

while fs_keyinput != 'q':
    fs_keyinput = input()
    if fs_keyinput != "":
        output = switch1.send_command(fs_keyinput)
        print(output)
        print('--++++++++--')
        switch1.get_vlans()
        for i in switch1.Vlans.items():
            print (i)
        switch1.populate_interfaces()
        for i in switch1.Interfaces.keys():
            print(i)
            print(switch1.Interfaces[i].InterfaceShortName)
            print(switch1.Interfaces[i].InterfaceName)


    else:
        try:
            exec(fs_keyinput)
        except NameError :
            print('NameError')
        except SyntaxError:
            print('SyntaxError')
        except AttributeError:
            print('AttributeError:')
        except TypeError:
            print('TypeError:')
        except KeyError:
            print('KeyError:')
        except ValueError:
            print('ValueError:')

switch1.Disconnect()
print('finished for now')

