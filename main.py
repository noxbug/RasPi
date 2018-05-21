import lib.kodirpc as kodi

#kodi.connect('192.168.1.10', 8080)
ping = kodi.rpc.ping()
print('done')