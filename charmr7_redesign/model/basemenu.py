import math
import sys
sys.path.append('.')
import utils as utils
sys.path.append('cmodule')

import charmr_module as cm
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

'''
Abstraction of all common functionality between different menus (main menu, settings menu, etc.)

PARAMETERS
locations: list (locations of menu options on the screen)
check_file: str (the checkmark style the  menu will use)
uncheck_file: str (the uncheck style the  menu will use)
'''

class BaseMenu(object):
    
    def __init__(self, view, locations, check_file, uncheck_file):

        self.locations = locations

        self.view = view

        self.cur_check = 0

        # the user-specified check file
        self.check_file = check_file

        # the user-specified uncheck file
        self.uncheck_file = uncheck_file
        
        self.touch_dict={
            'brightness_button': [[0,1716], [215,cm.hsize]],
            'temperature_button': [[215,1716], [420,cm.hsize]],
            'sketch_button': [[.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,cm.hsize]],
            'settings_button': [[.8507*cm.wsize,.8854*cm.hsize], [cm.wsize,cm.hsize]],
            'exit_button': [[.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]],
            'back_button': [[.6736*cm.wsize,.1771*cm.hsize], [.7708*cm.wsize,.2396*cm.hsize]],
            'slider': [[460,1730], [990,1850]]
            }

    def change_checkmark(self):    
    
        self.view.change_checkmarked_option(self.locations, self.cur_check)
        
    def menu_locations(self, locations, check):
        
        self.locations = locations
        self.check = check

    '''
    NOTE this is unchanged from the original code - I don't really know how it works so I am going to circle back later and try to
    simplify it.
    '''
    
    def buttons(self, button_input):
        """
        Manages the button locations and button movements of all the menu lists.
        Works for menus with any number of buttons, 1 through N
        Once called, button presses are automatically interpreted and the menu list is altered.
        MENU: The menu name (menu.{name}), of the menu list to be managed. 
        disp: If disp = 'display', diplays the updated menu list using DISPLAY(charmr_module.check.wfm, 'part')
        check_File & uncheck_File: If the user wishes to use a different checkmark icon, place the file destinations here.
        """

        # basically this method makes the menu, checks the first option, then if a new option is selected unchecks the original option and checks the new option
        n = len(self.locations)
        array = [0]*n
        for i in range(n):
            if i == 0: array[i] = 1
            else: array[i] = 0
        matrix = [ [array[(col-row)%n] for col in range(n)] for row in range(n)] # Matrix defining the possible check button positions (identity matrix)
        # Here the column # is the button that is checked, while the row # is the initally selected button location
        if   button_input == 'down':  matrix = [[array[(col-row-1)%n] for col in range(n)] for row in range(n)] 
        elif button_input == 'up':    matrix = [[array[(col-row+1)%n] for col in range(n)] for row in range(n)]      
        elif button_input == 'enter': select = self.cur_check # Enter/pause button
        # In this new matrix, the column # is the new button to be checked, while the row # is the previously checked location

        if   button_input == 'down': self.cur_check = (self.cur_check+1)%n
        elif button_input == 'up': self.cur_check = (self.cur_check-1)%n

    '''
    Takes in the touch location and determines which menu item was selected based on how many total menu items there are - unchanged from 
    the original, but in the future I plan to not have max 5 menu options hardcoded so there can be an unlimited number of menu options.

    ARGUMENTS
    touch: list (the x, y coordinates of wwhere the user touched)

    RETURN
    Menu item selected (int)
    '''
    def menu_touch(self, touch): #-> int:
        x1 = math.ceil(.1944*cm.wsize); x2 = math.ceil(.7986*cm.wsize)
        if   len(self.locations) == 1:
            if utils.touch_zone(touch, [[x1,math.ceil(.4219*cm.hsize)], [x2,math.ceil(.5260*cm.hsize)]]): self.cur_check = 0; return 1
        elif len(self.locations) == 2:
            if utils.touch_zone(touch, [[x1,math.ceil(.3281*cm.hsize)], [x2,math.ceil(.4375*cm.hsize)]]): self.cur_check = 0; return 1
            if utils.touch_zone(touch, [[x1,math.ceil(.5313*cm.hsize)], [x2,math.ceil(.6458*cm.hsize)]]): self.cur_check = 1; return 2       
        elif len(self.locations) == 3:
            if utils.touch_zone(touch, [[x1,math.ceil(.2969*cm.hsize)], [x2,math.ceil(.4010*cm.hsize)]]): self.cur_check = 0; return 1
            if utils.touch_zone(touch, [[x1,math.ceil(.4323*cm.hsize)], [x2,math.ceil(.5417*cm.hsize)]]): self.cur_check = 1; return 2
            if utils.touch_zone(touch, [[x1,math.ceil(.5729*cm.hsize)], [x2,math.ceil(.6771*cm.hsize)]]): self.cur_check = 2; return 3
        elif len(self.locations) == 4:
            if utils.touch_zone(touch, [[x1,math.ceil(.2917*cm.hsize)], [x2,math.ceil(.3958*cm.hsize)]]): self.cur_check = 0; return 1
            if utils.touch_zone(touch, [[x1,math.ceil(.3958*cm.hsize)], [x2,math.ceil(.5104*cm.hsize)]]): self.cur_check = 1; return 2
            if utils.touch_zone(touch, [[x1,math.ceil(.5104*cm.hsize)], [x2,math.ceil(.6250*cm.hsize)]]): self.cur_check = 2; return 3
            if utils.touch_zone(touch, [[x1,math.ceil(.6250*cm.hsize)], [x2,math.ceil(.7292*cm.hsize)]]): self.cur_check = 3; return 4  
        elif len(self.locations) == 5:
            if utils.touch_zone(touch, [[x1,math.ceil(.2708*cm.hsize)], [x2,math.ceil(.3593*cm.hsize)]]): self.cur_check = 0; return 1
            if utils.touch_zone(touch, [[x1,math.ceil(.3593*cm.hsize)], [x2,math.ceil(.4583*cm.hsize)]]): self.cur_check = 1; return 2
            if utils.touch_zone(touch, [[x1,math.ceil(.4583*cm.hsize)], [x2,math.ceil(.5521*cm.hsize)]]): self.cur_check = 2; return 3
            if utils.touch_zone(touch, [[x1,math.ceil(.5521*cm.hsize)], [x2,math.ceil(.6458*cm.hsize)]]): self.cur_check = 3; return 4
            if utils.touch_zone(touch, [[x1,math.ceil(.6458*cm.hsize)], [x2,math.ceil(.7292*cm.hsize)]]): self.cur_check = 4; return 5
    
    '''
    Creates and saves the menu image file to be displayed for the specific menu, and determines the locations of the different options
    on the menu depending on number of total options
    NOTE this is unchanged from the original, going to come back and simplify it once the redesign is working and tested

    ARGUMENTS
    menu_type: str (what type of menu)
    name (optional): str (the name of the menu)
    items (optional): list (what menu items should be included in the menu)

    RETURN
    button_List: list (a list of menu item locations on demo screen)
    items: list (a list of the menu items included in the menu in case one was not provided)
    '''
    def menu_build(self, menu_type, name = "", items = []): # -> list, list
        
        if cm.wsize == 1440 and cm.hsize == 1920: 
            directory = '/mnt/mmc/images/charmr/1440x1920/'
        if cm.wsize == 1264 and cm.hsize == 1680: 
            directory = '/mnt/mmc/images/charmr/1264x1680/'
        
        if   int(cm.wsize) == 1440 and int(cm.hsize) == 1920: 
            if   menu_type == 'main': 
                img = directory + "menu_main2.pgm"
                if cm.app1.name != "": items.append(cm.app1.name)
                if cm.app2.name != "": items.append(cm.app2.name)
                if cm.app3.name != "": items.append(cm.app3.name)
                if cm.app4.name != "": items.append(cm.app4.name)
                if cm.app5.name != "": items.append(cm.app5.name)
            elif menu_type == 'menu': 
                img = directory + "menu_reg.pgm"
        elif int(cm.wsize) == 1264 and int(cm.hsize) == 1680: 
            if   menu_type == 'main': 
                img = directory + "menu_main.pgm"
                if cm.app1.name != "": items.append(cm.app1.name)
                if cm.app2.name != "": items.append(cm.app2.name)
                if cm.app3.name != "": items.append(cm.app3.name)
                if cm.app4.name != "": items.append(cm.app4.name)
                if cm.app5.name != "": items.append(cm.app5.name)
            elif menu_type == 'menu': 
                img = directory + "menu_reg.pgm"        
        img = Image.open(img)
        I1 = ImageDraw.Draw(img)
        I1.fontmode = "1"
        buttonfont_Offset = 10
        xstart_Text = math.ceil(0.3055*cm.wsize)
        xstart_button = math.ceil(0.2083*cm.wsize)
        myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/Sans_CM.ttf", 110)
        if   len(items) == 1:
            ystart = math.ceil(.4375*cm.hsize)
            for iteration, item in enumerate(items):
                I1.text((xstart_Text, ystart), item, font=myFont, fill=0)
            button_List = [(xstart_button,ystart+buttonfont_Offset)]   
        elif len(items) == 2:
            ystart = math.ceil(.3490*cm.hsize); step = math.ceil(.2083*cm.hsize)
            for iteration, item in enumerate(items):
                I1.text((xstart_Text, ystart + step*iteration), item, font=myFont, fill=0)
            button_List = [(xstart_button,ystart+buttonfont_Offset), (xstart_button,ystart+step+buttonfont_Offset)]            
        elif len(items) == 3:  
            ystart = math.ceil(.3125*cm.hsize); step = math.ceil(.1406*cm.hsize)
            for iteration, item in enumerate(items):
                I1.text((xstart_Text, ystart + step*iteration), item, font=myFont, fill=0)  
            button_List = [(xstart_button,ystart+buttonfont_Offset), (xstart_button,ystart+step+buttonfont_Offset), (xstart_button,ystart+(2*step)+buttonfont_Offset)]        
        elif len(items) == 4:
            ystart = math.ceil(.3020*cm.hsize); step = math.ceil(.1146*cm.hsize)
            for iteration, item in enumerate(items):
                I1.text((xstart_Text, ystart + step*iteration), item, font=myFont, fill=0)  
            button_List = [(xstart_button,ystart+buttonfont_Offset), (xstart_button,ystart+step+buttonfont_Offset), (xstart_button,ystart+(2*step)+buttonfont_Offset), (xstart_button,ystart+(3*step)+buttonfont_Offset)]       
        elif len(items) == 5:      
            ystart = math.ceil(.2813*cm.hsize); step = math.ceil(.0990*cm.hsize)
            for iteration, item in enumerate(items):
                I1.text((xstart_Text, ystart + step*iteration), item, font=myFont, fill=0)
            button_List = [(xstart_button,ystart+buttonfont_Offset), (xstart_button,ystart+step+buttonfont_Offset), (xstart_button,ystart+(2*step)+buttonfont_Offset), (xstart_button,ystart+(3*step)+buttonfont_Offset), (xstart_button,ystart+(4*step)+buttonfont_Offset)]
        print("Menu " + name + " of length=" + str(len(items)) + " built")       
        menu = directory + "tmp" + name + ".pgm" 
        print("Saved to location: " + menu)
        img.save(menu)
        return button_List
