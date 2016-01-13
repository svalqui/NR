# Library for the Class, methods related to Network devices;
#
# Authors: Sergio Valqui
# Created : 2015/10/08
# Modified : 2016/

import netconfigparser

class Interface(object):
    """Class container for all attributes and methods related to an Interface, they are part of NetworkDevice"""
    def __init__(self):
        self.InterfaceName = ''
        self.InterfaceShortName = ''
        self.ShowInterface = []
        self.ShowInterfaceSwitchport = []
        self.ShowRunningConfiguration = []
        self.InterfaceDescription = ''
        self.PacketsInput = 0
        self.PacketsOutput = 0
        self.LineProtocol = ''
        self.InputErrors = ''
        self.OutputErrors = ''
        self.LastClearing = ''
        self.AdministrativeMode = ''
        self.AccessModeVlan = ''
        self.VoiceVlan = ''

    def load_interface_details(self):
        """
        fill in class details related/from sh int
        :param:
        :return:
        """
        for line in self.ShowInterface:
            if line.find('Description:') >= 0:
                self.InterfaceDescription = line.replace('Description:', '')
            elif line.find('packets input') >= 0:
                self.PacketsInput = int(line.split()[0])
            elif line.find('packets output') >= 0:
                self.PacketsOutput = int(line.split()[0])
            elif line.find('line protocol') >= 0:
                self.LineProtocol = line
            elif line.find('Last clearing of') >= 0:
                self.LastClearing = line



class NetworkDevice(object):
    """ Class container for all attributes and methods related to a Network Device
    """
    def __init__(self, device_name, user_name, user_password, enable_password, device_type='cisco_ios'):
        """ Initializing containers"""
        self.DeviceName = device_name
        self.UserName = user_name
        self.UPassword = user_password
        self.EnablePassword = enable_password
        self.ShowRunning = ''
        self.Interfaces = {}
        self.Vlans = {}
        self.Modules = []
        self.ShowInterfacesStatus = []
        self.ShowInterfaces = []
        self.ShowInterfaceSwitchport = []
        self.VRF = {}
        self.ShowVersion = ''
        self.ShowVlan = ''

        """ testing using Netmiko
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

    def show_version(self):
        self.ShowVersion = self.send_command("sh ver")
        self.ShowVersion = self.ShowVersion.splitlines()

    def show_module(self):
        self.ShowModule = self.send_command("sh module")
        self.ShowModule = self.ShowModule.splitlines()

    def show_running(self):
        self.ShowRunning = self.send_command("sh run")

    def show_int(self):
        self.ShowInterfaces = self.send_command("show interfaces")
        self.ShowInterfaces = self.ShowInterfaces.splitlines()

    def show_int_status(self):
        self.ShowInterfacesStatus = self.send_command("sh int status")
        self.ShowInterfacesStatus = self.ShowInterfacesStatus.splitlines()

    def show_int_switchport(self):
        self.ShowInterfaceSwitchport = self.send_command("sh int switchport")
        self.ShowInterfaceSwitchport = self.ShowInterfaceSwitchport.splitlines()

    def show_vlan(self):
        self.ShowVlan = self.send_command("sh vlan")
        self.ShowVlan = self.ShowVlan.splitlines()

    def populate_vlans(self):
        """
        :return: {vlan_id_int}: [Vlannumber_str, Vlanname, composite]
        """
        self.show_vlan()
        self.Vlans = netconfigparser.show_vlan_to_dictionary(self.ShowVlan)

    def populate_interfaces(self):

        self.show_int_status()

        self.show_int()
        ListShowInt = netconfigparser.show_interface_to_list(self.ShowInterfaces)

        self.show_int_switchport()
        ListShowIntSwi = netconfigparser.show_interface_switchport_to_list(self.ShowInterfaceSwitchport)

        for shintperint in ListShowInt:
            swi_int = Interface()
            swi_int.InterfaceName = shintperint[0].split()[0]
            swi_int.InterfaceShortName = netconfigparser.int_name_to_int_short_name(swi_int.InterfaceName)
            swi_int.ShowInterface = shintperint
            self.Interfaces[swi_int.InterfaceShortName] = swi_int

        for shintswiperint in ListShowIntSwi:
            intshortname = shintswiperint[0].split(":")[1].strip()
            self.Interfaces[intshortname].ShowInterfaceSwitchport = shintswiperint

        for intkey in self.Interfaces.keys():
            #print(dir(self.Interfaces[intkey]))
            a = self.Interfaces[intkey]
            #print("--+")
            #print(dir(a))
            a.load_interface_details()






