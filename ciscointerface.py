# Library for the Class, methods related to Network devices;
#
# Authors: Sergio Valqui
# Created : 2015/10/08
# Modified : 2016/

import interface


class Interface(interface):
    """Class container for all attributes and methods related to an Interface, they are part of NetworkDevice"""
    def __init__(self):
        self.ShowInterfacePerInt = []
        self.ShowInterfaceSwitchportPerInt = []
        self.ShowRunningConfigurationPerInt = []
        self.ShowInterfaceCapabilitiesPerInt = []
        self.LineProtocol = ''
        self.LastClearing = ''
        self.AdministrativeMode = ''
        self.AccessModeVlan = ''
        self.VoiceVlan = ''

    def load_interface_details(self):
        """
        fills in class details coming from 'sh int'
        and 'sh int switchport' both should be already filled
        :param:
        :return:
        """
        for line in self.ShowInterfacePerInt:
            if line.find('Description:') >= 0:
                self.InterfaceDescription = line.replace('Description:', '')
            elif line.find('packets input') >= 0:
                self.PacketsInput = int(line.split()[0])
            elif line.find('packets output') >= 0:
                self.PacketsOutput = int(line.split()[0])
            elif line.find('line protocol') >= 0:
                self.LineProtocol = line
            elif line.find('Last clearing of') >= 0:
                self.LastClearing = line.split()[-1]

        for line in self.ShowInterfaceSwitchportPerInt:
            if line.find('Administrative Mode:') >= 0:
                self.AdministrativeMode = line[19:]
            elif line.find('Access Mode VLAN:') >= 0:
                self.AccessModeVlan = line.split()[3]
            elif line.find('Voice VLAN:') >= 0:
                self.VoiceVlan = line.split()[2]

        for line in self.ShowInterfaceCapabilitiesPerInt:
            if line.find('Type:') >= 0:
                self.Type = line.split(":")[1].strip()


