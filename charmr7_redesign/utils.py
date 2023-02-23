import cmodule.charmr_module as cm
import os
import sys
import signal
import imp
import time
import math
import subprocess
import numpy as np
import datetime
import threading
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def clock(arg = "check"):
    
    sample_Time = datetime.datetime.now() + datetime.timedelta(hours=11, minutes=6, seconds=33) # The controller clock isn't correct, needs an offset 
    if sample_Time.minute > 9:
        current_Time = str(str(sample_Time.hour) + ":" + str(sample_Time.minute) + sample_Time.strftime("%p"))
    else:
        current_Time = str(str(sample_Time.hour) + ":0" + str(sample_Time.minute) + sample_Time.strftime("%p"))
    # if device.time != current_Time or arg == 'load':
    #     device.time = current_Time
    if sample_Time.hour > 12:
        hour = sample_Time.hour - 12
    else:
        hour = sample_Time.hour
    if sample_Time.minute > 9:
        current_Time = str(hour) + ":" + str(sample_Time.minute) + sample_Time.strftime("%p")
    else:
        current_Time = str(hour) + ":0" + str(sample_Time.minute) + sample_Time.strftime("%p")   

    return [current_Time, hour]


def command(string, call):
    if   call == 'sub':   subprocess.call(string, shell = True)
    elif call == 'os':    os.system(string)
    elif call == 'Popen': subprocess.Popen(string, stdout=subprocess.PIPE, shell = True)

def wait(t):
    """
    Pauses the program for t milliseconds
    """
    time.sleep(t/1000)

def touch_zone(touch, location): # Detects whether the touch was in a specific area
    """
    location is a list of size 2 of tuples of size 2.
    The first tuple is the top left corner and second tuple is the bottom right corner of the touch zone, respectively.
    """
    if touch[0] > cm.wsize - location[1][0] and touch[0] < cm.wsize - location[0][0] and touch[1] > location[0][1] and touch[1] < location[1][1]:   
        return True
    else: 
        return False