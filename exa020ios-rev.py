# An example series related to IOS upgrades
# On this example we will connect to multiple switches to check there is space in the file system
#  for an IOS upgrade
#
# Authors: Sergio Valqui
# Created : 2016/04/
# Modified : 2016/
# file_status = 0  # 0 : Good file exist with data; 1: file empty; 2: file do not exists
# this script need 2 files in the parent directory as follow:
# "exa020ios-rev-devices.txt" ; text file containing the devices names, one per line.
# "exa020ios-rev-model-to-ios.tx"; text file containing:switch model, ios name, ios size(in bytes); separate by comma,
#  which ios you wish to install on each model as below
# WS-C3750X-24P, c3750e-ipbasek9-mz.150-2.SE9.bin, 20430848
# WS-C3750G-48PS, c3750e-ipbasek9-mz.150-2.SE9.bin, 20430848
#
# s2t54-advipservicesk9-mz.SPA.151-2.SY7.bin (118655448 bytes)


import getpass
import netdef
import libnetconparser
import pathlib
import libfilesio
import sys
import netmiko

filename_devices = "exa020ios-rev-devices.txt"  # file to be located in the parent directory away from dev
current_directory = pathlib.Path.cwd()
path_and_file_devices = current_directory.parent.joinpath(filename_devices)
file_status_devices, devices_list = libfilesio.l_text_f(path_and_file_devices)

filename_model_ios = "exa020ios-rev-model-to-ios.tx"
path_and_file_model_ios = current_directory.parent.joinpath(filename_model_ios)
file_status_model_ios, model_ios_list = libfilesio.l_text_f(path_and_file_model_ios)

if file_status_devices == 0 and file_status_model_ios == 0:
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
else:
    print("File or files not found on parent directory")
    print("exa020ios-rev-devices.txt")
    print("exa020ios-rev-model-to-ios.tx")
