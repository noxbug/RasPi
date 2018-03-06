import RPIO as GPIO
import signal
import time
import json


# load keymap configuration
try:
    with open('keymap.json') as fid:
        keymap = json.load(fid)
except:
    print('Oops something went wrong! Load default keymap configuration')
    keymap =    {6:{'controller': 'UP',     'keyboard': 'KEY_W'},
                13:{'controller': 'DOWN',   'keyboard': 'KEY_S'},
                19:{'controller': 'LEFT',   'keybaord': 'KEY_A'},
                26:{'controller': 'RIGHT',  'keybaord': 'KEY_D'},
                12:{'controller': 'A',      'keybaord': 'KEY_D'},
                16:{'controller': 'B',      'keybaord': 'KEY_D'},
                20:{'controller': 'X',      'keybaord': 'KEY_D'},
                21:{'controller': 'Y',      'keybaord': 'KEY_D'},
                23:{'controller': 'SELECT', 'keybaord': 'KEY_D'},
                22:{'controller': 'START',  'keybaord': 'KEY_D'},
                27:{'controller': 'L1',     'keybaord': 'KEY_D'},
                17:{'controller': 'R1',     'keybaord': 'KEY_D'}}


# callback functions
def gpio_callback(pin, value):
    print(value)


# register interrupt
bouncetime = round(1/30*1000)  # 30 FPS
for pin in keymap:
    GPIO.add_interrupt_callback(int(pin), gpio_callback, edge='both', pull_up_down=GPIO.PUD_UP, threaded_callback=True, debounce_timeout_ms=bouncetime)

# save keymap
with open('keymap.json', 'w') as fid:
    json.dump(keymap, fid, indent=4, sort_keys=True, ensure_ascii=False)


# main loop
try:
    print('Press CTRL+C to stop to exit')
    signal.pause()
except KeyboardInterrupt:
    GPIO.cleanup()  # clean up

print('all done')
