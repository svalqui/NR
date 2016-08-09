# libnetscrapr library for interactions with REST api systems
#  Cisco Prime, Statseeker, Infoblox
# Author: Sergio Valqui
# Created : 2015/08/09

from bs4 import BeautifulSoup
import getpass
import requests
from requests.auth import HTTPBasicAuth

UserName = getpass.getpass("Username: ")
password = getpass.getpass()
url = input()

page = requests.get(url, verify=False, auth=HTTPBasicAuth(gs_UserName, gs_password))
print (page.status_code)
print ("============")
print(page.text)