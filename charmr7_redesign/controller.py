import cmodule.charmr_module as cm
import os
import sys
import signal
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
from model.mainsettingsmenu import MainSettingsMenu
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
            'brightness_button': [[0,1716], [215,cm.hsize]],
            'temperature_button': [[215,1716], [420,cm.hsize]],
            'sketch_button': [[.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,cm.hsize]],
            'settings_button': [[.8507*cm.wsize,.8854*cm.hsize], [cm.wsize,cm.hsize]],
            'exit_button': [[.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]],
            'back_button': [[.6736*cm.wsize,.1771*cm.hsize], [.7708*cm.wsize,.2396*cm.hsize]],
            'slider': [[460,1730], [990,1850]]
            }


    def __init__(self): 
        #NULL CHECKS
        self.touch_input = None
        self.button_input = None

        self.bght_temp_menu = BrightnessTemperatureMenu()
        print('1')
        self.main_menu = MainMenu()
        print('2')
        self.main_settings_menu = MainSettingsMenu()
        print('3')

        self.wfm_transition_dict = {'dictionary of waveform transitions'}
        print('4')

        self.current_application = 'main'
        print('5')

        self.display = Display()
        print('6')

        self.components={'main': self.send_menu_input(),
                         'mainsettings': self.send_msettings_input(), 
                         'slideshow': self.send_slideshow_input(),
                         'pause': self.send_pause_input(),
                         'pausesettings': self.send_psettings_input()
                         }
        print('7')
     

      # slideshow is a component of the controller and not the model because it is very view-heavy (all it does is change display UNLESS pause is pressed)
      # main menu serves as a setup for appropriate apps, however, does not control each application -> control of each application is independendt of main menu
      # so that we are not tied to a single main menu


    # Waits for user input
    def run(self):
        while True:
            user_input = utils.get_input()

            if type(user_input) == list: # screen touched, checks for common touch zones first
                
                # below options only available on pause and main screens
                if self.current_application in ['main', 'mainsettings', 'pause', 'pausesettings']:
                    # these options can only be selected with touch (list)
                    if utils.touch_zone(user_input, touch_dict['slider']):
                        self.load_slider(user_input)
                    elif utils.touch_zone(user_input, touch_dict['brightness_button']): 
                        self.load_brightness()
                    elif utils.touch_zone(user_input, touch_dict['temperature_button']):
                        self.load_temperature()          
                    elif utils.touch_zone(user_input, touch_dict['settings_button']): 
                        if self.current_application == 'main' or 'pause':
                            self.load_settings()
                        elif self.current_application == 'mainsettings':
                            self.current_application = 'main'
                            self.main_menu()
                        #elif self.current_application == 'pausesettings':

            # these menu-specific options can be selected by buttons or touch
            elif type(user_input) == str or list:
                func = self.components[self.current_application](user_input)

    def load_settings(self):
        if self.current_application == 'main':
            self.current_application = 'mainsettings'
            self.display.display_msettings()
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

        if command != None: command

    def load_pause():
        self.current_application = 'pause'
        self.display.display_pause()                                                                                                                                                                                                                                                                       

    def sketch_run(app):
        self.main_menu.launch_sketch_app()
        self.display.display_sketch_app()

    def slideshow_run(self, slideshow):
        while slideshow.cur_slide <  slideshow.length:
            user_input = utils.get_input(t=slideshow.slide_timer())

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

c = Controller()

print("about to run")

c.run()