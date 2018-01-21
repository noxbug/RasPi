from subtitle import Subtitle
import sys

path = sys.argv[1]
#path = 'sub.srt'

sub = Subtitle()
sub.open(path)
sub.translate()
