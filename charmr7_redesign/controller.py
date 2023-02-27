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
import utils as utils
from model.brightnesstemperaturemenu import BrightnessTemperatureMenu
import model.basemenu
from model.mainmenu import MainMenu
from model.mainsettingsmenu import MainSettingsMenu
from model.slideshow import Slideshow


'''
This class is responsible for recieving user input. It monitors what appplication the user is currently on (main menu, slideshow, etc.), and sends
the input to the appropriate application. It also sends commands to the display to display the appropriate application based on user input.
'''

class Controller:

    def __init__(self): 
        # I think these are unnecessary - user input can be stored as local variables since they are constantly changing
        # self.touch_input = None
        # self.button_input = None

        # responsible for monitoring the brightness/temperature of the demo
        self.bght_temp_menu = BrightnessTemperatureMenu()
        print('1')

        # responsible for monitoring applications that can be launched from the main menu (currently, slideshows, sketch app, and main menu settings)
        self.main_menu = MainMenu()
        print('2')
        self.main_settings_menu = MainSettingsMenu()
        print('3')

        self.slideshow = None

        # to be implemented
        self.wfm_transition_dict = {'dictionary of waveform transitions'}
        print('4')

        self.current_application = 'main'
        print('5')

        # responsible for displaying any changes to the demo (menus, slideshows, etc.)
        self.display = Display()
        print('6')

        # to be implemented - easier way to send user input to the appropriate input processing method
        # ideally - self.components[self.current_application](user_input) -> to process user input - no need for a big if/else
        # statement to figure out which method to send input to
        self.components={'main': self.send_menu_input,
                         'mainsettings': self.send_msettings_input, 
                         'slideshow': self.send_slideshow_input,
                         #'pause': self.send_pause_input,
                         'pausesettings': self.send_psettings_input
                         }
        print('7')

        self.touch_dict={
            'brightness_button': [[0,1716], [215,cm.hsize]],
            'temperature_button': [[215,1716], [420,cm.hsize]],
            'sketch_button': [[.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,cm.hsize]],
            'settings_button': [[.8507*cm.wsize,.8854*cm.hsize], [cm.wsize,cm.hsize]],
            'exit_button': [[.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]],
            'back_button': [[.6736*cm.wsize,.1771*cm.hsize], [.7708*cm.wsize,.2396*cm.hsize]],
            'slider': [[460,1730], [990,1850]]
            }


    '''
    Waits for user input. When input is recieved, sends input to correct processing function based on what the current application is.
    ''' 
    def run(self):
        while True:
            user_input = utils.get_input()

            if type(user_input) == list: # screen touched, checks for common touch zones first
                
                # below options only available on pause and main screens
                if self.current_application in ['main', 'mainsettings', 'pause', 'pausesettings']:
                    # these options can only be selected with touch (list)
                    if utils.touch_zone(user_input, self.touch_dict['slider']):
                        self.load_slider(user_input)

                    elif utils.touch_zone(user_input, self.touch_dict['brightness_button']): 
                        self.load_brightness()

                    elif utils.touch_zone(user_input, self.touch_dict['temperature_button']):
                        self.load_temperature()

                    elif utils.touch_zone(user_input, self.touch_dict['sketch_button']):
                         if self.current_application == 'pause' or 'pausesettings':
                            self.load_sketch()

                    elif utils.touch_zone(user_input, self.touch_dict['settings_button']): 
                        if self.current_application == 'main' or 'pause':
                            self.load_settings()

                        elif self.current_application == 'mainsettings':
                            self.load_main()

                        elif self.current_application == 'pausesettings':
                            self.load_pause()

            # these menu-specific options can be selected by buttons or touch
            elif type(user_input) == str or list:
                func = self.components[self.current_application](user_input)

    '''
    Sets the current application to be the main menu and sends a command to display to load the appropriate screen.
    '''
    def load_main(self):
        self.current_application = 'main'
        self.display.display_main_menu()

    '''
    Sets the current application to the appropriate settings. If the user is currently in the 'main' application, changes the current application to main settings 
    ('msettings') and displays the appropriate screen by sending a command to the display class. If the user is currently in the 'pause' application, changes the 
    current application to the pause settings ('psettings') and displays the appropriate screen.
    '''
    def load_settings(self):
        if self.current_application == 'main':
            self.current_application = 'mainsettings'
            self.display.display_msettings()
        elif self.current_application == 'pause':
            self.current_application = 'pausesettings'
            self.display.display_psettings()

    '''
    Displays the temp/brightness slider and sends the user input to the BrightnessTemperatureSlider class to change the brightness/temperature on the device.
    '''
    def load_slider(self, user_input):
        # figure out how to display check - in Jake's code it is tied up with buttons method
        #self.model.update_slider(user_input)
        self.bght_temp_menu.brightness_temperature_slider(user_input)
    
    '''
    Displays the 'brightness' label above the brightness/temperature slider and updates the BrightnessTemperatureMenu's current application so that any touches on the
    slider will modify device brightness
    '''
    def load_brightness(self):
        self.bght_temp_menu.select_type("bght")
        self.display.load_area(self.display.directory + 'label_brightness.pgm', (616,1718))   

    '''
    Displays the 'temperature' label above the brightness/temperature slider and updates the BrightnessTemperatureMenu's current application so that any touches on the
    slider will modify device temperature
    '''
    def load_temperature(self):
        self.bght_temp_menu.select_type("temp")
        self.display.load_area(self.display.directory + 'label_temperature.pgm', (616,1718))

    '''
    Sets the current application to be 'main' and sends a command to display to display the starup screen.
    '''
    def load_startup(self):
        self.current_application = 'main'
        self.display.display_startup_screen()

    def load_sketch(self):
            #def F_sketch(arg = None):
        """
        Clicking the sketch button during a paused slideshow calls acepsketch
        The draw function only works if the image is loaded as 'fast', highlighter as 'DU'
        This means for color images, any non-fast rendered images must be color index converted using color_convert()
        """
        slideshow_specs = self.slideshow.cm_slideshow
        
        if self.current_application == 'main':
            self.display.clear('best')
            os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt")
            self.load_main()
            return
        
        if self.current_application == 'psettings': # If demo was in a menu when the sketch button was pressed, remove the menu by reloading  and displaying the slide
            self.display.load(slideshow_specs) # Reload the slideshow slide #N
            self.display.display_area(slideshow_specs, (0,80), (1440,1715)) #Redisplay the background slideshow     

        if slideshow_specs.wfm[self.slideshow.cur_slide] == 3: # Only use highlighter on black and white text images
            self.display.load("/mnt/mmc/images/charmr/1440x1920/highlighter.pgm")   
            self.display.display(2, 'full')
            self.display.load(slideshow_specs)
            self.display.display_area(6, (0,80), (1440,1715))
            converted = PP1_22_40C(slideshow_specs.path + slideshow_specs.file[self.slideshow.cur_slide], 'text', 'pen') # color_convert.PP1_22_40C() for this GAL3 .wbf       
            # highlight_sketch.txt calls Jaya's ACeP sketch program. The background image is loaded as tmp_converted
            # This means that the color_convert function must be run regardless of the current wfm
            os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_highlighter.txt")
        else: # else use draw
            self.display.load("/mnt/mmc/images/charmr/1440x1920/draw.pgm")   
            self.display.display(2, 'full')
            converted = PP1_22_40C(slideshow_specs.path + slideshow_specs.file[self.slideshow.cur_slide], 'strd', 'fast') # color_convert.PP1_22_40C() for this GAL3 .wbf       
            os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_draw.txt")  
            
        self.load_pause() # Go back to pause when finished

    
    '''
    Sends user input to the main menu. Currently, users can select either a slideshow or the sketch app to be run. The main menu will return the application that
    is selected, and the controller will either run and display the slideshow or run and display the sketch app.
    '''
    def send_menu_input(self, user_input):
        application = self.main_menu.process_input(user_input)

        if application != None: 
            #UPDATE VIEW HERE!!! - SHOW SELECTED OPTION
            if type(application) == Slideshow:
                self.current_application = 'slideshow'
                
                self.slideshow = application

                self.slideshow_run()


    def send_msettings_input(self, user_input):
        pass

    def send_slideshow_input(self, user_input):
        pass

    # def send_pause_input(self, user_input):
    #     self.slideshow.process_pause_input(user_input)

    def send_psettings_input(self, user_input):

        # not ideal design, but prevents very convoluted code / needlessly passing info back and forth, so I am giving the slideshow access to the display. 
        # Once this version is up and running I want to go back and see if a better design is possible.
        output = self.slideshow.process_settings_input(user_input, self.display)

        # USE THIS TO TAKE CARE OF DISPLAYING PAUSE SCREEN CHECKMARKED OPTIONS, ETC
        self.display.update_pause_screen()

        if output == 'main':
            self.load_main()
        elif output == 'pause':
            self.load_pause()

    '''
    Sets the current application to be 'pause' and sends a command to display the pause screen.
    '''
    def load_pause(self):
        self.current_application = 'pause'
        self.display.display_pause()                                                                                                                                                                                                                                                                       

    '''
    Autoruns the slideshow. If no user input is recieved before the slide timeout, sends a command to the display to change the slide. Otherwise, processes the slideshow
    input. If a 'QUIT' command is recieved from the slideshow input processing method, will terminate the slideshow autorun (essentially pausing the slideshow on the 
    current slide)
    '''
    def slideshow_run(self):
        while self.slideshow.cur_slide <  self.slideshow.length:
            user_input = utils.get_input(t=self.slideshow.slide_timer())

            # no input before slide times out, automatically transition to next slide
            if user_input == None:
                self.display.change_slide(self.slideshow, "next")
            else:
                output = self.process_slideshow_input(self.slideshow, user_input)

                # come up with something better. Right now, if user pauses process input will return QUIT signifying that autoplay of slideshow should end
                if output == 'QUIT':
                    return

    '''
    Processes any user input recieved while a slideshow is running.
    Tap touch (user_input is a list of touch coordinates)
        - pause slideshow and load the appropriate pause screen
    Swipe touch (user_input is a string)
        - either changes slide or loads pause/main screen based on swipe direction
    Button input (user_input is a string)
        - either changes slide or loads pause screen based on swipe direction
    '''
    def process_slideshow_input(self, slideshow, user_input):
        if type(user_input) == list: 
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