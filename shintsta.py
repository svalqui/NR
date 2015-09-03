#
#
# Authors: Sergio Valqui
# Created : 2015/08/13
# Modified : 2015/0813

from netmiko import ConnetHandler



cisco_881 = {
    'device_type': 'cisco_ios',
    'ip':   '',
    'username': '',
    'password': '',
    'port' : 22,          # optional, defaults to 22
    'secret': '',     # optional, defaults to ''
    #'verbose': False,       # optional, defaults to True
 }

net_connect = ConnetHandler(**cisco_881)

output = net_connect.send_command('sh ver')
print(output)