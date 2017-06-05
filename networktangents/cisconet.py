# Library for the Class, methods related to Network devices;
#
# Authors: Sergio Valqui
# Created : 2015/10/08
# Modified : 2016/

import time
import networktangents

from lib import netconparser
from networktangents import ciscoint
from lib.restapi.maclookapi import QueryMac


class Device(networktangents.NetworkDevice):
    """ Class container for all attributes and methods related to a Network Device
    """
    def __init__(self, device_name, user_name, user_password, enable_password, device_type='cisco_ios'):
        super(Device, self).__init__(device_name, user_name, user_password, enable_password, device_type)
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
        self.base_ip_route = []
        self.ShowModule = []
        self.ShowCdpNeiDet = []
        self.ShowMacAddress = []
        self.ShowInterfacesStatus = []
        self.ShowInterfaces = []
        self.ShowInterfaceSwitchport = []
        self.ShowInterfaceCapabilities = []
        self.ShowEtherchannelPort = []
        self.ShowVRF = []
        self.ShowIPRoute = []
        self.ShowIPRouteVrf = []
        self.VRF = {}
        self.ShowVlan = ''
        self.ListIntLonNam = []
        self.MacAddress = {}
        self.list_commands = []

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
        time.sleep(0.1)
        output = self.Device_Connection.send_command(command, delay_factor=.2)
        return output.splitlines()

    def disconnect(self):
        self.Device_Connection.disconnect()

    def show_version(self):
        self.ShowVersion = self.send_command("sh ver")
        self.SystemUpTime = netconparser.line_from_text("uptime is", self.ShowVersion)
        self.ShowVersionBrief = netconparser.show_ver_brief(self.ShowVersion)
        self.ChassisModel = netconparser.show_ver_model(self.ShowVersionBrief)

    def show_file_system(self):
        self.Show_File_System = self.send_command("show file systems")

    def show_module(self):
        self.ShowModule = self.send_command("sh module")

    def show_running(self):
        self.ShowRunning = self.send_command("sh run")

    def show_cdp_nei_det(self):
        self.ShowCdpNeiDet = self.send_command("show cdp nei det")

    def show_mac_address(self):
        self.ShowMacAddress = self.send_command("show mac address")

    def show_int(self):
        self.ShowInterfaces = self.send_command("show interfaces")

    def show_int_status(self):
        self.ShowInterfacesStatus = self.send_command("sh int status")

    def show_int_switchport(self):
        self.ShowInterfaceSwitchport = self.send_command("sh int switchport")

    def show_int_capabilities(self):
        self.ShowInterfaceCapabilities = self.send_command("sh int capabilities ")

    def show_vlan(self):
        self.ShowVlan = self.send_command("sh vlan")

    def show_vrf(self):
        self.VRF = netconparser.show_vrf_to_dictionary(self.send_command("sh ip vrf"))

    def show_ip_route(self):
        self.base_ip_route = self.send_command("sh ip route")
        self.show_vrf()
        if len(self.VRF) > 0:
            for index in self.VRF.keys():
                ip_route_per_vrf = self.send_command("sh ip route vrf " + index)
                self.VRF[index][2] = ip_route_per_vrf

        for i in self.base_ip_route:
            if i.find('irec') > 0 :
                print (i)

        for index in self.VRF.keys():
            for line in VRF[index][2]: # Routes per vrf
                if line.find('irec') > 0 :
                    print('VRF : ', index, ' subnet : ', line)

    def show_etherchannelport(self):
        self.ShowEtherchannelPort = self.send_command("sh etherchannel port")

    def populate_vlans(self):
        """
        :return: {vlan_id_int}: [Vlannumber_str, Vlanname, composite]
        """
        self.show_vlan()
        self.Vlans = netconparser.show_vlan_to_dictionary(self.ShowVlan)

    def populate_mac_address(self):
        self.show_mac_address()
        # print("calling show mac add to dic")
        self.MacAddress = netconparser.show_mac_to_dictionary(self.ShowMacAddress)
        # print("\n\n\n", self.MacAddress, "\n\n\n")

    def populate_vrf(self):
        """
        :return: {vrf_id_int}: [Vrfnumber_str, Vrfname, composite]
        """
        self.show_vrf()
        self.VRF = netconparser.show_vrf_to_dictionary(self.ShowVRF)

    def populate_interfaces(self):
        """
        runs 'sh int status', 'sh int', 'sh int switchport', 'sh int capabilities',
        'sh mac add';
        and fills in NetworkDevice.Interfaces, dictionary;
        items are Interface classes
        :return:
        """
        self.show_int_status()

        self.show_int()
        listshowint = netconparser.show_interface_to_list(self.ShowInterfaces)

        self.show_int_switchport()
        listshowintswi = netconparser.show_interface_switchport_to_list(self.ShowInterfaceSwitchport)

        # print("calling populate mac add")
        self.populate_mac_address()

        for show_int_per_int in listshowint:  # through "sh interface" per interface
            swi_int = ciscoint.Interface()
            swi_int.InterfaceName = show_int_per_int[0].split()[0]
            swi_int.InterfaceShortName = netconparser.int_name_to_int_short_name(swi_int.InterfaceName)
            swi_int.ShowInterfacePerInt = show_int_per_int
            self.Interfaces[swi_int.InterfaceShortName] = swi_int
            self.ListIntLonNam.append(swi_int.InterfaceName)

        for show_int_sw_per_int in listshowintswi:  # through "sh interface switch" per interface
            intshortname = show_int_sw_per_int[0].split(":")[1].strip()
            self.Interfaces[intshortname].ShowInterfaceSwitchportPerInt = show_int_sw_per_int

        self.show_int_capabilities()
        dicshowintcap = netconparser.cut_include_from_list(self.ShowInterfaceCapabilities, self.ListIntLonNam)

        for key_int in self.Interfaces.keys():  # through all interfaces, key Interface_short_name
            int_holder = self.Interfaces[key_int]
            if int_holder.InterfaceName in dicshowintcap.keys():
                self.Interfaces[key_int].ShowInterfaceCapabilitiesPerInt = dicshowintcap[int_holder.InterfaceName]
                if key_int in self.MacAddress.keys():
                    self.Interfaces[key_int].ListMacAddress = self.MacAddress[key_int]
            int_holder.load_interface_details()

    def configure_interfaces(self, list_interfaces, list_commands, debug=True):
        if debug:
            pass
        self.Device_Connection.enable()
        self.Device_Connection.config_mode()
        if debug:
            print("in \"conf t\" mode")
        for interface in list_interfaces:
            if debug:
                print("int "+interface)
            self.Device_Connection.send_config_set(["int "+interface])
            self.Device_Connection.send_config_set(list_commands)
        self.Device_Connection.exit_config_mode()

    def reset_interfaces(self, list_interfaces, debug=True):
        self.list_commands = ["shutdown", "no shutdown"]
        self.configure_interfaces(list_interfaces, self.list_commands)
        if debug:
            print("reset :", list_interfaces)
        return

    def disable_interfaces(self, list_interfaces):
        self.list_commands = ["shutdown"]
        self.configure_interfaces(list_interfaces, self.list_commands)
        return

    def display_sh_ver_brief(self):
        # Working with the IOS version, getting it and presenting a brief.
        print("getting sh ver...")
        self.show_version()

        for line in self.ShowVersionBrief:
            print(line)

        print(self.SystemUpTime)
        print()

    def display_sh_modules(self):
        # for 6x00 platform.
        self.show_module()
        if len(self.ShowModule) > 0:
            if self.ShowModule[0].find("^") < 0:
                for line in self.ShowModule:
                    print(line)

    def display_sh_vlan_brief(self):
        # Working with Vlans, getting them and presenting a brief.
        print("Populating vlans...")
        self.populate_vlans()
        vlansordered = list(self.Vlans.keys())
        vlansordered.sort()
        for vlankey in vlansordered:
            line = netconparser.format_str_space([(self.Vlans[vlankey][0], 'r', 7),
                                                  (self.Vlans[vlankey][1], 'l', 32),
                                                  (self.Vlans[vlankey][2], 'l', 11)])
            print(line)

    def show_int_steroids(self):
        self.display_sh_ver_brief()
        self.display_sh_modules()
        self.display_sh_vlan_brief()

        # Working with interfaces details, getting details from interfaces and producing a report;
        # we will use 'show interface status' as a base and add fields to the default output.
        print('Populating interfaces...')
        self.populate_interfaces()

        number_interfaces = 0
        number_interface_used = 0
        up_time_short = netconparser.uptime_to_short(self.SystemUpTime)

        for line_int_status in self.ShowInterfacesStatus:
            vlan = ""
            if len(line_int_status) > 0:
                interface_short = line_int_status.split()[0]
                base_t = False
                if interface_short in self.Interfaces.keys():
                    interface = interface_short
                    # print(interface_short)
                    description = self.Interfaces[interface_short].InterfaceDescription
                    status = self.Interfaces[interface_short].LineProtocol.split()[-1]
                    if self.Interfaces[interface_short].AdministrativeMode == "trunk":
                        vlan = "trunk"
                    elif self.Interfaces[interface_short].AdministrativeMode == "routed":
                        vlan = "routed"
                    else:
                        vlan = self.Interfaces[interface_short].AccessModeVlan
                    voice = self.Interfaces[interface_short].VoiceVlan
                    inttype = self.Interfaces[interface_short].Type
                    if inttype.find("10/100/1000BaseT") >= 0:
                        number_interfaces += 1
                        base_t = True
                    packetsIn = self.Interfaces[interface_short].PacketsInput
                    packetsOut = self.Interfaces[interface_short].PacketsOutput
                    if packetsIn or packetsOut > 0:
                        used = 'Yes'
                        if base_t:
                            number_interface_used += 1
                    else:
                        used = 'No'
                    lastclearing = self.Interfaces[interface_short].LastClearing
                    if lastclearing == 'never':
                        lastclearing = up_time_short
                    line = netconparser.format_str_space([(interface, 'l', 12),
                                                          (description, 'l', 15),
                                                          (status, 'r', 12),
                                                          (vlan, 'r', 8),
                                                          (voice, 'l', 8),
                                                          (inttype, 'l', 20),
                                                          (used, 'l', 4),
                                                          (lastclearing, 'r', 15)
                                                          ])

                    print(line)

                    if len(self.Interfaces[interface_short].ListMacAddress) > 0 and \
                                    self.Interfaces[interface_short].AdministrativeMode == "static access":
                        for mac_entry in self.Interfaces[interface_short].ListMacAddress:
                            line = netconparser.format_str_space([(' ', 'r', 65),
                                                                  (str(mac_entry), 'l', 30)
                                                                  ])
                            # print(mac_entry)
                            print(line)

        print("Number of interfaces 10/100/1000BaseT: ", number_interfaces)
        print("Interfaces 10/100/1000BaseT in use: ", number_interface_used)
        print("Interfaces 10/100/1000BaseT spare: ", number_interfaces - number_interface_used)
        print("Percentage use of 10/100/1000BaseT: {:2.0%}".format(number_interface_used/number_interfaces))
        print("\nFinished with: ", self.DeviceName)
        print("\n\n")

        return

    def show_int_steroids_adv(self):
        self.display_sh_ver_brief()
        self.display_sh_modules()
        self.display_sh_vlan_brief()

        # Working with interfaces details, getting details from interfaces and producing a report;
        # we will use 'show interface status' as a base and add fields to the default output.
        print('Populating interfaces...')
        self.populate_interfaces()

        number_interfaces = 0
        number_interface_used = 0
        up_time_short = netconparser.uptime_to_short(self.SystemUpTime)

        for line_int_status in self.ShowInterfacesStatus:
            vlan = ""
            if len(line_int_status) > 0:
                interface_short = line_int_status.split()[0]
                base_t = False
                if interface_short in self.Interfaces.keys():
                    interface = interface_short
                    # print(interface_short)
                    description = self.Interfaces[interface_short].InterfaceDescription
                    status = self.Interfaces[interface_short].LineProtocol.split()[-1]
                    if self.Interfaces[interface_short].AdministrativeMode == "trunk":
                        vlan = "trunk"
                    elif self.Interfaces[interface_short].AdministrativeMode == "routed":
                        vlan = "routed"
                    else:
                        vlan = self.Interfaces[interface_short].AccessModeVlan
                    voice = self.Interfaces[interface_short].VoiceVlan
                    inttype = self.Interfaces[interface_short].Type
                    if inttype.find("10/100/1000BaseT") >= 0:
                        number_interfaces += 1
                        base_t = True
                    packetsIn = self.Interfaces[interface_short].PacketsInput
                    packetsOut = self.Interfaces[interface_short].PacketsOutput
                    if packetsIn or packetsOut > 0:
                        used = 'Yes'
                        if base_t:
                            number_interface_used += 1
                    else:
                        used = 'No'
                    lastclearing = self.Interfaces[interface_short].LastClearing
                    if lastclearing == 'never':
                        lastclearing = up_time_short
                    line = netconparser.format_str_space([(interface, 'l', 12),
                                                          (description, 'l', 15),
                                                          (status, 'r', 12),
                                                          (vlan, 'r', 8),
                                                          (voice, 'l', 8),
                                                          (inttype, 'l', 20),
                                                          (used, 'l', 4),
                                                          (lastclearing, 'r', 15)
                                                          ])

                    print(line)

                    if len(self.Interfaces[interface_short].ListMacAddress) > 0 and \
                                    self.Interfaces[interface_short].AdministrativeMode == "static access":
                        for mac_entry in self.Interfaces[interface_short].ListMacAddress:
                            mac_vendor = QueryMac().mac_company(str(mac_entry))
                            line = netconparser.format_str_space([(' ', 'r', 65),
                                                                  (str(mac_entry), 'l', 30),
                                                                  (mac_vendor, 'l', 20)
                                                                  ])
                            # print(mac_entry)
                            print(line)

        print("Number of interfaces 10/100/1000BaseT: ", number_interfaces)
        print("Interfaces 10/100/1000BaseT in use: ", number_interface_used)
        print("Percentage use of 10/100/1000BaseT: {:2.0%}".format(number_interface_used/number_interfaces))
        print("Percentage use of 10/100/1000BaseT: {:2.0%}".format(number_interface_used/number_interfaces))
        print("\nFinished with: ", self.DeviceName)
        print("\n")

        return
