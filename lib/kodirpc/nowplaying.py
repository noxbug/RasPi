from . import player
from . import rpc
import datetime
import sched
import time


global title
global artist
global album
global albumart
global play
global position
global currenttime
global totaltime
global active


def convert_time(time):
    """Convert time dictionary to datetime.time object"""
    return datetime.time(time['hours'], time['minutes'], time['seconds'], time['milliseconds']*1000)


def convert_deltatime(time):
    """Convert datetime.time object to datetime.deltatime object"""
    return datetime.timedelta(time.hour, time.minute, time.second)


def reset():
    """Reset the now playing section"""
    global title
    global artist
    global album
    global albumart
    global play
    global position
    global currenttime
    global totaltime
    global active

    title = ''
    artist = ''
    album = ''
    albumart = ''
    play = False
    position = 0
    active = False  # used to show/hide mini player


def update():
    """Update the now playing section"""
    global title
    global artist
    global album
    global albumart
    global play
    global position
    global currenttime
    global totaltime
    global active

    item = player.get_item()
    try:
        title = item['title']
        albumart = player.get_album_art_url()
        pos = player.get_position()
        position = pos['percentage']
        currenttime = convert_time(pos['time'])
        totaltime = convert_time(pos['totaltime'])
        play = bool(pos['speed'])
        active = True

        if item['type'] == 'song':
            artist = item['artist'][0]
            album = item['album']

        elif item['type'] == 'episode':
            artist = item['showtitle']
            album = 'Season ' + str(item['season'])

        elif item['type'] == 'movie':
            artist = ''
            album = ''
    except:
        reset()


def smart_updater():
    """Automatic update the now playing section based on the expected end time of now playing item"""
    global title
    global artist
    global album
    global albumart
    global play
    global position
    global currenttime
    global totaltime
    global active

    # update now playing section
    update()

    # calculate expected end time + 3s margin
    endtime = datetime.datetime.now()+convert_deltatime(totaltime)-convert_deltatime(currenttime)+datetime.timedelta(0, 0, 3)

    # code based on: https://pymotw.com/2/sched/
    scheduler = sched.scheduler(time.time, time.sleep)

    print('test')
