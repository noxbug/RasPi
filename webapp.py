from flask import Flask, render_template, redirect, url_for
from kodi import Kodi


class Now_playing:
    def __init__(self):
        self.title = 'Nothing Playing'
        self.artist = 'Unkown'
        self.album_art = '/static/ben.jpg'
        self.play = False
        self.position = 0

app = Flask(__name__)

kodi = Kodi('192.168.1.10')
now_playing = Now_playing()

@app.route('/')
@app.route('/index')
def index():
    global kodi
    global now_playing

    player = kodi.active_player()
    if len(player) != 0:
        item = kodi.item()
        now_playing.title = item['label']
        if item['type'] == 'episode':
            now_playing.artist = item['showtitle']
        else:
            now_playing.artist = item['showtitle']
        now_playing.album_art = kodi.album_art()
    else:
        now_playing.title = 'Nothing Playing'
        now_playing.artist = 'Unkown'
        now_playing.album_art = '/static/ben.jpg'
    return render_template('now_playing.html', now_playing=now_playing)

@app.route('/play')
def play():
    global kodi
    global now_playing
    try:
        now_playing.play = kodi.play_pause()
        now_playing.position = kodi.position()['percentage']
    except:
        now_playing.play = False
        now_playing.position = 0
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global kodi
    global now_playing
    kodi.stop()
    now_playing.play = False
    now_playing.position = 0
    return redirect(url_for('index'))

@app.route('/next')
def next():
    global kodi
    global now_playing
    try:
        now_playing.position = kodi.fast_forward()['percentage']
    except:
        now_playing.play = False
        now_playing.position = 0
    return redirect(url_for('index'))

@app.route('/previous')
def previous():
    global kodi
    global now_playing
    try:
        now_playing.position = kodi.fast_rewind()['percentage']
    except:
        now_playing.play = False
        now_playing.position = 0
    return redirect(url_for('index'))

@app.route('/translate_sub')
def translate_sub():
    global kodi
    kodi.translate_subtitle()
    return redirect(url_for('index'))

@app.route('/next_sub')
def next_sub():
    global kodi
    kodi.next_subtitle()
    return redirect(url_for('index'))

@app.route('/update')
def update():
    global kodi
    kodi.update_library()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')