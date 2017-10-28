from kodi import *
from lcd import*

kodi = Kodi()
player=kodi.get_active_players()
print(player)
now_playing = kodi.get_item()
print(now_playing)


print('Done!')