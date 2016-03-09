# A library to work, process the output fo Network Devices an return a more workable structure.
#
# Authors: Sergio Valqui
# Created : 2015/11/08
# Modified : 2016/


def cut_not_include(some_text, start_text, end_text, maximum_lines_per_section=10000):
    """ from some_text (output from Network device session), returns a List of List(strings), sections of some_text
    containing the lines between StartText to EndText, DOES NOT include StartText or EndText on the returning sections.
    Used when the output from the Network Device needs to be trimmed before is processed.
    to remove headers (sh vlan, sh mod, ...)
    """
    include = False
    matching_list_text = []
    list_content = []
    counter = 0
    for line in some_text:
        if not include:
            if line.find(start_text) >= 0:
                include = True
        else:
            if line.find(start_text) >= 0:
                if len(list_content) > 0:
                    matching_list_text.append(list_content)
                    list_content = []
                    counter = 0

            elif line.find(end_text) >= 0 or counter >= maximum_lines_per_section:
                include = False
                matching_list_text.append(list_content)
                list_content = []
                counter = 0
            else:
                list_content.append(line)
                counter += 1

    if len(list_content) > 0:
        matching_list_text.append(list_content)

    return matching_list_text


def cut_include_start_end(some_text, start_text, end_text, maximum_lines_per_section=10000):
    """ from some_text (output from Network device session), returns a List of List(strings), sections of some_text
    containing the lines between StartText to EndText, INCLUDING StartText and EndText on the returning sections.
    Used when the output from the Network Device needs to be trimmed before is processed.
    to extract sections (Interfaces)
    """
    include = False
    matching_list_text = []
    list_content = []
    counter = 0
    for line in some_text:
        if not include:
            if line.find(start_text) >= 0:
                include = True
                list_content.append(line)
                counter += 1
        else:
            if line.find(start_text) >= 0:
                matching_list_text.append(list_content)
                list_content = []
                counter = 0
                list_content.append(line)

            elif line.find(end_text) >= 0 or counter >= maximum_lines_per_section:
                include = False
                list_content.append(line)
                matching_list_text.append(list_content)
                list_content = []
                counter = 0
            else:
                list_content.append(line)
                counter += 1
    if len(list_content) > 0:
        matching_list_text.append(list_content)

    return matching_list_text


def cut_include_from_list(some_text, list_keys, maximum_lines_per_section=10000):
    """ from some_text (output from Network device session), returns a Dictionary, sections of some_text;
    each section starts with an item of the list 'list_keys', which becomes the index ; includes the matching item,
    and all following lines; section ends when the next item is found or when the end of the list is reached.

    :param some_text: output from a session
    :param list_keys: list of items that define the beginning of the sections we want to extract(cut)
    :param maximum_lines_per_section: if we want to limit the number of lines per section
    :return: matching_list: dictionary of sections
    """
    matching_list = {}
    matching_list_idx = ''
    list_content = []
    include = False
    counter = 0

    for line in some_text:
        if not include:
            if line in list_keys:
                include = True
                matching_list_idx = line
                list_content.append(line)
                counter += 1
        else:
            if line in list_keys:
                matching_list[matching_list_idx] = list_content
                list_content = []
                matching_list_idx = line
                list_content.append(line)
                counter = 1
            elif counter >= maximum_lines_per_section:
                include = False
                counter = 0
                list_content.append(line)
                matching_list[matching_list_idx] = list_content
                list_content = []
            else:
                list_content.append(line)
                counter += 1

    if len(list_content) > 0:
        matching_list[matching_list_idx] = list_content

    return matching_list


def show_vlan_to_dictionary(show_vlan_output=''):
    """ from a Show Vlan text returns a Dictionary, Indexed by Vlan Number as integer.
    Dictionary: [VlanNumber_int], List
      List:(VlanNumber_str, VlanName, Composite(Vlan1))
    :param show_vlan_output
    :return a dictionary of index int(vlan number)
    """
    show_vlan_dictionary = {}
    show_vlan_list = cut_not_include(show_vlan_output, 'VLAN Name', 'VLAN Type')
    for line in show_vlan_list[0]:
        if len(line) > 0:
            line_split = line.split()
            if line_split[0].isnumeric():
                show_vlan_dictionary[int(line_split[0])] = [line_split[0], line_split[1], "Vlan"+line_split[0]]
    return show_vlan_dictionary


def show_interface_to_list(show_interface = ''):
    """from 'show int' returns a List of list(strings)
    :param show_interface:
    List: ['sh int contents per interface','...']
    :return:
    """
    show_interface_list = cut_include_start_end(show_interface, "line protocol", "#")
    return show_interface_list


def show_interface_switchport_to_list(show_interface_switchport=''):
    """from show int switchport returns a list of list(strings)
    List: ['sh int switchport content per interface']
    :param show_interface_switchport:
    :return:
    """
    show_interface_switchport_list = cut_include_start_end(show_interface_switchport, "Name:", "#")
    return show_interface_switchport_list


def int_name_to_int_short_name(interface_name=''):
    """From interface name returns the short name of the interface
    Ethernet
    Port-channel
    Vlan
    Loopback
    Tunnel
    :param interface_name:
    :return:
    """
    interface_short_name = ''
    short_text = interface_name[0:2]
    if interface_name.find('Ethernet') >= 0:
        start_numbering = interface_name.find('Ethernet') + 8
        int_numbering = interface_name[start_numbering:]
        interface_short_name = short_text + int_numbering
    elif interface_name.find('Port-channel') >= 0:
        int_numbering = interface_name[12:]
        interface_short_name = short_text + int_numbering
    elif interface_name.find('Vlan') >= 0:
        int_numbering = interface_name[4:]
        interface_short_name = short_text + int_numbering
    elif interface_name.find('Loopback') >= 0:
        int_numbering = interface_name[8:]
        interface_short_name = short_text + int_numbering
    elif interface_name.find('Tunnel') >= 0:
        int_numbering = interface_name[6:]
        interface_short_name = short_text + int_numbering
    else:
        print('Interface, ', interface_name, ' not predefined on int_name_to_int_short_name')

    return interface_short_name


def line_from_text(content='', some_text=[]):
    """
    returns the first line containing 'content'
    :param content:
    :param some_text: list of strings
    :return: line containing text
    """
    matching_line = ''
    for line in some_text:
        if line.find(content) >= 0:
            matching_line = line
            break
    return matching_line


def format_str_space(list_tuples):
    """
    Format spacing and lenght of a string(text).
    Used to format text before print it
    :param list_tuples: a list of tuples ( text_to_format, 'l' or 'c' or 'r', text_width )
    l : left justified
    c: centered
    r : right justified
    :return: a single string
    """
    formatted_str = ''
    for tupleset in list_tuples:
        formatted_section = ''
        if tupleset[1] == 'l':
            formatted_section = tupleset[0].strip()[:tupleset[2]].ljust(tupleset[2])
        elif tupleset[1] == 'c':
            formatted_section = tupleset[0].center(tupleset[2])
        elif tupleset[1] == 'r':
            formatted_section = tupleset[0].strip()[:tupleset[2]].rjust(tupleset[2])

        formatted_str += formatted_section + ' '

    return formatted_str


def uptime_to_short(sh_ver_uptime_line):
    """
    uptime to short converts the uptime line form sh version to short format 1y2m3d
    :param sh_ver_uptime_line: line from show version containing the uptime
    :return: uptime short format
    """
    fs_year = ''
    fs_week = ''
    fs_day = ''
    fs_hour = ''
    fs_minu = ''
    up_time_short = ''

    dumbline = sh_ver_uptime_line.split()
    for (index, word) in enumerate(dumbline):
        if (word.find('ear') >= 0) and (index > 0):
            fs_year = dumbline[index - 1]
        if (word.find('eek') >= 0) and (index > 0):
            fs_week = dumbline[index - 1]
        if (word.find('ay') >= 0) and (index > 0):
            fs_day = dumbline[index - 1]
        if (word.find('our') >= 0) and (index > 0):
            fs_hour = dumbline[index - 1]
        if (word.find('inut') >= 0) and (index > 0):
            fs_minu = dumbline[index - 1]
    if fs_year != '':
        up_time_short = up_time_short + fs_year + 'y'
    if fs_week != '':
        up_time_short = up_time_short + fs_week + 'w'
    if fs_day != '':
        up_time_short = up_time_short + fs_day + 'd'
    if fs_hour != '':
        up_time_short = up_time_short + fs_hour + 'h'
    if fs_minu != '':
        up_time_short = up_time_short + fs_minu + 'm'

    return up_time_short
