# Interface Source Class
# Authors: Sergio Valqui
# Created : 2016/08/31
# Modified : 2016/
# to contain all common properties and functions for all interfaces


class Interface(object):
    """Class container for all attributes and methods related to an Interface, they are part of NetworkDevice"""
    def __init__(self):
        self.InterfaceName = ''
        self.InterfaceShortName = ''
        self.InterfaceDescription = ''
        self.PacketsInput = ''
        self.PacketsOutput = ''
        self.InputErrors = ''
        self.OutputErrors = ''
        self.Type = ''
        self.ListMacAddress = []

    def load_interface_details(self):
        """
        fills in class details coming from 'sh int'
        and 'sh int switchport' both should be already filled
        :param:
        :return:
        """
        return


