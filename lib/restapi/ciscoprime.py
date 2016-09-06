# "https://pi31.its.unimelb.edu.au/webacs/api/v2/data/ClientSessions.json?.full=true&userName=tommyblue",
# "https://pi31.its.unimelb.edu.au/webacs/api/v1/data/RadioDetails?.full=true&operStatus=\"DOWN\"&slotId=\"0\"",
# "https://pi31.its.unimelb.edu.au/webacs/api/v1/data/RadioDetails?.full=true&operStatus=\"DOWN\"",
# "https://pi31.its.unimelb.edu.au/webacs/api/v1/data/RadioDetails?.full=true&operStatus=\"DOWN\"&slotId=\"0\"&apName=contains(\"EXT\")"
# "https://pi31.its.unimelb.edu.au/webacs/api/v2/data/ClientSessions/59036754\"
# "https://pi31.its.unimelb.edu.au/webacs/api/v2/data\"
#  reachabilityStatus - D_Content : str Value : Reachable

import getpass
import requests
import json
from requests.auth import HTTPBasicAuth

gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()

header_json = {"content-type": "application/json"}
header_xml = {"content-type": "text/xml"}
header_html = {"content-type": "text/html"}

print("============")
url = "https://pi.unimelb.net.au/webacs/api/v2/data/AccessPointDetails.json?.full=true&reachabilityStatus=UNREACHABLE" # check working
#url = "https://pi.unimelb.net.au/webacs/api/v2/data/ClientSessions.json?.full=true&userName=" # Check Working
#url = "https://pi.unimelb.net.au/webacs/api/v1/data/Alarms.json?.condition.value=AP_DISASSOCIATED&severity=MAJOR"
#url = "https://pi.unimelb.net.au/webacs/api/v1/data/Alarms.json?.full=true"
#url = "https://pi.unimelb.net.au/webacs/api/v2/data/AccessPointDetails/587698.json?.full=true" # Checked working

r = requests.get(url, headers=header_json, verify=False, auth=HTTPBasicAuth(gs_UserName, gs_password))
print("Querying :  ", url)
print(r.status_code)
##print ("============")
##print(r.text)
print("#########################")
decoded = json.loads(r.text)
print("decoded TYPE   ", type(decoded))


def navigate(json_loads, indent=""):
    if isinstance(json_loads, dict):
        for index in json_loads.keys():
            if isinstance(json_loads[index], dict):
                print(indent, index, "- D_Content : dict found on dict resending")
                indent += "  "
                navigate(json_loads[index], indent)
            elif isinstance(json_loads[index], list):
                print(indent, index, "- D_Content : list found on dict resending, len :", len(json_loads[index]))
                indent += "  "
                navigate(json_loads[index], indent)
            elif isinstance(json_loads[index], str):
                print(indent, index, "- D_Content : str Value :", json_loads[index])
            elif isinstance(json_loads[index], int):
                print(indent, index, "- D_Content : int Value :", json_loads[index])
            elif isinstance(json_loads[index], float):
                print(indent, index, "- D_Content : float Value :", json_loads[index])
            elif isinstance(json_loads[index], True):
                print(indent, index, "- D_Content : True Value :", json_loads[index])
            elif isinstance(json_loads[index], False):
                print(indent, index, "- D_Content : False Value :", json_loads[index])
            elif isinstance(json_loads[index], None):
                print(indent, index, "- D_Content : None Value :", json_loads[index])
            else:
                print(indent, index, "- D_Content : Obj not pre defined")

    elif isinstance(json_loads, list):
        print(indent, "- L-Content : list here")
        for element in json_loads:
            if isinstance(element, dict):
                print(indent, "- L-Content : dict found on list resending")
                navigate(element, indent)
            elif isinstance(element, list):
                print(indent, "- L-Content : list found on list resending, len :", len(element))
                navigate(element, indent)
            elif isinstance(element, str):
                print(indent, "- L-Content : str Value :", element)
            elif isinstance(element, int):
                print(indent, "- L-Content : int Value :", element)
            elif isinstance(element, float):
                print(indent, "- L-Content : float Value :", element)
            elif isinstance(element, True):
                print(indent, "- L-Content : True Value :", element)
            elif isinstance(element, False):
                print(indent, "- L-Content : False Value :", element)
            elif isinstance(element, None):
                print(indent, "- L-Content : None Value :", element)
            else:
                print(indent, "- L-Content : Obj not pre defined")

    elif isinstance(json_loads, str):
        print(indent, "- Content : str Value :", json_loads)
    elif isinstance(json_loads, int):
        print(indent, "- Content : int Value :", json_loads)
    elif isinstance(json_loads, float):
        print(indent, "- Content : float Value :", json_loads)
    elif isinstance(json_loads, True):
        print(indent, "- Content : True Value :", json_loads)
    elif isinstance(json_loads, False):
        print(indent, "- Content : False Value :", json_loads)
    elif isinstance(json_loads, None):
        print(indent, "- Content : None Value :", json_loads)
    else:
        print(indent, "Obj not pre defined")

    return

#navigate(decoded)
print("\n\n\n ########## \n\n\n")

print(decoded['queryResponse']["@first"])
print(decoded['queryResponse']["@last"])
print(decoded['queryResponse']["@count"])

for i in decoded['queryResponse']['entity']:
    print(i['@url'])
    print(i['accessPointDetailsDTO']['name'])
    if 'cdpNeighbors' in i['accessPointDetailsDTO'] :
        #print(type(i['accessPointDetailsDTO']['cdpNeighbors']))
        for j in i['accessPointDetailsDTO']['cdpNeighbors'].keys():
            #print(type(i['accessPointDetailsDTO']['cdpNeighbors'][j]))
            for l in i['accessPointDetailsDTO']['cdpNeighbors'][j]:
                print(l["neighborName"])
                print(l["neighborPort"])
                print()
    else:
        print("No cdpNeighbors on this device\n")
