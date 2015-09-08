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

output = net_connect.send_command('sh ver')
print(output)