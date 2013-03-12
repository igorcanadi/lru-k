import sys
import json

lines = open('postgres.log').read().split('\n')[:-1]
pages = []
for i, line in enumerate(lines):
    if line[0:10] == 'LOG:  [AFB':
        try:
            pages.append(int(line[10:].split(']')[0]))
        except:
            pass

print json.dumps(pages)
