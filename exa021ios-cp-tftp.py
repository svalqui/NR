# On this examples we will connect to multiple switches to check if there is space in the file system
#  for an IOS upgrade
#
# Authors: Sergio Valqui
# Created : 2016/11
# Modified : 2016/
# file_status = 0  # 0 : Good file exist with data; 1: file empty; 2: file do not exists
#
# This script needs 2 files in the parent directory as follow:
# "exa021ios-cp-tftp-devices.txt" ; text file containing the devices names, one per line.
# "exa021ios-cp-tftp-ios.txt"; text file containing:device model, ios name, and size of file (.bin)
# to be copied from the tftp server to the device, as below
#    WS-C3750X-24P, c3750e-ipbasek9-mz.150-2.SE9.bin, 20430848
#
# This script writes a log file in the parent directory
# "exa021ios-cp-log.txt"; text file containing most print statements.
#

import getpass
import os
import sys

from lib import filesio, netconparser
from networktangents import cisconet
from datetime import datetime

filename_devices = "exa021ios-cp-tftp-devices.txt"  # file to be located in the parent directory away from dev
path_and_file_devices = os.path.join(os.path.abspath(os.pardir), filename_devices)
file_status_devices, devices_list = filesio.l_text_f(path_and_file_devices, True)

filename_model_ios = "exa021ios-cp-tftp-ios.txt" # file to be located in the parent directory away from dev
path_and_file_model_ios = os.path.join(os.path.abspath(os.pardir), filename_model_ios)
file_status_model_ios, model_ios_list = filesio.l_text_f(path_and_file_model_ios, True)

log_list = []

# 0 : Good file exist with data; 1: file empty; 2: file do not exists
if file_status_devices == 0 and file_status_model_ios == 0:
    UserName = getpass.getpass("Username: ")
    password = getpass.getpass()
    EnablePass = getpass.getpass("Enabled Password: ")
    tftp_ip = input("TFTP IP address: ")
    model_dic = {}

    for model_ios in model_ios_list:  # creating dictionary by model
        model_split = model_ios.split(",")
        model_dic[model_split[0]] = [model_split[0], model_split[1], model_split[2]]

    for device_name in devices_list:
        line_log = "\n\nConnecting to: " + device_name
        print(line_log)
        log_list.append(line_log)
        connected = False
        current_ios = ''
        try:
            host = cisconet.Device(device_name, UserName, password, EnablePass)
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
            host.Device_Connection.enable()

            # Working with the IOS version, getting it and presenting a brief.
            print("getting sh ver...")
            host.show_version()

            for line in host.ShowVersionBrief:
                print(line)
                log_list.append(line)
                if line.find("image file is") >= 0:  # Extracting the ios filename
                    current_ios = line.split(":")[1].strip('"')
                    if current_ios.find("/") >= 0:
                        current_ios = current_ios.split("/")[1]
            line_log = "Current IOS File : " + current_ios
            print(line_log)
            log_list.append(line_log)

            line_log = host.SystemUpTime
            print(line_log)
            log_list.append(line_log)

            line_log = "Device Model: " + host.ChassisModel
            print(line_log)
            log_list.append(line_log)

            print("\ngetting show file systems....")
            host.show_file_system()
            FS_list = netconparser.show_fs_to_space_free(host.Show_File_System)

            if host.ChassisModel in model_dic:
                ios_to_copy = model_dic[host.ChassisModel]
                ios_to_match = ios_to_copy[1].strip()
                ios_size_to_match = ios_to_copy[2].strip()

                if current_ios == ios_to_match:  # if the ios already on device and running
                    line_log = "Switch : " + device_name + " Already running : " + ios_to_match
                    print(line_log)
                    log_list.append(line_log)

                else:  # Current ios do not match Proposed ios
                    line_log = "FileSystem       Free Space in Bytes"
                    print(line_log)
                    log_list.append(line_log)

                    for file_system in FS_list:  # item[0] file system name, item[1] size in bytes
                        comment = ''
                        if int(file_system[1]) < int(ios_size_to_match):  # if space in file sys is less than ios size
                            comment = "NO SPACE FOR: " + ios_to_match + " needs : " + ios_size_to_match + "  *****"
                            line = netconparser.format_str_space([(file_system[0], 'l', 15), (file_system[1], 'r', 15),
                                                                  (comment, 'r', 80)])
                            print(line)
                            log_list.append(line)
                        else:
                            comment = "Space OK, Proceeding with tftp copy"
                            line = netconparser.format_str_space([(file_system[0], 'l', 15), (file_system[1], 'r', 15),
                                                                  (comment, 'r', 80)])
                            print(line)
                            log_list.append(line)
                            copy_text = "copy tftp://" + tftp_ip + "/" + ios_to_match + " " + file_system[0]
                            print(copy_text)
                            host.send_command(copy_text)
                            print("Copied, ", ios_to_copy, " to ", file_system, " on ", device_name)

            else:  # Devices Chassis Model not listed in the file
                line_log = host.ChassisModel + " Not found on file exa021ios-cp-tftp-ios.txt"
                print(line_log)
                log_list.append(line_log)

            host.disconnect()

    filename_log = "exa021ios-rev-log-" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".txt"
    path_and_file_log = os.path.join(os.path.abspath(os.pardir), filename_log)
    filesio.w_text_file(path_and_file_log, log_list)

else:
    print("File or files not found on parent directory")
    print("exa021ios-cp-tftp-devices.txt")
    print("exa021ios-cp-tftp-ios.tx")


