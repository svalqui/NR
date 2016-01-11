# libnetservices library for functions related to Network services
# Such ssh, Sockets etc
# Author: Sergio Valqui
# Created : 2015/08/13


def ssh_pse_exp(obj_ssh_ses, obj_ssh_ses_cha, fs_command, fs_prompt, fb_print):
    '''
    ssh pseudo expect; receives data from the session channel till founds prompt or empty
    returns fl_return, list of text (response from device); fs_last_prompt
    ---
    obj_ssh_ses: Object session needed to maintain the link with the channel
    obj_ssh_ses_cha: the chanel with device to send/rcv commands/outputs
    fs_command: text to send to the device
    fs_prompt: prompt expected to indicate end of waiting/receiving
    fb_print: would you like it printed on the screen?
    '''
    fs_command += '\n'
    obj_ssh_ses_cha.send(fs_command)
    fs_buffer = b""

    while not bytes(fs_prompt,'ascii') in fs_buffer:
        # Flush the receive buffer
        fs_buffer += obj_ssh_ses_cha.recv(1024)

    fl_return = fs_buffer.decode().split('\n')
    fs_last_prompt = fl_return[-1]

    if fb_print:
        for line in fl_return:
            print(line)

    return fl_return, fs_last_prompt

def ssh_ses_con(fs_devnam= '', fs_user='', fs_pass= '', fs_enapass='', fb_ena = False):
    '''
    ssh session connect, opens a ssh session to a SSH Server device
    returns the ssh Object, Status of the connection, and prompt
    ---
    fs_devnam: device/host name
    fs_user: username
    fs_pass: password
    fs_enapass: enable password
    fb_enable: go to enable mode or not
    ---
    Returns : obj_ssh_ses (session)), obj_ses_cha (channel), fn_status
    fn_Status: 0 = session failed,
    1 = Username no requested,
    2 = Username/password Failed,
    3 = Enabled Mode Failed,
    5 = Succeed
    '''
    import paramiko as P
    import sys

    fn_status = 0

    print('\nConnecting to: ', fs_devnam)

    P.common.logging.basicConfig(level=P.common.DEBUG)
    #P.transport.set_keepalive(1)
    try:
        obj_ssh_ses = P.SSHClient()
        obj_ssh_ses.set_missing_host_key_policy(P.AutoAddPolicy())
        obj_ssh_ses.connect(fs_devnam, username = fs_user, password = fs_pass)
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise
    else:
        print('Connected to: ', fs_devnam)
        fn_status = 5
        obj_ssh_ses_cha = obj_ssh_ses.invoke_shell()
        print('Shell enabled')

        ssh_pse_exp(obj_ssh_ses, obj_ssh_ses_cha,'terminal length 0', '>', True)
        ssh_pse_exp(obj_ssh_ses, obj_ssh_ses_cha,'sh ver', '>', True)
        print('setting session')
        if fb_ena:
            ssh_pse_exp(obj_ssh_ses, obj_ssh_ses_cha,'enable', 'Password:', True)
            ssh_pse_exp(obj_ssh_ses, obj_ssh_ses_cha,fs_enapass, '#', True)
            print('Logged in enabled mode\n')
            print('exit netser lib')

    return (obj_ssh_ses, obj_ssh_ses_cha, fn_status)

def ssh_ses_clo(obj_ssh_ses, obj_ses_cha):
    '''
    ssh sesssion close
    :param obj_ssh_ses: ssh session to be close
    :param obj_ses_cha: ssh session channel to be close
    :return: nothing
    '''
    obj_ses_cha.close()
    obj_ssh_ses.close()
    return