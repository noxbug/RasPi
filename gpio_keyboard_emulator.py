from evdev import UInput, ecodes as e
import subprocess
import pigpio
import signal
import time
import json
import os

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

# construct path to keymap file
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
keymap_path = os.path.join(script_dir, 'keymap.json')
print(keymap_path)

# load keymap configuration
try:
    with open(keymap_path, 'w') as fid:
        keymap = json.load(fid)
except:
    print('Oops something went wrong! Load default keymap configuration')
    keymap =   {'13':{'controller': 'UP',     'keyboard': 'U'},
                '19':{'controller': 'DOWN',   'keyboard': 'D'},
                 '6':{'controller': 'LEFT',   'keyboard': 'L'},
                '26':{'controller': 'RIGHT',  'keyboard': 'R'},
                '12':{'controller': 'A',      'keyboard': 'A'},
                '16':{'controller': 'B',      'keyboard': 'B'},
                '20':{'controller': 'X',      'keyboard': 'X'},
                '21':{'controller': 'Y',      'keyboard': 'Y'},
                '23':{'controller': 'SELECT', 'keyboard': 'SPACE'},
                '22':{'controller': 'START',  'keyboard': 'ENTER'},
                '27':{'controller': 'L1',     'keyboard': 'E'},
                '17':{'controller': 'R1',     'keyboard': 'I'}}

# save keymap
with open(keymap_path, 'w') as fid:
    json.dump(keymap, fid, indent=4, sort_keys=True, ensure_ascii=False)

# parse keymap for faster indexing
keymap_str_index = keymap
keymap = {}
# events = []
for key in keymap_str_index:
    int_key = int(key)
    keymap[int_key] = keymap_str_index[key]
    keymap[int_key]['keyboard'] = eval('e.KEY_' + keymap[int_key]['keyboard'])
    # events.append(keymap[int_key]['keyboard'])
del(keymap_str_index)

# create uinput device
ui = UInput()

# callback function
# 0: falling edge
# 1: rising edge
# 2: watchdog timeout
level_conversion = {0: 1, 1: 0}
def gpio_callback(pin, level, tick):
    ui.write(e.EV_KEY, keymap[pin]['keyboard'], level_conversion[level])
    ui.syn()
    # debug
    print(str(pin) + ' level: ' + str(level) + ' @ ' + str(tick))


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
    ui.close()

print('All done!')
