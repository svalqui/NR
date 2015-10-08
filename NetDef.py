#
#
# Authors: Sergio Valqui
# Created : 2015/10/08
# Modified : 2015/10/08

class NetworkDevice:
    """ Class container for all attributes and methods related to a Network Device """
    def __init__(self, DeviceName, UserName, UPassword, EnablePassword):
        """ Initializing containers"""
        self.DeviceName = DeviceName
        self.UserName = UserName
        self.UPassword = UPassword
        self.EnablePassword = EnablePassword
        self.Connected = False
        self.Interfaces = {}
        self.Vlans = {}
        self.Modules = []
        self.ShIntSwitchport = {}
        self.ShIntStatus = {}
        self.VRF = {}

    def GetConnected(self, self.DeviceName, self.UserName, self.UPassword, self.EnablePassword):
        from netmiko import ConnectHandler
        Cisco_Device = {
            'device_type': 'cisco_ios',
            'ip': self.DeviceName,
            'username': self.UserName,
            'password': self.UPassword,
            #'port' : 22,          # optional, defaults to 22
            'secret': self.EnablePassword,     # optional, defaults to ''
            #'verbose': False,       # optional, defaults to True
            }
        Device_Connetion = ConnectHandler(**Cisco_Device)






