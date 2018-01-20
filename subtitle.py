import datetime
import re


class Sub:
    def __init__(self, index, start, end, text):
        self.index = index
        self.start = start
        self.end = end
        self.text = text

class Subtitle:
    def __init__(self):
        self.subs = []
        self.regex = re.compile(r"""(?P<index>\d+)\n
                (?P<start_h>\d\d):
                (?P<start_m>\d\d):
                (?P<start_s>\d\d),
                (?P<start_ms>\d\d\d)\s-->\s
                (?P<end_h>\d\d):
                (?P<end_m>\d\d):
                (?P<end_s>\d\d),
                (?P<end_ms>\d\d\d)\n
                (?P<text>(?:.+\n?)+)""", re.VERBOSE | re.MULTILINE)

    def parse(self, path):
        # open file and read content
        f = open(path)
        raw_text = f.read()
        f.close()

        # parse content
        for match in self.regex.finditer(raw_text):
            index = int(match.group('index'))
            start_h = int(match.group('start_h'))
            start_m = int(match.group('start_m'))
            start_s = int(match.group('start_s'))
            start_ms = int(match.group('start_ms'))
            end_h = int(match.group('end_h'))
            end_m = int(match.group('end_m'))
            end_s = int(match.group('end_s'))
            end_ms = int(match.group('end_ms'))
            text = match.group('text').rstrip()  # remove trailing \n

            # create datetime.time objects
            start = datetime.time(start_h, start_m, start_s, start_ms*1000)
            end = datetime.time(end_h, end_m, end_s, end_ms*1000)

            # append subs
            self.subs.append(Sub(index, start, end, text))

subs = Subtitle()
subs.parse('sub.srt')