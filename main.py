from kodi import *
from lcd import*

mykodi = Kodi()
mykodi.get_player_item()


myLcd = Lcd()
myLcd.write_string('pipi')
myLcd.set_ddram_address(0,1)
myLcd.cleanup()



print('Done!')