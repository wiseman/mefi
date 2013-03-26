import os
import os.path
import random


p = '/Users/jwiseman/Desktop/ask.metafilter'
files = os.listdir('/Users/jwiseman/Desktop/ask.metafilter')
random.shuffle(files)
for f in files[:5]:
  print os.path.join(p, f)
