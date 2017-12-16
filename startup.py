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

start_process('transmission-gtk')
start_process('kodi')
