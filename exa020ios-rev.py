# An example series related to IOS upgrades
# .
#
# Authors: Sergio Valqui
# Created : 2016/04/
# Modified : 2016/
# file_status = 0  # 0 : Good file exist with data; 1: file empty; 2: file do not exists
# s2t54-advipservicesk9-mz.SPA.151-2.SY7.bin (118655448 bytes)
# c3750e-ipbasek9-mz.150-2.SE9.bin            (20430848 bytes)

import getpass
import netdef
import libnetconparser
import pathlib
import libfilesio
import sys
import netmiko

filename = "exa020ios-rev-devices.txt"  # file to be located in the parent directory away from dev
path_and_file = pathlib.Path.cwd().parent.joinpath(filename)
files_status, devices_list = libfilesio.l_text_f(path_and_file)

if files_status == 0:
    gs_UserName = getpass.getpass("Username: ")
    gs_password = getpass.getpass()
    gs_EnablePass = getpass.getpass("Enabled Password: ")

    for device_name in devices_list:
        print("\n\nConnecting to: ", device_name)
        connected = False
        try:
            switch1 = netdef.NetworkDevice(device_name, gs_UserName, gs_password, gs_EnablePass)
            connected = True
        except netmiko.ssh_exception.NetMikoTimeoutException:
            print("Time out, Could NOT connect to: ", device_name)
        except ValueError:
            print("Could NOT connect to: ", device_name, " Possible empty/unknown character in file")
        except:
            print("Error: ", sys.exc_info()[0])

        if connected:
            switch1.Device_Connection.enable()

            # Working with the IOS version, getting it and presenting a brief.
            print("getting sh ver...")
            switch1.show_version()

            for line in switch1.ShowVersionBrief:
                print(line)

            print(switch1.SystemUpTime)
            print("Device Model: ", switch1.ChassisModel)
            print("\ngetting show file systems....")
            switch1.show_file_system()
            File_System = libnetconparser.show_fs_to_space_free(switch1.Show_File_System)
            print("FileSystem            Free Space in Bytes")
            for item in File_System:
                line = libnetconparser.format_str_space([(item[0], 'l', 25), (item[1], 'r', 12)])
                print(line)

            switch1.disconnect()
