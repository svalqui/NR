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
from lib import restapi

gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()

header_json = {"content-type": "application/json"}
header_xml = {"content-type": "text/xml"}
header_html = {"content-type": "text/html"}

print("============")

#url = "https://pi.unimelb.net.au/webacs/api/v2/data/ClientSessions.json?.full=true&userName=" # Check Working
#url = "https://pi.unimelb.net.au/webacs/api/v1/data/Alarms.json?.condition.value=AP_DISASSOCIATED&severity=MAJOR"
#url = "https://pi.unimelb.net.au/webacs/api/v1/data/Alarms.json?.full=true"
#url = "https://pi.unimelb.net.au/webacs/api/v2/data/AccessPointDetails/587698.json?.full=true" # Checked working
# Pagination = 99


class CiscoPrimeApi():
    def __init__(self):
        self.user_name = ""
        self.password = ""
        self.url = ""
        self.list_content = []
        self.page = ""
        self.page_decoded = ""

    def read_page(self, url, first_result=0, max_result=99, show=False):
        self.url = url + "&.maxResults=" + str(max_result) + "&.firstResult=" + str(first_result)
        self.page = requests.get(self.url, headers=header_json, verify=False,
                                 auth=HTTPBasicAuth(self.user_name, self.password))
        if show:
            print("Querying :  ", self.url)
            print(self.page.status_code)
        self.page_decoded = json.loads(page.text)
        return self.page_decoded

    def read_unreachable(self):
        self.url = "https://pi.unimelb.net.au/webacs/api/v2/data/AccessPointDetails.json?.full=true" \
                   "&reachabilityStatus=UNREACHABLE"
        self.list_content = []  # list of page_decoded
        reach_end = False
        page_counter = 0
        first_result = 0
        max_result = 99
        while not reach_end:
            current_page = self.read_page(url, first_result, max_result)
            self.list_content.append(current_page)
            page_counter = current_page['queryResponse']["@count"]
            if current_page['queryResponse']["@last"] < page_counter:
                first_result += 100
            else:
                reach_end = True
        return list_content
    #print(decoded['queryResponse']["@first"])

    def list_unreachable_neighbor(self):
        list_ap_neighbor = []
        list_ap_no_neighbor = []
        self.list_content = self.read_unreachable()
        for item in self.list_content:
            for entity in item['queryResponse']['entity']:
                #print(i['@url'])
                print(entity['accessPointDetailsDTO']['name'])
                if 'cdpNeighbors' in entity['accessPointDetailsDTO'] :
                    #print(type(i['accessPointDetailsDTO']['cdpNeighbors']))
                    for neighbor in entity['accessPointDetailsDTO']['cdpNeighbors'].keys():
                        #print(type(i['accessPointDetailsDTO']['cdpNeighbors'][j]))
                        for detail in entity['accessPointDetailsDTO']['cdpNeighbors'][neighbor]:
                            print(detail["neighborName"])
                            print(detail["neighborPort"])
                            print()
                            list_ap_neighbor.append([entity['accessPointDetailsDTO']['name'], detail["neighborName"],
                                                     detail["neighborPort"]])
                else:
                    print("No cdpNeighbors on this device\n")
                    list_ap_no_neighbor.append(entity['accessPointDetailsDTO']['name'])
        return list_ap_neighbor, list_ap_no_neighbor




