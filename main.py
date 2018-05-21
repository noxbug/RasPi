import lib.kodirpc as kodi

kodi.connect('192.168.1.10')
kodi.nowplaying.smart_updater()

print(kodi.nowplaying.title)