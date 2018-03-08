import subprocess
import pigpio
import signal
import time
import json
import uinput

# load uinput kernel module
subprocess.call(['sudo', 'modprobe', 'uinput'])

# start pgpio daemon
try:
	pid = subprocess.
subprocess.call(['sudo', 'pigpiod'])

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

# callback functions
def gpio_callback(pin, level, tick):
    print(str(pin) + ' level: ' + str(level) + ' @ ' + str(tick))

# setup gpio + events
glitch_time = round(1/30*1000)  # 30 FPS
events = []
for key in keymap:
	# gpio
	pin = int(key)
	gpio.set_mode(pin, pigpio.INPUT)
	gpio.set_pull_up_down(pin, pigpio.PUD_UP)
	gpio.set_glitch_filter(pin, glitch_time)
	gpio.callback(pin, pigpio.EITHER_EDGE, gpio_callback)
	# events
	keymap[key]['keyboard'] = eval('uinput.KEY_' + keymap[key]['keyboard'])

print(keymap)



# main loop
try:
    print('Press CTRL+C to exit')
    signal.pause()
except KeyboardInterrupt:
    # clean up
    gpio.stop()
    subprocess.call(['sudo', 'pkill', 'pigpiod'])

print('All done!')
