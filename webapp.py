from flask import Flask, render_template, redirect, url_for
from kodi import Kodi

webapp = Flask(__name__)

kodi = Kodi('192.168.1.10')
play = False

@webapp.route('/')
def index():
    global kodi
    global play

    player = kodi.get_active_players()
    if len(player) != 0:
        item = kodi.get_item()
        title = item['label']
        if item['type'] == 'episode':
            artist = item['showtitle']
        else:
            artist = item['showtitle']
        album_art_url = kodi.get_album_art()
    else:
        title = 'Nothing Playing'
        artist = 'Unkown'
        album_art_url = '/static/ben.jpg'
    return render_template('index.html', title=title, artist=artist, album_art=album_art_url, play=play)

@webapp.route('/previous')
def previous():
    global kodi
    kodi.fast_rewind()
    return redirect(url_for('index'))

@webapp.route('/play')
def play():
    global kodi
    global play
    try:
        play = kodi.play_pause()
    except:
        play = False
    return redirect(url_for('index'))

@webapp.route('/stop')
def stop():
    global kodi
    kodi.stop()
    return redirect(url_for('index'))

@webapp.route('/next')
def next():
    global kodi
    kodi.fast_forward()
    return redirect(url_for('index'))

@webapp.route('/translate_sub')
def translate_sub():
    global kodi
    kodi.translate_subtitle()
    return redirect(url_for('index'))

@webapp.route('/next_sub')
def next_sub():
    global kodi
    kodi.next_subtitle()
    return redirect(url_for('index'))

@webapp.route('/update')
def update():
    global kodi
    kodi.update_library()
    return redirect(url_for('index'))

if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')