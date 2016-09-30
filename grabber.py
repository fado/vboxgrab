import os
import re
import subprocess

VM = 'Wintest'
SNAPSHOT = 'Testshot'
USER = 'Padraig'
PASSWORD = 'password'
DIRECTORY = os.path.normpath('/home/pdonnelly/Dropbox/PhD/code/qux.txt')
FILE = os.path.normpath('C:\Users\Padraig\Desktop\qux.txt')

LIST = 'VBoxManage list runningvms'
RESTORE = 'VBoxManage snapshot %s restore %s' % (VM, SNAPSHOT)
STOP = 'VBoxManage controlvm %s poweroff' % VM
START = 'VBoxManage startvm %s --type headless' % VM
COPY = 'VBoxManage guestcontrol %s copyfrom --username %s --password %s '\
        '--target-directory %s %s' % (VM, USER, PASSWORD, DIRECTORY, FILE)

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

if __name__ == '__main__':

    if is_running():
        print 'VM already running. Stopping it.'
        stop_vm()

    subprocess.call(RESTORE.split(), shell=False)

    with open(os.devnull, 'w') as devnull:
        startvm = subprocess.call(START.split(), stdout=devnull,
                stderr=devnull, shell=False)

    if is_running():
        print 'VM started.'
    else:
        print 'Failed to start the VM. Sorry.'

    with open(DIRECTORY, 'w+') as fh:
        fh.close()
    subprocess.call(COPY.split(), shell=False)

    stop_vm()

