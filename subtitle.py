class Sub:
    def __index__(self, index ,start, end, text):
        self.index = index
        self.start = start
        self.end = end
        self.text = text

class Subtitle:
    def __index__(self):
        self.subs = []

    def parse_block(self, block):
        index = block[1]

    def parse(self, path):
        f = open(path)
        text = f.read()
        f.close()
        for block in text.split('\n\n'):
            self.parse_block(block)

subs = Subtitle()
subs.parse('sample.txt')