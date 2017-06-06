# A library to work, process the output of Network Devices, and return a more workable structure.
#
# Authors: Sergio Valqui
# Created : 2015/11/08
# Modified : 2016/


def cut_not_include(some_text, start_text, end_text, maximum_lines_per_section=10000):
    """ from some_text (output from Network device session), returns a List of List(strings), sections of some_text
    containing the lines between StartText to EndText, DOES NOT include StartText or EndText on the returning sections.
    Used when the output from the Network Device needs to be trimmed before is processed.
    to remove headers (sh vlan, sh mod, ...)
    :param some_text usually the full command output
    :param start_text the text that defines the begging of a section
    :param end_text the text that defines the ending of a section
    :param maximum_lines_per_section if the end_text is not found yet how many lines we want to take in a section
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
    to extract sections (e.g. Interfaces)
    :param some_text usually the full command output
    :param start_text the text that defines the begging of a section
    :param end_text the text that defines the ending of a section
    :param maximum_lines_per_section if the end_text is not found yet how many lines we want to take in a section
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
    :return a dictionary of index int(vlan number);
    Dic[VlanNumber_int]: [[VlanNumber_str, VlanName, Composite(Vlan1)],...]
    """
    show_vlan_dictionary = {}
    show_vlan_list = cut_not_include(show_vlan_output, 'VLAN Name', 'VLAN Type')
    for line in show_vlan_list[0]:
        if len(line) > 0:
            line_split = line.split()
            if line_split[0].isnumeric():
                show_vlan_dictionary[int(line_split[0])] = [line_split[0], line_split[1], "Vlan"+line_split[0]]
    return show_vlan_dictionary


def show_mac_to_dictionary(show_mac_address=''):
    """ from show mac address returns a dictionary, Indexed by Interface(short name) as per output.
    Dictionary: [Int_name_short], List
      List: (mac_address, Vlan_number_text). (('0100.0ccc.cccc','345'),('0100.0ccc.cccc','345'),(,),...)
    :param show_mac_address:
    :return: a dictionary of index int_name_short
             show_mac_dictionary[vlan]: [[mac_add, vlan_num], [mac_add, vlan_num],... ]

    vlan   mac address     type    learn     age              ports
    ------+----------------+--------+-----+----------+--------------------------
    2123  0008.aaaa.aaaa   dynamic  Yes        170   Po7
    *  345  0100.eeee.ffff    static  Yes          -   Po1,Po3,Po7,Po8,Po9,Router

    Vlan    Mac Address       Type        Ports
    ----    -----------       --------    -----
     All    0100.0ccc.cccc    STATIC      CPU
     All    0100.0ccc.cccd    STATIC      CPU
     All    0100.0ccc.ccce    STATIC      CPU

    """
    show_mac_dictionary = {}
    for line in show_mac_address:
        if len(line) > 0:
            line_split = line.split()
            if len(line_split) > 3:
                if line_split[-1].find(",") < 0:  # doesn't find multiple ports entry
                    if line_split[0].isnumeric():
                        if line_split[-1] in show_mac_dictionary.keys():
                            if not [line_split[1], line_split[0]] in show_mac_dictionary[line_split[-1]]:
                                show_mac_dictionary[line_split[-1]].append([line_split[1], line_split[0]])
                        else:
                            show_mac_dictionary[line_split[-1]] = []
                            show_mac_dictionary[line_split[-1]].append([line_split[1], line_split[0]])

                    elif line_split[0] in ("R", "S", "D" "*") and line_split[1].isnumeric():
                        if line_split[-1] in show_mac_dictionary.keys():
                            if not [line_split[2], line_split[1]] in show_mac_dictionary[line_split[-1]]:
                                show_mac_dictionary[line_split[-1]].append([line_split[2], line_split[1]])
                        else:
                            show_mac_dictionary[line_split[-1]] = []
                            show_mac_dictionary[line_split[-1]].append([line_split[2], line_split[1]])

    return show_mac_dictionary


def show_interface_to_list(show_interface=''):
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


def show_vrf_to_dictionary(show_ip_vrf=''):
    """
    Nuts#sh ip vrf
    Name                             Default RD            Interfaces
    VPN-ONE                          110:5133               Vl1230
                                                            Vl1234
                                                            Tu0
                                                            Tu12
    VPN-TWO                         120:5133              Vl1910
                                                            Tu11
                                                            Tu23
    Nuts#

    :param show_ip_vrf:
    :return: a dictionary of index vrf: Dic[vrf]: [RD, [Interfaces_list], [ip_route]]
    inside a dictionary "distinguisher", and Interfaces
    """
    # Structure needs to be reviewed sv 2017/06
    vrf_name = ''
    vrf = {}
#    distinguisher = {}
    vrf_interface_list = []
    vrf_ip_route = []
    for line in show_ip_vrf:
        line_split = line.split()
        if len(line_split) > 1 and line_split[1].find(':') > 0:
            if len(line_split) == 2:  # Name and RD
                vrf_name = line_split[0].strip()
                vrf_rd = line_split[1]
                vrf_interface_list = []
            else:
                vrf_name = line_split[0].strip()
                vrf_rd = line_split[1]
                vrf_interface_list.append(line_split[2])
            vrf[vrf_name] = [vrf_rd, vrf_interface_list, vrf_ip_route]
        elif len(line_split) == 1:
            vrf[vrf_name][1].append(line_split[0])

    return vrf


def int_name_to_int_short_name(interface_name=''):
    """From interface name returns the short name of the interface
    Ethernet
    Port-channel
    Vlan
    Loopback
    Tunnel
    Group-Async
    mgmt
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
    elif interface_name.find('Group-Async') >= 0:
        int_numbering = interface_name[11:]
        interface_short_name = short_text + int_numbering
    elif interface_name.find('mgmt') >= 0:
        interface_short_name = interface_name
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


def show_ver_brief(show_version):
    brief = []
    for line in show_version:
        if line.find("IOS Software") >= 0:
            brief.append(line)
        elif line.find("System image file is") >= 0:
            brief.append(line)
        elif line.find("bytes of memory") >= 0:
            brief.append(line)
        elif line.find("bytes of physical memory") >= 0:
            brief.append(line)
        elif line.find("isco") >=0 and line.find("processor") >= 0:
            brief.append(line)
    return brief


def show_ver_model(show_version):
    model = ''
    for line in show_version:
        if line.find("isco") >= 0 and line.find("rocessor") >= 0:
            model = line.split()[1]
            break
    return model


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


def show_fs_to_space_free(sh_file_systems, debug=False):
    """
    from 'show file systems', returns a list of tuple
    :param sh_file_systems:
    :param debug:
    :return:
    """
    master_id = ''
    file_systems_free_space = ()
    other_fs = ''

    for line in sh_file_systems:
        if len(line) > 0:
            if line[0] == "*":
                master_line = line
                if debug == True:
                    print('master: ', master_line)
                line_split = master_line.split()
                master_fs = line_split[-1]
                master_fs_size = line_split[2]
                file_systems_free_space = ((master_fs, master_fs_size),)
                master_id = master_fs[:-2]

    for line in sh_file_systems:
        if len(line) > 0:
            if line[0] != "*" and line.find(master_id) >= 0:
                line_split = line.split()
                for string in line_split:
                    if string.find(master_id) >= 0:
                        other_fs = string
                other_fs_size = line_split[1]
                file_systems_free_space += ((other_fs, other_fs_size),)

    return file_systems_free_space





