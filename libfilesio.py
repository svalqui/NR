# A library to work with files to read and write text files, common uses for NetworkTangents only.
#
# Authors: Sergio Valqui
# Created : rebuilt from 2013
# Modified : 2016/


def l_text_f(path_and_filename, show_progress=False):
    import pathlib
    status = 0  # 0 : Good file exist with data; 1: file empty; 2: file do not exists
    content = []
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
                content.append(line.rstrip("\n"))  # strip returns
    else:
        if show_progress:
            print(str(path_and_filename))
            print("File DO NOT Exists")
            status = 2
    return status, content


def w_text_file(path_and_filename, content, overwrite=False, create_copy=False, debug=False):
    import pathlib
    if pathlib.Path.exists(path_and_filename):
        if overwrite:  # Write
            file_obj = open(path_and_filename, 'w')
        elif create_copy:  # Copy and Write
            import shutil
            import datetime
            date_time_now = datetime.datetime.now().strftime("-%Y%m%d-%H%M%S")
            new_filename = path_and_filename + date_time_now

        else:  # Append
            file_obj = open(path_and_filename, 'a')
    else:  # Write if path doesn't exists
        file_obj = open(path_and_filename, 'w')

    for line in content:
        if type(line).__name__ == "str":
            file_obj.write(line + '\n')
        else:
            file_obj.write(str(line) + '\n')
    file_obj.close()

    return
