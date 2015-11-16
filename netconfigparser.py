

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
            print('not including line: ', line)
            print()
        else:
            if line.find(start_text) >= 0:
                if len(list_content) > 0:
                    matching_list_text.append(list_content)
                    print('found start', line)
                    print('added list :',list_content)
                    print()
                    list_content = []
                    counter = 0

            elif line.find(end_text) >= 0 or counter >= maximum_lines_per_section:
                include = False
                matching_list_text.append(list_content)
                print('found last', line)
                print('added list :',list_content)
                print()
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
                print('found start: ', line)
                print('including line: ', line)
                print()
        else:
            if line.find(start_text) >= 0:
                matching_list_text.append(list_content)
                print('found start', line)
                print('added list :', list_content)
                print()
                list_content = []
                counter = 0

            elif line.find(end_text) >= 0 or counter >= maximum_lines_per_section:
                include = False
                list_content.append(line)
                matching_list_text.append(list_content)
                print('found last', line)
                print('added list :', list_content)
                print()
                list_content = []
                counter = 0
            else:
                list_content.append(line)
        counter += 1
    if len(list_content) > 0:
        matching_list_text.append(list_content)

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
    """from show int returns a List
    List: ['sh int contents per interface','...']
    """
    show_interface_list = cut_include_start_end(show_interface,"line protocol", "#")
    return show_interface_list

def show_interface_switchport_to_list(show_interface_switchport = ''):
    """from show int switchport retuns a list
    List: ['sh int switchport content per interface']
    :param show_interface_switchport:
    :return:
    """
    show_interface_switchport_list = cut_include_start_end(show_interface_switchport, "Name:", "#")
    return show_interface_switchport_list















