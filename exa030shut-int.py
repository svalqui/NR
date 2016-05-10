# An example of how to shutdown interfaces that have been idle for more than 4 months.
# On this example we will connect to multiple switches to check if the interfaces have been used in the
#  last 4 months, by checking the bytes input and output, and the counters date.
#
# Authors: Sergio Valqui
# Created : 2016/05/
# Modified : 2016/
# file_status = 0  # 0 : Good file exist with data; 1: file empty; 2: file do not exists
#
# This script needs 1 file in the parent directory as follow:
# "exa030shut-int-devices.txt" ; text file containing the devices names, one per line.
#
# This script writes a log file in the parent directory
# "exa030shut-int-log.txt"; text file containing most print statements.
#

import getpass
import netdef
import libnetconparser
import os
import libfilesio
import sys
import netmiko

filename_devices = "exa030shut-int-devices.txt"  # file to be located in the parent directory away from dev
path_and_file_devices = os.path.join(os.path.abspath(os.pardir), filename_devices)
file_status_devices, devices_list = libfilesio.l_text_f(path_and_file_devices, True)

log_list = []

# 0 : Good file exist with data; 1: file empty; 2: file do not exists
if file_status_devices == 0:
    gs_UserName = getpass.getpass("Username: ")
    gs_password = getpass.getpass()
    gs_EnablePass = getpass.getpass("Enabled Password: ")
    model_dic = {}

    for device_name in devices_list:
        line_log = "\n\nConnecting to: " + device_name
        print(line_log)
        log_list.append(line_log)
        connected = False
        current_ios = ''
        try:
            switch1 = netdef.NetworkDevice(device_name, gs_UserName, gs_password, gs_EnablePass)
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
            File_System = libnetconparser.show_fs_to_space_free(switch1.Show_File_System)


        switch1.disconnect()

    filename_log = "exa030shut-int-log.txt"
    path_and_file_log = os.path.join(os.path.abspath(os.pardir), filename_log)
    libfilesio.w_text_file(path_and_file_log, log_list)

else:
    print("File or files not found on parent directory")
    print("exa030shut-int-devices.txt")


