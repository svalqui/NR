# Reboot all interface where a WAP is in disassociated state.
#
#
# Authors: Sergio Valqui
# Created : 2016/09
# Modified : 2016/09

import getpass
import lib.restapi.ciscoprimeapi as cpriapi

user_name = getpass.getpass("Username: ")
password = getpass.getpass()

class_cisco_prime = cpriapi.CiscoPrimeApi(user_name, password)
list_content = class_cisco_prime.read_unreachable()