import lib.kodirpc as kodi
import time

kodi.connect('192.168.1.10')
kodi.nowplaying.update()

time.sleep(3*60)