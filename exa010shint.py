# An example "show interfaces on steroids" to manipulate the output of "sh int status" and
# return something a little bit more useful.
#
# Authors: Sergio Valqui
# Created : 2015/12/
# Modified : 2016/08

import getpass
import netfun

gs_DeviceName = input('DeviceName: ')
gs_UserName = getpass.getpass("Username: ")
gs_password = getpass.getpass()
gs_EnablePass = getpass.getpass("Enabled Password: ")

netfun.show_int_steroids(gs_DeviceName, gs_UserName, gs_password, gs_EnablePass)

