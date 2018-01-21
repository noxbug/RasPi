from subtitle import Subtitle
import sys

path = sys.argv[1]

sub = Subtitle()
sub.open(path)
sub.translate()
