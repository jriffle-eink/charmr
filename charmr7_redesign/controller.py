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
import utils as utils
from model.brightnesstemperaturemenu import BrightnessTemperatureMenu
import model.basemenu
from model.basemenu import BaseMenu as basemenu
from view import Display
from model.mainmenu import MainMenu
from model.mainsettingsmenu import MainSettingsMenu
from model.slideshow import Slideshow


'''
This class is responsible for recieving user input. It monitors what appplication the user is currently on (main menu, slideshow, etc.), and sends
the input to the appropriate application. It also sends commands to the display to display the appropriate application based on user input.
'''

class Controller:

    def __init__(self): 
        
        self.view = Display() 

        self.current_application = 'startup'
        
        #self.startup = Startup()
                
        # responsible for monitoring the brightness/temperature of the demo
        self.bght_temp_menu = BrightnessTemperatureMenu(self.view) 

        # responsible for monitoring applications that can be launched from the main menu (currently, slideshows, sketch app, and main menu settings)
        self.main_menu = MainMenu(self.view) # Builds menu, saves as temporary image

        self.main_settings_menu = MainSettingsMenu(self.view)
        
        self.slideshow = Slideshow(self.view, 1)

        # to be implemented
        self.wfm_transition_dict = {'dictionary of waveform transitions'} # should be loaded from a json file?
        
        # to be implemented - easier way to send user input to the appropriate input processing method
        # ideally - self.components[self.current_application](user_input) -> to process user input - no need for a big if/else
        # statement to figure out which method to send input to
        # self.components={'main': self.send_menu_input,
        #                  'mainsettings': self.send_msettings_input, 
        #                  # 'slideshow': self.send_slideshow_input,
        #                  # #'pause': self.send_pause_input,
        #                  # 'pausesettings': self.send_psettings_input
        #                  }

        self.touch_dict = basemenu.touch_dict
 
    def run(self):
        self.view.clear("text")
        self.view.clear("init")
        
        self.run_main_menu()
        
    '''
    Sets the current application to be the main menu and sends a command to display to load the appropriate screen.
    '''
    def run_main_menu(self):
        
        if self.current_application in ['startup', 'slideshow']:
            self.view.clear("best")
            self.main_menu.display()
            
        elif self.current_application == 'settings':
            self.view.clear("best", area=cm.area.menu)
            self.main_menu.display(area = ['body'])
            
        
        self.menu = self.main_menu
                
        self.current_application = 'main'
                
        self.buttons = self.main_menu.buttons
        
        self.command_dict = {'slider': self.bght_temp_menu.brightness_temperature_slider,
                             'brightness_button': self.bght_temp_menu.select_brightness,
                             'temperature_button': self.bght_temp_menu.select_temp,
                             'sketch_button': None,
                             'settings_button': self.run_settings,
                             0: self.run_slideshow,
                             1: None,
                             2: None,
                             3: None,
                             4: None
                             }
        
        self.wait_for_input()
        
    '''
    Sets the current application to the appropriate settings. If the user is currently in the 'main' application, changes the current application to main settings 
    ('msettings') and displays the appropriate screen by sending a command to the display class. If the user is currently in the 'pause' application, changes the 
    current application to the pause settings ('psettings') and displays the appropriate screen.
    '''
    def run_settings(self):

        if self.current_application == 'main':
            
            self.main_settings_menu.display()
            
            self.menu = self.main_settings_menu
            
            self.command_dict = {'slider': None,
                                 'brightness_button': None,
                                 'temperature_button': None,
                                 'sketch_button': None,
                                 'settings_button': self.run_main_menu,
                                 0: None,
                                 1: None,
                                 2: None,
                                 3: None,
                                 4: None
                                 }
            
        else: pass
    
        self.current_application = 'settings'
        
        self.wait_for_input()
        self.wait_for_settings_input()
        
    '''
    Autoruns the slideshow. If no user input is recieved before the slide timeout, sends a command to the display to change the slide. Otherwise, processes the slideshow
    input. If a 'QUIT' command is recieved from the slideshow input processing method, will terminate the slideshow autorun (essentially pausing the slideshow on the 
    current slide)
    '''
    def run_slideshow(self):
        
        self.current_application = 'slideshow'
        
        while self.slideshow.cur_slide <  self.slideshow.length:
            
            self.slideshow.display_slide("next")            
            user_input = utils.get_input(t=self.slideshow.slide_timer())

            # if no input before slide times out, automatically transition to next slide
            if user_input in [None, 'swipe left']:
                if self.slideshow.cur_slide < self.slideshow.length-1:
                    self.slideshow.change_slide("next")
                else: break
            
            if user_input == 'swipe right':
                if self.slideshow.cur_slide > 0:
                    self.slideshow.change_slide("back")
                else: 
                    self.slideshow.change_slide("remain")
            # else:
            #     output = self.process_slideshow_input(self.slideshow, user_input)

                # come up with something better. Right now, if user pauses process input will return QUIT signifying that autoplay of slideshow should end
                # if output == 'QUIT':
                #     return
        self.run_main_menu()
        
    def run_pause(self):

        if self.current_application == 'pause':
            
            self.main_settings_menu.display()
            
            #self.menu = self.pause_menu
            
            self.command_dict = {'slider': None,
                                 'brightness_button': None,
                                 'temperature_button': None,
                                 'sketch_button': None,
                                 'settings_button': self.run_settings
                                 }
            
        else: pass
    
        
        self.wait_for_input()
        
    def wait_for_input(self, timer = False):
    
        while True:
            
            user_input = utils.get_input()

            if type(user_input) == list: # screen touched, checks for common touch zones first

                for key in self.command_dict:      

                    if type(key) == str and utils.touch_zone(user_input, self.touch_dict[key]):

                        if key == 'slider': self.command_dict[key](user_input)
                        
                        else: self.command_dict[key]()


            # these menu-specific options can be selected by buttons
            elif type(user_input) == str: # button press
                                
                if user_input in ['up','down']:
                    
                    self.menu.buttons(user_input) # change the buttons appropriately
                    self.menu.change_checkmark()
                    
                elif user_input == 'enter':
                    
                    self.command_dict[self.menu.cur_check]() 

    def wait_for_settings_input(self):

            while True:

                user_input = utils.get_input()

                if type(user_input) == list: # screen touched, checks for common touch zones first
                    output = self.main_settings_menu.process_input(user_input)

                    if output != None:
                        if output == 'pause':
                            self.current_application = 'pause'
                                # display pause
                        elif output == 'main':
                            self.current_application = 'main'
                            self.main_menu.display()

                        else: self.slideshow.process_settings_output(output)

                    # # these menu-specific options can be selected by buttons
                    # elif type(user_input) == str: # button press

                    #     if user_input in ['up','down']:

                    #         self.menu.buttons(user_input) # change the buttons appropriately
                    #         self.menu.change_checkmark()

                    #     elif user_input == 'enter': pass

                    #         #super(MainMenu, self).cur_check  

    def send_psettings_input(self, user_input):
        output = self.slideshow.process_settings_input(user_input)
        
        slideshow_output = self.slideshow.process_settings_output(output)

        # need to update current application

        if slideshow_output == 'main':
            self.current_application = 'main'
        elif slideshow_output == 'pause':
            self.current_application = 'pause'

    def send_msettings_input(self, user_input):
        output = self.main_settings_menu.process_input(user_input)

        slideshow_output = self.slideshow.process_settings_output(output)
    

    '''
    Displays the temp/brightness slider and sends the user input to the BrightnessTemperatureSlider class to change the brightness/temperature on the device.
    '''
    def run_slider(self, user_input):
        # figure out how to display check - in Jake's code it is tied up with buttons method
        #self.model.update_slider(user_input)
        self.bght_temp_menu.brightness_temperature_slider(user_input)
    
    '''
    Displays the 'brightness' label above the brightness/temperature slider and updates the BrightnessTemperatureMenu's current application so that any touches on the
    slider will modify device brightness
    '''
    # def load_brightness(self):
    #     self.bght_temp_menu.select_type("bght")
    #     self.display.load_area(self.display.directory + 'label_brightness.pgm', (616,1718))   

    '''
    Displays the 'temperature' label above the brightness/temperature slider and updates the BrightnessTemperatureMenu's current application so that any touches on the
    slider will modify device temperature
    '''
    # def load_temperature(self):
    #     self.bght_temp_menu.select_type("temp")
    #     self.display.load_area(self.display.directory + 'label_temperature.pgm', (616,1718))

    '''
    Sets the current application to be 'main' and sends a command to display to display the starup screen.
    '''
    # def load_startup(self):
    #     self.current_application = 'main'
    #     self.display.display_startup_screen()

    '''
    Sends user input to the main menu. Currently, users can select either a slideshow or the sketch app to be run. The main menu will return the application that
    is selected, and the controller will either run and display the slideshow or run and display the sketch app.
    '''
    def send_menu_input(self, user_input):
        application = self.main_menu.process_input(user_input)

        # if application != None: 
        #     if type(application) == Slideshow:
        #         self.current_application = 'slideshow'
                
        #         self.slideshow = application

        #         self.slideshow_run()


    # def send_pause_input(self, user_input):
    #     self.slideshow.process_pause_input(user_input)

    '''
    Sets the current application to be 'pause' and sends a command to display to display the pause screen.
    '''
    def run_pause(self):
        self.current_application = 'pause'
        self.slideshow.display_pause()                                                                                                                                                                                                                                                                       

    def run_sketch(self, app): pass
        # self.main_menu.launch_sketch_app()
        # self.display.display_sketch_app()


    '''
    Processes any user input recieved while a slideshow is running.
    Tap touch (user_input is a list of touch coordinates)
        - pause slideshow and load the appropriate pause screen
    Swipe touch (user_input is a string)
        - either changes slide or loads pause/main screen based on swipe direction
    Button input (user_input is a string)
        - either changes slide or loads pause screen based on swipe direction
    '''
    def send_slideshow_input(self, slideshow, user_input):
        if type(user_input) == list: 
            #direction = 'remain'
            self.run_pause()

            return 'QUIT'
            # CLEAR("strd")# Tap touch returns list value

        elif type(user_input) == str: # Swipe touch returns string value
            if user_input == "swipe left":  
                direction = "next"
            if user_input == "swipe right":
                direction = "back"
            if user_input == "swipe down":
                self.run_main()
                return 'QUIT'
            if user_input == "swipe up" or "enter":
                self.run_pause()
                return 'QUIT'
            if user_input == "up":
                direction = "next"
            if user_input == "down":
                direction = "back"          

        self.slideshow.change_slide(direction) # LOADS AND DISPLAYS SLIDE
        
if __name__ == '__main__':

    c = Controller()

    c.run()