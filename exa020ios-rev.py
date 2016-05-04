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
#    WS-C3750X-24P, c3750e-ipbasek9-mz.150-2.SE9.bin, 20430848
#
# s2t54-advipservicesk9-mz.SPA.151-2.SY7.bin (118655448 bytes)


import getpass
import netdef
import libnetconparser
import os
import libfilesio
import sys
import netmiko

filename_devices = "exa020ios-rev-devices.txt"  # file to be located in the parent directory away from dev
path_and_file_devices = os.path.join(os.path.abspath(os.pardir), filename_devices)
file_status_devices, devices_list = libfilesio.l_text_f(path_and_file_devices, True)

filename_model_ios = "exa020ios-rev-model-to-ios.txt"
path_and_file_model_ios = os.path.join(os.path.abspath(os.pardir), filename_model_ios)
file_status_model_ios, model_ios_list = libfilesio.l_text_f(path_and_file_model_ios, True)

# 0 : Good file exist with data; 1: file empty; 2: file do not exists
if file_status_devices == 0 and file_status_model_ios == 0:
    gs_UserName = getpass.getpass("Username: ")
    gs_password = getpass.getpass()
    gs_EnablePass = getpass.getpass("Enabled Password: ")
    model_dic = {}

    for model_ios in model_ios_list:
        model_split = model_ios.split(",")
        model_dic[model_split[0]] = [model_split[0], model_split[1], model_split[2]]

    for device_name in devices_list:
        print("\n\nConnecting to: ", device_name)
        connected = False
        current_ios = ''
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
                if line.find("image file is") >= 0:  # Extracting the ios filename
                    current_ios = line.split(":")[1].strip('"')
                    if current_ios.find("/") >= 0:
                        current_ios = current_ios.split("/")[1]
            print("Current IOS File : ", current_ios)

            print(switch1.SystemUpTime)
            print("Device Model: ", switch1.ChassisModel)
            print("\ngetting show file systems....")
            switch1.show_file_system()
            File_System = libnetconparser.show_fs_to_space_free(switch1.Show_File_System)

            if switch1.ChassisModel in model_dic:
                ios_to_review = model_dic[switch1.ChassisModel]
                ios_to_match = ios_to_review[1].strip()
                ios_size_to_match = ios_to_review[2].strip()

                if current_ios == ios_to_match:
                    print("Switch : ", device_name, " Already running : ", ios_to_match)
                else:
                    print("FileSystem       Free Space in Bytes")
                    for item in File_System:  # item[0] file system name, item[1] size in bytes
                        comment = ''
                        if int(item[1]) < int(ios_size_to_match):  # if space in file sys is less than ios size
                            comment = "NO SPACE FOR: " + ios_to_match + " needs : " + ios_size_to_match + "  *****"
                        line = libnetconparser.format_str_space([(item[0], 'l', 15), (item[1], 'r', 15),
                                                                 (comment, 'r', 80)])
                        print(line)
            else:
                print(switch1.ChassisModel, " Not found on file exa020ios-rev-model-to-ios.txt")

            switch1.disconnect()
else:
    print("File or files not found on parent directory")
    print("exa020ios-rev-devices.txt")
    print("exa020ios-rev-model-to-ios.tx")
