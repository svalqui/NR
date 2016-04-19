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


switch1 = netdef.NetworkDevice(gs_DeviceName, gs_UserName, gs_password, gs_EnablePass,'cisco_ios')

fs_keyinput = ''

while fs_keyinput != 'q':
    fs_keyinput = input()
    if fs_keyinput != "":
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

switch1.disconnect()
print('finished for now')

