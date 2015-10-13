

def cut_not_include(list_text, start_text, end_text, maximum_lines_per_section=500):
    ''' from a ListText, returns a List of List, sections of ListText containing the lines between StartText to EndText,
    does not include StartText or EndText on the returning sections
    '''
    include = False
    new_list_text = []
    list_content = ''
    counter = 0
    for line in list_text:
        if not include:
            if line.find(start_text) >= 0:
                include = True
        else:
            if line.find(start_text) :
                if len(list_content) > 0:
                    new_list_text.append(list_content)
                    list_content = ''
                    counter = 0
            elif line.find(end_text) or counter == maximum_lines_per_section:
                include = False
                new_list_text.append(list_content)
                list_content = ''
                counter = 0

            list_content += list_content
            counter +=1
    return new_list_text




def show_vlan_to_dictionary(show_vlan_list=''):
    ''' from a Show Vlan List returns a Dictionary
    Dictionary: [Ordinal], List
      List:(VlanNumber, VlanName, Composite(Vlan1))
    '''
    show_vlan_dictionary = {}
    Ordinal = 0

    show_vlan_list = cut_not_include(show_vlan_dictionary,'','')

    for line in shvlanlist:
        if len(line) > 0:
            line_split = line.split()
            if line_split[0].find('/') >= 0:
                Ordinal += 1
                ShVlanDic[Ordinal] = []
    return show_vlan_dictionary