from subprocess import check_output, call
from time import sleep

def start_process(process):
    try:
        # find PID to check if process is already running
        pid = check_output(['pgrep', process]).decode('utf-8')
    except:
        # start process if not running
        sleep(1)
        call(process + ' &', shell=True)


start_process('leafpad')
