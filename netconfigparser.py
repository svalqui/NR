

def cut_not_include(some_text, start_text, end_text, maximum_lines_per_section=10000):
    ''' from some_text (output from Network device session), returns a List of List, sections of some_text containing
    the lines between StartText to EndText, does not include StartText or EndText on the returning sections.
    When the output from the Network Device needs to be trimmed before is processed.
    to remove headers (sh vlan, sh mod, ...)
    '''
    include = False
    list_text = some_text.splitlines()
    matching_list_text = []
    list_content = []
    counter = 0
    for line in list_text:
        if not include:
            if line.find(start_text) >= 0:
                include = True
                print('found start: ', line)
            #print('not including line: ', line)
            #print()
        else:
            if line.find(start_text) >= 0:
                if len(list_content) > 0:
                    matching_list_text.append(list_content)
                    #print('found start', line)
                    #print('added list :',list_content)
                    #print()
                    list_content = []
                    counter = 0

            elif line.find(end_text) >= 0 or counter >= maximum_lines_per_section:
                include = False
                matching_list_text.append(list_content)
                #print('found last', line)
                #print('added list :',list_content)
                #print()
                list_content = []
                counter = 0
            else:
                list_content.append(line)
        counter += 1

    if len(list_content) > 0:
        matching_list_text.append(list_content)

    return matching_list_text

def cut_include_start_end(some_text, start_text, end_text, maximum_lines_per_section=10000):
    ''' from some_text (output from Network device session), returns a List of List, sections of some_text containing
    the lines between StartText to EndText, including StartText and EndText on the returning sections.
    When the output from the Network Device needs to be trimmed before is processed.
    to extract sections (Interfaces)
    '''
    include = False
    list_text = some_text.splitlines()
    matching_list_text = []
    list_content = []
    counter = 0
    for line in list_text:
        if not include:
            if line.find(start_text) >= 0:
                include = True
                list_content.append(line)
                #print('found start: ', line)
                #print('including line: ', line)
                #print()
        else:
            if line.find(start_text) >= 0:
                matching_list_text.append(list_content)
                #print('found start', line)
                #print('added list :', list_content)
                #print('-----1')

                list_content = []
                counter = 0
                list_content.append(line)

            elif line.find(end_text) >= 0 or counter >= maximum_lines_per_section:
                include = False
                list_content.append(line)
                matching_list_text.append(list_content)
                #print('found last on section', line)
                #print('added list :', list_content)
                #print('-------2')
                list_content = []
                counter = 0
            else:
                list_content.append(line)
        counter += 1
    if len(list_content) > 0:
        matching_list_text.append(list_content)
        #print("added LAST list:", list_content)

    return matching_list_text

def show_vlan_to_dictionary(show_vlan_output=''):
    ''' from a Show Vlan text returns a Dictionary, Index Vlan Number as text
    Dictionary: [VlanNumber], List
      List:(VlanNumber, VlanName, Composite(Vlan1))
    '''
    show_vlan_dictionary = {}
    show_vlan_list = cut_not_include(show_vlan_output,'VLAN Name','VLAN Type')
    for line in show_vlan_list[0]:
        if len(line) > 0:
            line_split = line.split()
            if line_split[0].isnumeric():
                show_vlan_dictionary[line_split[0]] = [line_split[0], line_split[1], "Vlan"+line_split[0]]
    return show_vlan_dictionary

def show_interface_to_list(show_interface = ''):
    """from show int returns a List of list
    List: ['sh int contents per interface','...']
    """
    show_interface_list = cut_include_start_end(show_interface,"line protocol", "#")
    return show_interface_list

def show_interface_switchport_to_list(show_interface_switchport = ''):
    """from show int switchport returns a list of list
    List: ['sh int switchport content per interface']
    :param show_interface_switchport:
    :return:
    """
    show_interface_switchport_list = cut_include_start_end(show_interface_switchport, "Name:", "#")
    return show_interface_switchport_list

def int_name_to_int_short_name(interface_name = ''):
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
    elif interface_name.find('Port-channel')>= 0:
        int_numbering = interface_name[12:]
        interface_short_name = short_text + int_numbering
    elif interface_name.find('Vlan')>= 0:
        int_numbering = interface_name[4:]
        interface_short_name = short_text + int_numbering
    elif interface_name.find('Loopback')>= 0:
        int_numbering = interface_name[8:]
        interface_short_name = short_text + int_numbering
    elif interface_name.find('Tunnel')>= 0:
        int_numbering = interface_name[6:]
        interface_short_name = short_text + int_numbering
    else:
        print('Interface, ', interface_name, ' not predefined on int_name_to_int_short_name')

    return interface_short_name

def line_from_text(content= '', some_text= []):
    '''
    returns the first line containing content
    :param line:
    :param some_text:
    :return: line containing text
    '''
    matching_line = ''
    for line in some_text:
        if line.find(content)>= 0
            matching_line = line
            break

    return matching_line



















