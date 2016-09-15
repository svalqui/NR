#
#
# Authors: Sergio Valqui
# Created : 2015/08/13
# Modified : 2015/0813

from netmiko import ConnectHandler
import getpass

gs_DeviceName = input('DeviceName: ')
gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()
gs_EnablePass = getpass.getpass("Enabled Password: ")

cisco_881 = {
    'device_type': 'cisco_ios',
    'ip':   gs_DeviceName,
    'username': gs_UserName,
    'password': gs_password,
    #'port' : 22,          # optional, defaults to 22
    'secret': gs_EnablePass,     # optional, defaults to ''
    #'verbose': False,       # optional, defaults to True
 }

net_connect = ConnectHandler(**cisco_881)

fs_keyinput = ''

while fs_keyinput != 'q':
    fs_keyinput = input()
    if fs_keyinput[:1] == "_":
        output = net_connect.send_command(fs_keyinput[1:])
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

net_connect.disconnect()
print('finished for now')


