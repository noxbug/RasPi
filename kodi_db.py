from subtitle import Subtitle
from kodi import Kodi

kodi = Kodi('192.168.1.10')
path = kodi.get_path_from_db()
info = kodi.help('Player.SetSubtitle')

subtitle = Subtitle()
subtitle.open(path)



print('pipi')

