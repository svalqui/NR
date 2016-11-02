# An example series related to IOS upgrades
# On this examples we will connect to multiple switches to check if there is space in the file system
#  for an IOS upgrade
#
# Authors: Sergio Valqui
# Created : 2016/04/
# Modified : 2016/
# file_status = 0  # 0 : Good file exist with data; 1: file empty; 2: file do not exists
#
# This script needs 2 files in the parent directory as follow:
# "exa020ios-rev-devices.txt" ; text file containing the devices names, one per line.
# "exa020ios-rev-model-to-ios.tx"; text file containing:switch model, ios name, ios size(in bytes); separate by comma,
#  which ios you wish to install on each model as below
#    WS-C3750X-24P, c3750e-ipbasek9-mz.150-2.SE9.bin, 20430848
#
# This script writes a log file in the parent directory
# "exa020ios-rev-log.txt"; text file containing most print statements.
#
#  Reference : s2t54-advipservicesk9-mz.SPA.151-2.SY7.bin (118655448 bytes)


import getpass
import os
import sys

import netmiko

from lib import filesio, netconparser
from networktangents import cisconetworkdevice

filename_devices = "exa020ios-rev-devices.txt"  # file to be located in the parent directory away from dev
path_and_file_devices = os.path.join(os.path.abspath(os.pardir), filename_devices)
file_status_devices, devices_list = filesio.l_text_f(path_and_file_devices, True)

filename_model_ios = "exa020ios-rev-model-to-ios.txt"
path_and_file_model_ios = os.path.join(os.path.abspath(os.pardir), filename_model_ios)
file_status_model_ios, model_ios_list = filesio.l_text_f(path_and_file_model_ios, True)

log_list = []

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
        line_log = "\n\nConnecting to: " + device_name
        print(line_log)
        log_list.append(line_log)
        connected = False
        current_ios = ''
        try:
            switch1 = cisconetworkdevice.CiscoNetworkDevice(device_name, gs_UserName, gs_password, gs_EnablePass)
            connected = True
        except netmiko.ssh_exception.NetMikoTimeoutException:
            line_log = "Time out, Could NOT connect to: " + device_name
            print(line_log)
            log_list.append(line_log)
        except ValueError:
            line_log = "Could NOT connect to: " + device_name + " Possible empty/unknown character in file"
            print(line_log)
            log_list.append(line_log)
        except:
            line_log = "Error: " + sys.exc_info()[0]
            print(line_log)
            log_list.append(line_log)

        if connected:
            switch1.Device_Connection.enable()

            # Working with the IOS version, getting it and presenting a brief.
            print("getting sh ver...")
            switch1.show_version()

            for line in switch1.ShowVersionBrief:
                print(line)
                log_list.append(line)
                if line.find("image file is") >= 0:  # Extracting the ios filename
                    current_ios = line.split(":")[1].strip('"')
                    if current_ios.find("/") >= 0:
                        current_ios = current_ios.split("/")[1]
            line_log = "Current IOS File : " + current_ios
            print(line_log)
            log_list.append(line_log)

            line_log = switch1.SystemUpTime
            print(line_log)
            log_list.append(line_log)

            line_log = "Device Model: " + switch1.ChassisModel
            print(line_log)
            log_list.append(line_log)

            print("\ngetting show file systems....")
            switch1.show_file_system()
            File_System = netconparser.show_fs_to_space_free(switch1.Show_File_System)

            if switch1.ChassisModel in model_dic:
                ios_to_review = model_dic[switch1.ChassisModel]
                ios_to_match = ios_to_review[1].strip()
                ios_size_to_match = ios_to_review[2].strip()

                if current_ios == ios_to_match:
                    line_log = "Switch : " + device_name + " Already running : " + ios_to_match
                    print(line_log)
                    log_list.append(line_log)

                else:
                    line_log = "FileSystem       Free Space in Bytes"
                    print(line_log)
                    log_list.append(line_log)

                    for item in File_System:  # item[0] file system name, item[1] size in bytes
                        comment = ''
                        if int(item[1]) < int(ios_size_to_match):  # if space in file sys is less than ios size
                            comment = "NO SPACE FOR: " + ios_to_match + " needs : " + ios_size_to_match + "  *****"
                        line = netconparser.format_str_space([(item[0], 'l', 15), (item[1], 'r', 15),
                                                              (comment, 'r', 80)])
                        print(line)
                        log_list.append(line)
            else:

                line_log = switch1.ChassisModel + " Not found on file exa020ios-rev-model-to-ios.txt"
                print(line_log)
                log_list.append(line_log)

            switch1.disconnect()

    filename_log = "exa020ios-rev-log.txt"
    path_and_file_log = os.path.join(os.path.abspath(os.pardir), filename_log)
    filesio.w_text_file(path_and_file_log, log_list)

else:
    print("File or files not found on parent directory")
    print("exa020ios-rev-devices.txt")
    print("exa020ios-rev-model-to-ios.tx")


