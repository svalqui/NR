# Network Device source class
# Authors: Sergio Valqui
# Created : 2016/08/31
# Modified : 2016/
# to contain all common properties and functions for all network devices


class NetworkDevice(object):
    """ Class container for all attributes and methods related to a Network Device
    """
    def __init__(self, device_name, user_name, user_password, enable_password, device_type='cisco_ios'):
        self.DeviceName = device_name
        self.UserName = user_name
        self.UPassword = user_password
        self.EnablePassword = enable_password
        self.Interfaces = {}
        self.Vlans = {}
        self.VRF = {}
        self.MacAddress = {}

        """ testing using Netmiko as seems stable
        """

        from netmiko import ConnectHandler
        self.Cisco_Device = {
            'device_type': device_type,
            'ip': self.DeviceName,
            'username': self.UserName,
            'password': self.UPassword,
            'secret': self.EnablePassword,
        }
        self.Device_Connection = ConnectHandler(**self.Cisco_Device)

    def send_command(self, command):
        output = self.Device_Connection.send_command(command)
        return output

    def disconnect(self):
        self.Device_Connection.disconnect()

    def ios_version(self):
        return

    def clear_txt_configuration(self):
        return

    def mac_address(self):



