import time
import json

# load keymap configuration
try:
    with open('keymap.json') as fid:
        keymap = json.load(fid)
except:
    print('Oops something went wrong! Load default keymap configuration')
    keymap = {1:{'keyboard': 'KEY_W', 'controller': 'UP'},
                2:{'keyboard': 'KEY_S', 'controller': 'DOWN'},
                3:{'keyboard': 'KEY_A', 'controller': 'LEFT'},
                4:{'keyboard': 'KEY_D', 'controller': 'RIGHT'}}

print('Done')


# save keymap
with open('keymap.json', 'w') as fid:
    json.dump(keymap, fid, indent=4, sort_keys=True, ensure_ascii=False)


print('all done')
