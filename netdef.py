# Library for the Class, methods related to Network devices;
#
# Authors: Sergio Valqui
# Created : 2015/10/08
# Modified : 2016/

import libnetconparser


class Interface(object):
    """Class container for all attributes and methods related to an Interface, they are part of NetworkDevice"""
    def __init__(self):
        self.InterfaceName = ''
        self.InterfaceShortName = ''
        self.ShowInterfacePerInt = []
        self.ShowInterfaceSwitchportPerInt = []
        self.ShowRunningConfigurationPerInt = []
        self.ShowInterfaceCapabilitiesPerInt = []
        self.InterfaceDescription = ''
        self.PacketsInput = ''
        self.PacketsOutput = ''
        self.LineProtocol = ''
        self.InputErrors = ''
        self.OutputErrors = ''
        self.LastClearing = ''
        self.AdministrativeMode = ''
        self.AccessModeVlan = ''
        self.VoiceVlan = ''
        self.Type = ''

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


class NetworkDevice(object):
    """ Class container for all attributes and methods related to a Network Device
    """
    def __init__(self, device_name, user_name, user_password, enable_password, device_type='cisco_ios'):
        self.DeviceName = device_name
        self.UserName = user_name
        self.UPassword = user_password
        self.EnablePassword = enable_password
        self.ShowVersion = ''
        self.ShowVersionBrief = ''
        self.ChassisModel = ''
        self.ShowRunning = ''
        self.SystemUpTime = ''
        self.Show_File_System = ''
        self.Interfaces = {}
        self.Vlans = {}
        self.ShowModule = []
        self.ShowCdpNeiDet = []
        self.ShowMacAddress = []
        self.ShowInterfacesStatus = []
        self.ShowInterfaces = []
        self.ShowInterfaceSwitchport = []
        self.ShowInterfaceCapabilities = []
        self.ShowEtherchannelPort = []
        self.VRF = {}
        self.ShowVlan = ''
        self.ListIntLonNam = []
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

    def show_version(self):
        self.ShowVersion = self.send_command("sh ver")
        self.ShowVersion = self.ShowVersion.splitlines()
        self.SystemUpTime = libnetconparser.line_from_text("uptime is", self.ShowVersion)
        self.ShowVersionBrief = libnetconparser.show_ver_brief(self.ShowVersion)
        self.ChassisModel = libnetconparser.show_ver_model(self.ShowVersionBrief)

    def show_file_system(self):
        self.Show_File_System = self.send_command("show file systems")
        self.Show_File_System = self.Show_File_System.splitlines()

    def show_module(self):
        self.ShowModule = self.send_command("sh module")
        self.ShowModule = self.ShowModule.splitlines()

    def show_running(self):
        self.ShowRunning = self.send_command("sh run")

    def show_cdp_nei_det(self):
        self.ShowCdpNeiDet = self.send_command("show cdp nei det")
        self.ShowCdpNeiDet = self.ShowCdpNeiDet.splitlines()

    def show_mac_address(self):
        self.ShowMacAddress = self.send_command("show mac address")
        self.ShowMacAddress = self.ShowMacAddress.splitlines()

    def show_int(self):
        self.ShowInterfaces = self.send_command("show interfaces")
        self.ShowInterfaces = self.ShowInterfaces.splitlines()

    def show_int_status(self):
        self.ShowInterfacesStatus = self.send_command("sh int status")
        self.ShowInterfacesStatus = self.ShowInterfacesStatus.splitlines()

    def show_int_switchport(self):
        self.ShowInterfaceSwitchport = self.send_command("sh int switchport")
        self.ShowInterfaceSwitchport = self.ShowInterfaceSwitchport.splitlines()

    def show_int_capabilities(self):
        self.ShowInterfaceCapabilities = self.send_command("sh int capabilities ")
        self.ShowInterfaceCapabilities = self.ShowInterfaceCapabilities.splitlines()

    def show_vlan(self):
        self.ShowVlan = self.send_command("sh vlan")
        self.ShowVlan = self.ShowVlan.splitlines()

    def show_etherchannelport(self):
        self.ShowEtherchannelPort = self.send_command("sh etherchannel port")
        self.ShowEtherchannelPort = self.ShowEtherchannelPort.splitlines()

    def populate_vlans(self):
        """
        :return: {vlan_id_int}: [Vlannumber_str, Vlanname, composite]
        """
        self.show_vlan()
        self.Vlans = libnetconparser.show_vlan_to_dictionary(self.ShowVlan)

    def populate_interfaces(self):
        """
        runs 'sh int status', 'sh int', 'sh int switchport', 'sh int capabilities';
        and fills in NetworkDevice.Interfaces, dictionary;
        items are Interface classes
        :return:
        """
        self.show_int_status()

        self.show_int()
        listshowint = libnetconparser.show_interface_to_list(self.ShowInterfaces)

        self.show_int_switchport()
        listshowintswi = libnetconparser.show_interface_switchport_to_list(self.ShowInterfaceSwitchport)

        for shintperint in listshowint:
            swi_int = Interface()
            swi_int.InterfaceName = shintperint[0].split()[0]
            swi_int.InterfaceShortName = libnetconparser.int_name_to_int_short_name(swi_int.InterfaceName)
            swi_int.ShowInterfacePerInt = shintperint
            self.Interfaces[swi_int.InterfaceShortName] = swi_int
            self.ListIntLonNam.append(swi_int.InterfaceName)

        for shintswiperint in listshowintswi:
            intshortname = shintswiperint[0].split(":")[1].strip()
            self.Interfaces[intshortname].ShowInterfaceSwitchportPerInt = shintswiperint

        self.show_int_capabilities()
        dicshowintcap = libnetconparser.cut_include_from_list(self.ShowInterfaceCapabilities, self.ListIntLonNam)

        for intkey in self.Interfaces.keys():
            intholder = self.Interfaces[intkey]
            if intholder.InterfaceName in dicshowintcap.keys():
                self.Interfaces[intkey].ShowInterfaceCapabilitiesPerInt = dicshowintcap[intholder.InterfaceName]

            intholder.load_interface_details()

    def populate_mac_address(self):
        self.show_mac_address()
        self.MacAddress = libnetconparser.show_mac_to_dictionary(self.ShowMacAddress)

