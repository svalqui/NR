#
#
# Authors: Sergio Valqui
# Created : 2015/08/13
# Modified : 2015/0813



import getpass
import NetDef

gs_DeviceName = input('DeviceName: ')
gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()
gs_EnablePass = getpass.getpass("Enabled Password: ")


switch1 = NetDef.NetworkDevice(gs_DeviceName, gs_UserName, gs_password, gs_EnablePass)

fs_keyinput = ''

while fs_keyinput != 'q':
    fs_keyinput = input()
    if fs_keyinput != "":
        output = switch1.SendCommand(fs_keyinput)
        print(output)
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

