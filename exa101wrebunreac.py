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

list_ap_cdp = []
list_ap_no_cdp = []

print("sending query")
class_cisco_prime = cpriapi.CiscoPrimeApi(user_name, password)
holder = class_cisco_prime.read_unreachable()
print(holder)

list_ap_cdp, list_ap_no_cdp = class_cisco_prime.list_unreachable_neighbors()
for item in list_ap_cdp:
    print(item)
print("\n\n#####\n\n")
for item in list_ap_no_cdp:
    print(item)