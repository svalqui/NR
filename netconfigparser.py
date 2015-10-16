

def cut_not_include(some_text, start_text, end_text, maximum_lines_per_section=1000):
    ''' from some_text (output from Network device session), returns a List of List, sections of some_text containing
    the lines between StartText to EndText, does not include StartText or EndText on the returning sections.
    When the output from the Network Device needs to be trimmed before is processed.
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

            elif line.find(end_text) >= 0 or counter <= maximum_lines_per_section:
                include = False
                matching_list_text.append(list_content)
                print('found last', line)
                print('added list :',list_content)
                print()
                list_content = []
                counter = 0

        list_content.append(line)
        counter += 1

    return matching_list_text

def show_vlan_to_dictionary(show_vlan_output=''):
    ''' from a Show Vlan text returns a Dictionary
    Dictionary: [VlanNumber], List
      List:(VlanNumber, VlanName, Composite(Vlan1))
    '''
    show_vlan_dictionary = {}
    print(len(show_vlan_output))

    show_vlan_list = cut_not_include(show_vlan_output,'VLAN Name','VLAN Type')
    print(len(show_vlan_list))
    print(show_vlan_list)
    for line in show_vlan_list[0]:
        if len(line) > 0:
            print('line: ',line)
            line_split = line.split()
            if line_split[0].isnumeric():
                print(line_split[0])
                show_vlan_dictionary[line_split[0]] = [line_split[0], line_split[1], "Vlan"+line_split[0]]
    return show_vlan_dictionary











