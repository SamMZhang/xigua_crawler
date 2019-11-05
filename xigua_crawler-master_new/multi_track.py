# coding: utf-8

import subprocess
import time
import atexit
import sys


commands = [
    'python3',
    '/home/iip/ZZB/Code/xigua_crawler-master/track.py',
    '1'
]

sub_ps = []
start = int(sys.argv[1])
stop = int(sys.argv[2])


def at_exit():
    for process in sub_ps:
        process.kill()

atexit.register(at_exit)

for i in range(start, stop):
    beg = time.time()
    commands[2] = str(i)
    sub_p = subprocess.Popen(commands)
    sub_ps.append(sub_p)
    print('{}th setup!'.format(i))
    time.sleep(900 - (time.time() - beg))

while True:
    print('all process is running.')
    q = input()
    if q == 'q':
        break

print('end')
