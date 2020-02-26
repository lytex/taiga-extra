import re
from time import sleep
from taiga.exceptions import TaigaRestException

def wait(t):
    real = 1.1*t + 10
    print('Sleep for ', real, ' seconds')
    sleep(real)

def send(func):
    sent = False
    while not sent:
        try:
            func()
            sent = True
            # input('Next')
        except TaigaRestException as e:
            t = int(re.search('[0-9]+', e.args[0])[0])
            wait(t)