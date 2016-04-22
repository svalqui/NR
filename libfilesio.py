# A library to work with files to read and write text files, common uses for NetworkTangents only.
#
# Authors: Sergio Valqui
# Created : rebuilt from 2013
# Modified : 2016/


def ltxtf(filename, show_progress= False):
    import os
    status = 0  # 0 : Good file exist with data; 1: File empty; 2: file do not exists
    content_return = []
    if os.path.exists(filename):  # if the file exists
        file_obj = open(filename, 'r')
        content_lines = file_obj.readlines()
        number_lines = len(content_lines)
        file_obj.close()
        if number_lines <= 0:  # file is empty
            status = 1
            if show_progress:
                print(filename)
                print("File EMPTY")
        else:  # if has lines
            for line in content_lines:
                content_return.append(line.rstrip("\n"))  # strip returns
    else:
        if show_progress:
            print(filename)
            print("File DO NOT Exists")
            status = 2
    return status, content_return
