import os
import re
import subprocess

VM = 'Wintest'
SNAPSHOT = 'Testshot'
USER = 'Padraig'
PASSWORD = 'password'
DESTINATION = os.path.normpath('/home/pdonnelly/Dropbox/PhD/code/vboxgrab/qux.txt')
FILE = os.path.normpath('C:\Users\Padraig\Desktop\qux.txt')

LIST = 'VBoxManage list runningvms'
RESTORE = 'VBoxManage snapshot %s restore %s' % (VM, SNAPSHOT)
STOP = 'VBoxManage controlvm %s poweroff' % VM
START = 'VBoxManage startvm %s --type headless' % VM
COPY = 'VBoxManage guestcontrol %s copyfrom --username %s --password %s '\
        '--target-directory %s %s' % (VM, USER, PASSWORD, DESTINATION, FILE)

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

    # Create the file we're going to be writing to.
    with open(DESTINATION, 'w+') as fh:
        fh.close()
    # And make sure we can write to it.
    os.chmod(DESTINATION, 0o666)

    subprocess.call(COPY.split(), shell=False)

    # Stop that mother.
    stop_vm()

