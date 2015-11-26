#
#
# Authors: Sergio Valqui
# Created : 2015/10/08
# Modified : 2015/

import netconfigparser


class Interface:
    """Class container for all attributes and methods related to an Interface"""
    def __init__(self):
        self.InterfaceName = ''
        self.InterfaceShortName=''
        self.ShowInterface = []
        self.ShowInterfaceSwitchport = []
        self.ShowRunningConfiguration = []

    def read_configuration(self):
        pass

    def write_configuration(self, commands):
        pass

    def delete_configuration(self):
        pass


class NetworkDevice:
    """ Class container for all attributes and methods related to a Network Device
        .. thinking if interfaces should be a list or Dictionary.... ummmm....
     """
    def __init__(self, device_name, user_name, user_password, enable_password, device_type='cisco_ios'):
        """ Initializing containers"""
        self.DeviceName = device_name
        self.UserName = user_name
        self.UPassword = user_password
        self.EnablePassword = enable_password
        self.ShowRunning = ''
        self.Interfaces = []
        self.Vlans = {}
        self.Modules = []
        self.ShowInterfacesStatus = []
        self.VRF = {}
        self.ShowVersion = ''
        self.ShowVlan = ''

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
        self.Device_Connection = ConnectHandler(**self.Cisco_Device)

    def send_command(self, command):
        output = self.Device_Connection.send_command(command)
        return output

    def disconnect(self):
        self.Device_Connection.disconnect()

    def show_version(self):
        self.ShowVersion = self.send_command("sh ver")

    def show_running(self):
        self.ShowRunning = self.send_command("sh run")

    def get_vlans(self):
        self.ShowVlan = self.send_command("sh vlan")
        self.Vlans = netconfigparser.show_vlan_to_dictionary(self.ShowVlan)

    def get_int_status(self):
        self.ShowInterfacesStatus = self.send_command("sh int status")
        self.ShowInterfacesStatus = self.ShowInterfacesStatus.splitlines()

    def populate_interfaces(self):
        ListShowInt = netconfigparser.show_interface_to_list(self.send_command("sh int"))
        ListShowIntSwi = netconfigparser.show_interface_switchport_to_list(self.send_command("sh int switchport"))
        #shointswi = netconfigparser.show_interface_switchport_to_list(self.ShowInterfaceSwitchport)

        for i in ListShowInt:
            swi_int = Interface()
            interface_name = i[0].split()[0]



            print(i)
            print()

        #for j in shointswi:
        #    print(j)
         #   print()








