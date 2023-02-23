import cmodule.charmr_module as cm
import os
import sys
import signal
import importlib
import time
import math
import subprocess
import numpy as np
import datetime
import threading
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from view import Display
from mainapplication import DemoModel
import utils
from model.brightnesstemperaturemenu import BrightnessTemperatureMenu
import model.basemenu
from model.mainmenu import MainMenu
from model.slideshow import Slideshow


'''
This class is responsible for recieving user input. It will send input to the functionControl class, which will manipulate slideshow, 
brightness, etc. as necessary. Any updates to the state of the program will be shown by the screenDisplay class.

Parameters:
program_model (functionControl) : responsible for deciding what to do with user input (modify slideshow, sketch, etc.)
display (screenDisplay) : responsible for displaying any changes to the state of the program (changing slides, highlighting, etc.)

'''

class Controller:

    global touch_dict
    
    touch_dict={
            'brightness_button': [[0,1716], [215,1920]],
            'temperature_button': [[215,1716], [420,1920]],
            'sketch_button': [[.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,1.000*cm.hsize]],
            'settings_button': [[.8507*cm.wsize,.8854*cm.hsize], [1.000*cm.wsize,1.000*cm.hsize]],
            'exit_button': [[.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]],
            'back_button': [[.6736*cm.wsize,.1771*cm.hsize], [.7708*cm.wsize,.2396*cm.hsize]],
            'slider': [[460,1730], [990,1850]]
            }


    def __init__(self): 
        #NULL CHECKS
        self.touch_input = None
        self.button_input = None

        self.bght_temp_menu = BrightnessTemperatureMenu()

        self.main_menu = MainMenu()

        self.wfm_transition_dict = {'dictionary of waveform transitions'}

        self.current_application = 'main'

        self.display = Display()

        self.components={
        'main': self.send_menu_input,
        # 'slideshow': self.send_slideshow_input,
        # 'pause': self.send_pause_input,
        # 'mainsettings': self.send-msettings_input

    }
      

      # slideshow is a component of the controller and not the model because it is very view-heavy (all it does is change display UNLESS pause is pressed)
      # main menu serves as a setup for appropriate apps, however, does not control each application -> control of each application is independendt of main menu
      # so that we are not tied to a single main menu


    # Waits for user input
    def run(self):
        while True:
            user_input = get_input()

            if type(user_input) == list: # screen touched 
                
                # below options only available on pause and main screens
                if self.current_application == 'main' or 'mainsettings' or 'pause' or 'pausesettings':
                    # these options can only be selected with touch (list)
                    if utils.touch_zone(user_input, touch_dict['slider']):
                        self.load_slider(user_input)
                    elif utils.touch_zone(user_input, touch_dict['brightness_button']): 
                        self.load_brightness()
                    elif utils.touch_zone(user_input, touch_dict['temperature_button']):
                        self.load_temperature()          
                    elif utils.touch_zone(user_input, touch_dict['settings_button']): 
                        self.load_settings()

            # these options can be selected by touch or buttons
            elif type(user_input) == str or list:
                func = self.components[self.current_application](user_input)

    def load_settings(self):
        if self.current_application == 'main':
            self.current_application = 'mainsettings'
            #self.display.display_msettings()
        elif self.current_application == 'pause':
            self.current_application = 'pausesettings'
            #self.display.display_psettings()

    def load_slider(self, user_input):
        # figure out how to display check - in Jake's code it is tied up with buttons method
        #self.model.update_slider(user_input)
        self.bght_temp_menu.brightness_temperature_slider(user_input)
    
    def load_brightness(self):
        self.bght_temp_menu.select_type("bght")
        self.display.load_area(self.bght_temp_menu.directory + 'label_brightness.pgm', (616,1718))   

    def load_temperature(self):
        self.bght_temp_menu.select_type("temp")
        self.display.load_area(self.bght_temp_menu.directory + 'label_temperature.pgm', (616,1718))

    def load_startup(self):
        self.current_application = 'main'
        self.display.display_startup_screen()

    def send_menu_input(self, user_input):
        command = self.main_menu.process_input(user_input)

        app = self.main_menu.app_selector(command)
        # turn this into dictionary
        if app is Slideshow:
            self.current_application = 'slideshow'

            # create a new thread to run this
            self.slideshow_run(app)
        elif app is Sketch:
            self.current_application = 'sketch'
            self.sketch_run(app)

    def load_pause():
        self.current_application = 'pause'
        self.display.display_pause()                                                                                                                                                                                                                                                                       

    def sketch_run(app):
        self.main_menu.launch_sketch_app()
        self.display.display_sketch_app()

    def slideshow_run(self, slideshow):
        while slideshow.cur_slide <  slideshow.length:
            user_input = self.get_input(t=slideshow.slide_timer())

            # no input before slide times out, automatically transition to next slide
            if user_input == None:
                self.display.change_slide(slideshow, "next")
            else:
                output = self.process_slideshow_input(user_input)

                # come up with something better. Right now, if user pauses process input will return QUIT signifying that autoplay of slideshow should end
                if output == 'QUIT':
                    return

    def process_slideshow_input(self, slideshow, user_input):
        if type(user_input) == list: 
            slideshow.pause()
            #direction = 'remain'
            self.load_pause()

            return 'QUIT'
            # CLEAR("strd")# Tap touch returns list value

        elif type(user_input) == str: # Swipe touch returns string value
            if user_input == "swipe left":  
                direction = "next"
            if user_input == "swipe right":
                direction = "back"
            if user_input == "swipe down":
                self.load_main()
                return 'QUIT'
            if user_input == "swipe up" or "enter":
                self.load_pause()
                return 'QUIT'
            if user_input == "up":
                direction = "next"
            if user_input == "down":
                direction = "back"          

        self.display.change_slide(slideshow, direction) # LOADS AND DISPLAYS SLIDE

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

        if cm.touch: # charmr_module.py determines whether the controller has touch feature
            touchd_proc = subprocess.Popen('get_touch -d 3000 -n', stdout = subprocess.PIPE, shell = True)
        button_proc = subprocess.Popen('get_button 1', stdout = subprocess.PIPE, shell = True) 
        
        if cm.touch:
            while button_proc.returncode is None:
                touchd_proc.poll(); button_proc.poll()
                if t != None:
                    if (time.time() - start_Time)*1000 >= t: 
                        break
                else: self.display.display_clock() # On-screen clock display
                if touchd_proc.returncode is None: 
                    pass
                else: 
                    break
        else:
            while button_proc.returncode is None:
                button_proc.poll()
                if t != None:
                    if (time.time() - start_Time)*1000 >= t: 
                        break
                else: self.display.display_clock() # On-screen clock display
        
        if cm.touch and touchd_proc.returncode is not None: 
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
            if cm.touch: touchd_proc.kill()
            return button
            
        else: 
            button = None; touch = None
            button_proc.kill(); 
            if cm.touch: touchd_proc.kill()

c = Controller()

c.run()