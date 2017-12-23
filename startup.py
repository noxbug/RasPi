from subprocess import check_output, call
from time import sleep


def start_process(process):
    try:
        # find PID to check if process is already running
        pid = check_output(['pgrep', process]).decode('utf-8')
    except:
        sleep(1)
        # start process if not running
        call(process + ' &', shell=True)

#start_process('transmission-gtk')
#start_process('kodi')

class StartupObj:
    def __init__(self, bash_file='/home/pi/PycharmProjects/raspi/startup.sh', log_file='/home/pi/Desktop/startup.log'):
        self.bash_file = bash_file
        self.log_file = log_file
        self.command_list=[]
    def run(self):
        # write the bash script
        f = open(self.bash_file, 'w')
        f.write('#!/bin/bash \n\n')
        for command in self.command_list:
            f.write(command + ' & echo $! >> ' + self.log_file + '\n')
        f.close()
        # execute the script
        call('sudo -u pi ' + self.bash_file, shell=True)


startupObj = StartupObj()
startupObj.command_list.append('transmission-gtk')
startupObj.command_list.append('kodi')
startupObj.run()
