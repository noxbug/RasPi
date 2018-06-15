from . import player
from . import rpc
import threading
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


def _dict_to_datetime(time):
    """Convert time dictionary to datetime.time object"""
    return datetime.time(time['hours'], time['minutes'], time['seconds'], time['milliseconds']*1000)


def _datetime_to_deltatime(time):
    """
    Convert datetime.time object to datetime.deltatime object
    Used to do calculations
    """
    return datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second, microseconds=time.microsecond)


def _deltatime_to_seconds(time):
    """
    Convert datetime.deltatime object to seconds
    Used for delay
    """
    return time.days*24*60*60 + time.seconds + time.microseconds/1000000


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
        currenttime = _dict_to_datetime(pos['time'])
        totaltime = _dict_to_datetime(pos['totaltime'])
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
            
        print('Update complete')
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

    try:
        # calculate expected end time + 3sec margin
        endtime = _deltatime_to_seconds( _datetime_to_deltatime(totaltime) - _datetime_to_deltatime(currenttime) + datetime.timedelta(seconds=3) )

        # code based on: https://pymotw.com/2/sched/
        scheduler = sched.scheduler(time.time, time.sleep)

        # schedule event
        update_event = scheduler.enter(endtime, 1, update)

        # start a thread to run the events
        thread = threading.Thread(target=scheduler.run)
        thread.start()

        print('done')
    except:
        pass
