import os
import argparse
import paramiko
import sys
#from nlc_ctrl import enable_nlc, disable_nlc

USER_NAME = 'agora'
REMOTE_HOST = '10.82.0.242'
SSH_PORT = 25552
PWD = 'bestvoip'

#networksetting =[None, None, None, None, None, None, None, None]
networksetting =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def remote_execute_result(remote_ip, user, passwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_ip, SSH_PORT, user, passwd)
    print "{0} run command :".format(remote_ip), cmd
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().strip()
    print "Result:", result
    ssh.close()
    return result

def run_tc_remote(ip_list = None, ulbw = None, ullr = None, uldelay = None, dlbw = None, dllr = None, dldelay = None, uljitter = None, dljitter = None, clear = None, nlc = False):
    if ip_list == None:
        return False
    
    cmd = ''

    if clear=="1":
        if nlc:
            disable_nlc()
        else:
            cmd = '/home/agora/anaconda2/bin/python /home/agora/remote_tc_ctrl/setNetworkByIpEx.py --clear'
    else:
        if nlc:
            enable_nlc(dlbw = dlbw, dllr = dllr, dldelay = dldelay, ulbw = ulbw, ullr = ullr, uldelay = uldelay)
        else:
            #cmd = '/home/agora/anaconda2/bin/python /home/agora/remote_tc_ctrl/setNetworkByIpEx.py --iplist %s --ulbw %s --ullr %s --dlbw %s --dllr %s' % (ip_list, ulbw, ullr, dlbw, dllr)
            cmd = '/usr/bin/python /home/agora/media_quality_test/network_py3/tools/set_network_by_ip.py --ip_local %s --ulbw %s --ullr %s --uldelay %s --dlbw %s --dllr %s --dldelay %s --uljitter %s --dljitter %s' % (ip_list, ulbw, ullr, uldelay, dlbw, dllr, dldelay, uljitter, dljitter)
    
    if not nlc:
        return remote_execute_result(REMOTE_HOST, USER_NAME, PWD, cmd)

if __name__ == '__main__':
    #run_tc_remote('192.168.3.111', 1000, 0, 0, 0)
    if len(sys.argv) != 0:
        for index in range(0, len(sys.argv) - 1):
            networksetting[index] = sys.argv[index + 1]


    run_tc_remote(networksetting[0], networksetting[1], networksetting[2], networksetting[3],
                  networksetting[4], networksetting[5], networksetting[6], networksetting[7],
                  networksetting[8], networksetting[9], nlc = False)