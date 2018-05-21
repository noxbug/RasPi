from flask import Flask, render_template, redirect, request, url_for
from lib.kodi import Kodi as Kodi


class NowPlaying:
    def __init__(self):
        #self.title = 'Nothing Playing'
        #self.artist = 'Unknown'
        #self.album_art = '/static/ben.jpg'
        self.title = ''
        self.artist = ''
        self.album_art = '/static/blue.png'
        self.play = False
        self.position = 0
        self.active = False

    def reset(self):
        self.__init__()

    def update(self):
        player = kodi.get_active_player()
        if len(player) != 0:
            self.active = True
            item = kodi.get_item()
            now_playing.title = item['label']
            if item['type'] == 'episode':
                now_playing.artist = item['showtitle']
            else:
                now_playing.artist = item['showtitle']
            now_playing.album_art = kodi.album_art()
        else:
            now_playing.reset()


app = Flask(__name__)

kodi = Kodi('192.168.1.10')
now_playing = NowPlaying()

@app.route('/')
@app.route('/index')
def index():
    global kodi
    global now_playing
    now_playing.update()
    return render_template('now_playing.html', now_playing=now_playing)

@app.route('/play')
def play():
    global kodi
    global now_playing
    try:
        now_playing.play = kodi.play_pause()
        now_playing.get_position = kodi.get_position()['percentage']
        now_playing.update()
    except:
        now_playing.reset()
    return redirect(request.referrer)

@app.route('/stop')
def stop():
    global kodi
    global now_playing
    kodi.stop()
    now_playing.reset()
    return redirect(url_for('index'))

@app.route('/next')
def next():
    global kodi
    global now_playing
    try:
        now_playing.get_position = kodi.fast_forward()['percentage']
    except:
        now_playing.reset()
    return redirect(url_for('index'))

@app.route('/previous')
def previous():
    global kodi
    global now_playing
    try:
        now_playing.get_position = kodi.fast_rewind()['percentage']
    except:
        now_playing.reset()
    return redirect(url_for('index'))

@app.route('/remote')
def remote():
    now_playing.update()
    return render_template('remote.html', now_playing=now_playing)

@app.route('/up')
def up():
    global kodi
    kodi.input_up()
    return redirect(url_for('remote'))

@app.route('/down')
def down():
    global kodi
    kodi.input_down()
    return redirect(url_for('remote'))

@app.route('/left')
def left():
    global kodi
    kodi.input_left()
    return redirect(url_for('remote'))

@app.route('/right')
def right():
    global kodi
    kodi.input_right()
    return redirect(url_for('remote'))

@app.route('/select')
def select():
    global kodi
    now_playing.update()
    kodi.input_select()
    return redirect(url_for('remote'))

@app.route('/back')
def back():
    global kodi
    kodi.input_back()
    return redirect(url_for('remote'))

@app.route('/home')
def home():
    global kodi
    kodi.input_home()
    return redirect(url_for('remote'))

@app.route('/context_menu')
def context_menu():
    global kodi
    kodi.input_context_menu()
    return redirect(url_for('remote'))

@app.route('/info')
def info():
    global kodi
    kodi.input_info()
    return redirect(url_for('remote'))

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