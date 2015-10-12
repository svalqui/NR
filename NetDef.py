#
#
# Authors: Sergio Valqui
# Created : 2015/10/08
# Modified : 2015/10/08

class NetworkDevice:
    """ Class container for all attributes and methods related to a Network Device """
    def __init__(self, device_name, user_name, user_password, enable_password, device_type='cisco_ios'):
        """ Initializing containers"""
        self.DeviceName = device_name
        self.UserName = user_name
        self.UPassword = user_password
        self.EnablePassword = enable_password
        self.Interfaces = {}
        self.Vlans = {}
        self.Modules = []
        self.ShIntSwitchport = {}
        self.ShIntStatus = {}
        self.VRF = {}

        from netmiko import ConnectHandler
        self.Cisco_Device = {
            'device_type': device_type,
            'ip': self.DeviceName,
            'username': self.UserName,
            'password': self.UPassword,
            #'port' : 22,          # optional, defaults to 22
            'secret': self.EnablePassword,     # optional, defaults to ''
            #'verbose': False,       # optional, defaults to True
            }
        self.Device_Connetion = ConnectHandler(**self.Cisco_Device)

    def SendCommand(self, command):
        output = self.Device_Connetion.send_command(command)
        return(output)

    def Disconnect(self):
        self.Device_Connetion.disconnect()







