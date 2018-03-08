import subprocess
import pigpio
import signal
import time
import json
import uinput

# load uinput kernel module
subprocess.call(['sudo', '-i', 'modprobe', 'uinput'])

try:
    # check if pigpio daemon running
    pid = subprocess.check_output(['pgrep', 'pigpiod']).encode("utf-8")
    print(pid)
except:
    # start if needed
    print('Starting pigpio daemon...')
    subprocess.call(['sudo', 'pigpiod'])
    time.sleep(1)

# create pigpio instance
gpio = pigpio.pi()

# load keymap configuration
try:
    with open('keymap.json') as fid:
        keymap = json.load(fid)
except:
    print('Oops something went wrong! Load default keymap configuration')
    keymap =   {'13':{'controller': 'UP',     'keyboard': 'W'},
                '19':{'controller': 'DOWN',   'keyboard': 'S'},
                 '6':{'controller': 'LEFT',   'keyboard': 'A'},
                '26':{'controller': 'RIGHT',  'keyboard': 'D'},
                '12':{'controller': 'A',      'keyboard': 'K'},
                '16':{'controller': 'B',      'keyboard': 'D'},
                '20':{'controller': 'X',      'keyboard': 'D'},
                '21':{'controller': 'Y',      'keyboard': 'D'},
                '23':{'controller': 'SELECT', 'keyboard': 'D'},
                '22':{'controller': 'START',  'keyboard': 'D'},
                '27':{'controller': 'L1',     'keyboard': 'D'},
                '17':{'controller': 'R1',     'keyboard': 'D'}}

# save keymap
with open('keymap.json', 'w') as fid:
    json.dump(keymap, fid, indent=4, sort_keys=True, ensure_ascii=False)

# parse keymap for faster indexing
keymap_str_index = keymap
keymap = {}
events = []
for key in keymap_str_index:
    int_key = int(key)
    keymap[int_key] = keymap_str_index[key]
    keymap[int_key]['keyboard'] = eval('uinput.KEY_' + keymap[int_key]['keyboard'])
    events.append(keymap[int_key]['keyboard'])
del(keymap_str_index)

# create uinput device
dev = uinput.Device(events)


# callback function
# 0: falling edge
# 1: rising edge
# 2: watchdog timeout
level_conversion = {0: 1, 1: 0}
def gpio_callback(pin, level, tick):
    dev.emit(keymap[pin]['keyboard'], level_conversion[level])
    # debug
    # print(str(pin) + ' level: ' + str(level) + ' @ ' + str(tick))


# setup gpio
glitch_filter_time = round(1/30*1000)  # 30 FPS
for pin in keymap:
    gpio.set_mode(pin, pigpio.INPUT)
    gpio.set_pull_up_down(pin, pigpio.PUD_UP)
    gpio.set_glitch_filter(pin, glitch_filter_time)
    gpio.callback(pin, pigpio.EITHER_EDGE, gpio_callback)

# main loop
try:
    print('Press Ctrl+C to exit')
    signal.pause()
except KeyboardInterrupt:
    # clean up
    gpio.stop()
    subprocess.call(['sudo', 'pkill', 'pigpiod'])

print('All done!')
