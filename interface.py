# Interface Source Class

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

    def load_interface_details(self):
        """
        fills in class details coming from 'sh int'
        and 'sh int switchport' both should be already filled
        :param:
        :return:
        """
        return


