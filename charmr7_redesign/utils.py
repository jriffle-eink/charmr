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

def get_input(swipe = None, t=None): # Optional t input is the timeout, meant for slideshow
    """
    get_Input() waits indefintely for either a screen touch or a button press and returns global values 'button, touch'
    If a button is pressed, returns as 'up', 'down' or 'enter'. Brightness button returns as None.
    The screen can be either tapped or swiped.
        If screen is tapped, returns as a tuple giving location of the tap.
        If the screen is swiped, returns the direction of swipe as a string 'swipe left', 'swipe right', 'swipe up', or 'swipe down'
    Optional argument t: Timeout feature. get_Input will wait for t milliseconds before exiting function and moving on
    """
    button = None; touch = None

    if t != None:
        start_Time = time.time()

    touchd_proc = subprocess.Popen('get_touch -d 3000 -n', stdout = subprocess.PIPE, shell = True)
    button_proc = subprocess.Popen('get_button 1', stdout = subprocess.PIPE, shell = True) 
    
    while button_proc.returncode is None:
        touchd_proc.poll(); button_proc.poll()
        if t != None and (time.time() - start_Time)*1000 >= t: 
            break
        #else: self.display.display_clock() # On-screen clock display
        if touchd_proc.returncode is None: 
            pass
        else: 
            break    

    
    if touchd_proc.returncode is not None: 
        if swipe != None:
            timestart = time.time()
            touchu_proc = subprocess.Popen('get_touch -u 1000 -n', stdout = subprocess.PIPE, shell = True)
            while touchu_proc.returncode is None and (time.time()-timestart)<0.75:
                touchu_proc.poll(); break
        touchd, err = touchd_proc.communicate(); button = None
        touch_Split = touchd.split(', '); tx = int(touch_Split[0]); ty = int(touch_Split[1])
        touchd = [tx, ty]  

        touch = touchd
        if swipe != None:
            touchu, err = touchu_proc.communicate(); button = None
            touch_Split = touchu.split(', '); tx = int(touch_Split[0]); ty = int(touch_Split[1])
            touchu = [tx, ty]   
            if abs(touchd[0] - touchu[0]) < 200 and abs(touchd[1] - touchu[1]) < 200:
                touch = touchd  
            if abs(touchd[0] - touchu[0]) > 200 or abs(touchd[1] - touchu[1]) > 200:
                if touchd[0] - touchu[0] > 0 and abs(touchd[0] - touchu[0]) > 2.7*abs(touchd[1] - touchu[1]): # 2.7 corresponds to swipes being within 20 degrees of x,y axes
                    touch = "swipe right"
                if touchd[0] - touchu[0] < 0 and abs(touchd[0] - touchu[0]) > 2.7*abs(touchd[1] - touchu[1]):
                    touch = "swipe left"
                if touchd[1] - touchu[1] > 0 and abs(touchd[1] - touchu[1]) > 2.7*abs(touchd[0] - touchu[0]):
                    touch = "swipe up"
                if touchd[1] - touchu[1] < 0 and abs(touchd[1] - touchu[1]) > 2.7*abs(touchd[0] - touchu[0]):
                    touch = "swipe down"     

        button_proc.kill()
        return touch
    
    elif button_proc.returncode is not None: 
        button, err = button_proc.communicate(); 
        button = int(button); touch = None
        if   button == 1: button = 'up'
        elif button == 2: button = 'down'
        elif button == 4: button = 'enter'
        
        touchd_proc.kill()
        return button
        
    else: 
        button = None; touch = None
        button_proc.kill(); 
        touchd_proc.kill()

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