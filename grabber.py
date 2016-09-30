import os
import re
import subprocess
import xmlrpclib
from socket import error as socket_error
from socket import timeout
from time import sleep

VM = 'Wintest'
SNAPSHOT = 'Testshot'
USER = 'Padraig'
PASSWORD = 'password'
DESTINATION = os.path.normpath('/home/pdonnelly/Dropbox/PhD/code/vboxgrab')
FILE = os.path.normpath('C:\Users\Padraig\Desktop\# DECRYPT MY FILES #.txt')
CERBER = os.path.normpath('C:\current\cerber.exe')

LIST = 'VBoxManage list runningvms'
RESTORE = 'VBoxManage snapshot %s restore %s' % (VM, SNAPSHOT)
STOP = 'VBoxManage controlvm %s poweroff' % VM
START = 'VBoxManage startvm %s --type headless' % VM
COPY = 'VBoxManage guestcontrol %s copyfrom '\
        '%s --target-directory %s '\
        '--username %s --password %s --verbose' % (VM, FILE, DESTINATION, USER, PASSWORD)
IP = 'VBoxManage guestproperty get %s /VirtualBox/GuestInfo/Net/0/V4/IP' % VM
RUN = 'VBoxManage %s run --exe %s' % (VM, CERBER)

def is_running():
    runningvms = subprocess.Popen(LIST.split(), stdout=subprocess.PIPE).communicate()[0]
    for vm in runningvms.split(os.linesep):
        if re.search(VM, vm):
            return True
        return False

def stop_vm():
    subprocess.call(STOP.split(), shell=False)
    while is_running():
        sleep(1)

def get_ip():
    guestproperties = subprocess.Popen(IP.split(), stdout=subprocess.PIPE)
    for guestproperty in guestproperties.stdout:
        ip = guestproperty.split()[-1]
        print "I got %s as the IP address of the VM." % ip
        return ip

def get_server():
    return xmlrpclib.ServerProxy('http://%s:9000' % get_ip())

if __name__ == '__main__':

    # Get rid of the last file if it exists.
    try:
        os.remove(DESTINATION)
    except OSError:
        pass

    # Check we're not trying to start a VM that's already running.
    if is_running():
        print 'VM already running. Stopping it.'
        stop_vm()

    # Restore the snapshot.
    subprocess.call(RESTORE.split(), shell=False)

    # Start the VM.
    with open(os.devnull, 'w') as devnull:
        startvm = subprocess.call(START.split(), stdout=devnull,
                stderr=devnull, shell=False)

    # Check it's running.
    if is_running():
        print 'VM started.'
    else:
        print 'Failed to start the VM. Sorry.'

    print "Infecting the VM with Cerber."
    subprocess.call(RUN.split(), shell=False)
    print "Waiting 120 seconds for encryption to complete."
    sleep(120)

    server = get_server()

    try:
        print server.get_url()
    except socket_error as error:
        print "Connection timed out."

    # Stop that mother.
    stop_vm()

