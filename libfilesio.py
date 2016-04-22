# A library to work with files to read and write text files, common uses for NetworkTangents only.
#
# Authors: Sergio Valqui
# Created : rebuilt from 2013
# Modified : 2016/


def l_text_f(path_and_filename, show_progress= False):
    import pathlib
    status = 0  # 0 : Good file exist with data; 1: file empty; 2: file do not exists
    content_return = []
    if pathlib.Path.exists(path_and_filename):  # if the file exists
        file_obj = pathlib.Path.open(path_and_filename, 'r')
        content_lines = file_obj.readlines()
        number_lines = len(content_lines)
        file_obj.close()
        if number_lines <= 0:  # file is empty
            status = 1
            if show_progress:
                print(str(path_and_filename))
                print("File EMPTY")
        else:  # if has lines
            for line in content_lines:
                content_return.append(line.rstrip("\n"))  # strip returns
    else:
        if show_progress:
            print(str(path_and_filename))
            print("File DO NOT Exists")
            status = 2
    return status, content_return
