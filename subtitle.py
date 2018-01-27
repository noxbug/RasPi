from googletrans import Translator
from kodi import Kodi
import datetime
import sys
import os
import re

class Sub:
    def __init__(self, index, start, end, text):
        self.index = index
        self.start = start
        self.end = end
        self.text = text

class Subtitle:
    def __init__(self, language_id='nl', path=''):
        self.subs = []
        self.path = path
        self.language_id = language_id
        self.regex = re.compile(r"""(?P<index>\d+)\n
                (?P<start_HH>\d\d):
                (?P<start_MM>\d\d):
                (?P<start_SS>\d\d),
                (?P<start_mmm>\d\d\d)\s-->\s
                (?P<end_HH>\d\d):
                (?P<end_MM>\d\d):
                (?P<end_SS>\d\d),
                (?P<end_mmm>\d\d\d)\n
                (?P<text>(?:.+\n?)+)""", re.VERBOSE)

    def translate(self):
        translator = Translator()
        nsubs = str(len(self.subs))
        for sub in self.subs:
            sub.text = translator.translate(sub.text, dest=self.language_id).text
            print(' translate ' + str(sub.index) + ' of ' + nsubs, end='\r')
        self.save()

    def save(self):
        path_split = os.path.splitext(self.path)
        path_language_id = path_split[0] + '_' + self.language_id + path_split[1]
        file = open(path_language_id, 'w')
        for sub in self.subs:
            file.write(str(sub.index) + '\n')
            file.write(sub.start.strftime('%H:%M:%S,%f')[0:12] + ' --> ')
            file.write(sub.end.strftime('%H:%M:%S,%f')[0:12] + '\n')
            file.write(sub.text + '\n\n')
        file.close()


    def open(self, path):
        try:
            # open file and read content
            self.path = os.path.splitext(path)[0] + '.srt'
            file = open(self.path, 'r', encoding='iso-8859-1')
            raw_text = file.read()
            file.close()

            # parse content
            for match in self.regex.finditer(raw_text):
                index = int(match.group('index'))
                start_HH = int(match.group('start_HH'))
                start_MM = int(match.group('start_MM'))
                start_SS = int(match.group('start_SS'))
                start_mmm = int(match.group('start_mmm'))
                end_HH = int(match.group('end_HH'))
                end_MM = int(match.group('end_MM'))
                end_SS = int(match.group('end_SS'))
                end_mmm = int(match.group('end_mmm'))
                text = match.group('text').rstrip()  # remove trailing \n

                # create datetime.time objects
                start = datetime.time(start_HH, start_MM, start_SS, start_mmm * 1000)
                end = datetime.time(end_HH, end_MM, end_SS, end_mmm * 1000)

                # append subs
                self.subs.append(Sub(index, start, end, text))
        except:
            print('File not found: \"' + self.path + '\"')

if __name__ == '__main__':
    if sys.argv[1] == '-kodi':
        kodi = Kodi('192.168.1.10')
        path = kodi.get_item_path()
    else:
        path = sys.argv[1]

    subtitle = Subtitle()
    subtitle.open(path)
    subtitle.translate()
