#
# http://www.macvendorlookup.com/api/v2/{MAC_Address}

import requests
import json
import lib.restapimaster
import time


class QueryMac(lib.restapimaster.RestApi):
    def __init__(self):
        super(QueryMac, self).__init__()
        self.urlbase = "http://www.macvendorlookup.com/api/v2/"
        self.url_queried = ""
        self.list_content = []
        self.page = ""
        self.page_decoded = ""
        self.current_page = ""
        self.mac_manufacturer = ""

    def read_page(self, mac="", debug=False):
        self.url_queried = self.urlbase + mac
        if debug:
            print("reading ...", self.url_queried)
        self.page = requests.get(self.url_queried, headers=self.header_json)
        time.sleep(0.1)
        if debug:
            print("Querying :  ", self.url_queried)
            print(self.page.status_code)
        self.page_decoded = json.loads(self.page.text)
        return self.page_decoded

    def mac_company(self, mac="", debug=False):
        self.mac_manufacturer = ""
        self.read_page(mac)
        if len(self.page_decoded) > 0 :
            if "country" in self.page_decoded[0]:
                self.mac_manufacturer = self.page_decoded[0]["country"]
            else:
                self.mac_manufacturer = "MAC Manufacturer not found on http://www.macvendorlookup.com"
        else:
            self.mac_manufacturer = "No response from http://www.macvendorlookup.com"
        return



# - L-Content : list here
# - L-Content : dict found on list resending
# country - D_Content : str Value : UNITED STATES
# company - D_Content : str Value : Dell Inc
# endDec - D_Content : str Value : 26403110125567
# endHex - D_Content : str Value : 180373FFFFFF
# addressL3 - D_Content : str Value : Round Rock Texas 78682
# startDec - D_Content : str Value : 26403093348352
# addressL2 - D_Content : str Value :
# addressL1 - D_Content : str Value : One Dell Way, MS:RR5-45
# startHex - D_Content : str Value : 180373000000
# type - D_Content : str Value : MA-L
