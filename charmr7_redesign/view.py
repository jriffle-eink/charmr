import cmodule.charmr_module as cm
import model.basemenu
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
import utils

'''
This class is responsible for all visual renderings. The instrcutions for each display (main menu, pause, settings, slideshow) is broken up into distinct methods.
'''

class Display():
    
    def __init__(self): 
        self.rotation_Current = 1

        self.rot_List  = [[526, 1060], [833, 1060], [526, 1357],  [833, 1357]]
        self.disp_List = [[654, 826],  [990, 826]]
        self.flsh_List = [[599, 1108], [822, 1108], [1046, 1108], [599, 1300], [822, 1300]]
        self.auto_List = [1046, 1300]
        self.menu_List = [[270, 620],  [270, 820],  [270, 1020],  [270, 1220]]
        self.sshw_List = [[771, 575],  [887, 575],  [1003, 575]]
    
        if cm.wsize == 1440 and cm.hsize == 1920: 
            self.directory = '/mnt/mmc/images/charmr/1440x1920/'
        if cm.wsize == 1264 and cm.hsize == 1680: 
            self.directory = '/mnt/mmc/images/charmr/1264x1680/'
        
        self.wfm_disp = { # we should make this a json file to import so it's easily accessible for changes
            'init': 0,
            'text': 3,
            'fast': 4,
            'strd': 2,
            'best': 5, 
            'DU': 1,
            'DUIN': 6,
            'DUOUT': 7,
            }

    def display_brightness(self):
        self.load_area(self.directory + 'label_brightness.pgm', (616,1718))

    def display_temp(self):
        self.load_area(self.directory + 'label_temperature.pgm', (616,1718))

    '''
    Clears the current screen. Takes one of 5 arguments: 'slideshow', 'full', 'fast', 'strd', 'best', or 'none'
    'slideshow': Manages clearing before the current slide in the slideshow, based on user specifications and recommendations
    The other arguments can be user designated in the program or read from the charmr_module
    Auto flash is set to 'norm' (standard display white flash)
    ''' 
    def clear(self, flsh, disp = 'full'):

        if  flsh == 'full': 
            self.load(self.directory + 'white240.pgm'); 
            subprocess.call("bs_disp_" + disp + " 0", shell = True)    
        elif flsh == 'text': 
            self.load(self.directory + 'white240.pgm'); 
            subprocess.call("bs_disp_" + disp + " 3", shell = True)
        elif flsh == 'fast':   
            self.load(self.directory + 'white240.pgm'); 
            subprocess.call("bs_disp_" + disp + " 4", shell = True)
        elif flsh == 'strd': 
            self.load(self.directory + 'white240.pgm'); 
            subprocess.call("bs_disp_" + disp + " 2", shell = True)
        elif flsh == 'best': 
            self.load(self.directory + 'white240.pgm'); 
            subprocess.call("bs_disp_" + disp + " 5", shell = True)
        elif flsh == 'none': pass


    '''
    The screen displayed on launch. Currently, it is the startup image
    '''
    def display_startup(self):
        
        self.clear('init')
    
        self.clear('best')
    
        self.load(cm.startup.file, cm.startup.rot)

        self.display(cm.startup)
    
    '''
    Changes the menu option that is displayed with a chekcmark, called when a user selects a new option

    ARGUMENTS:
    menu: BaseMenu (the menu the user is currently working with)
    disp (optional): bool (whether or not the checkmark will be displayed)
    '''
    def change_checkmarked_option(self, locations, cur_check, disp=True):
        print("Loading new checkmark\n\n")
        if type(locations[0]) == int:
            if cur_check == 1:
                subprocess.call('bs_load_img_area ' + str(cm.check.rot) + " " + str(locations[0]) + " " + str(locations[1]) + " " + cm.check.file, shell = True)
            else:     
                subprocess.call('bs_load_img_area ' + str(cm.uncheck.rot) + " " + str(locations[0]) + " " + str(locations[1]) + " " + cm.uncheck.file, shell = True)  
            if disp: 
                self.display(cm.check, 'part')
            return

        for i in range(len(locations)): # Finds the checked value (1) and makes all other buttons unchecked (0)
            print(i)
            if i != cur_check:
                print("Not checked")
                subprocess.call('bs_load_img_area ' + str(cm.uncheck.rot) + " " + str(locations[i][0]) + " " + str(locations[i][1]) + " " + cm.uncheck.file, shell = True)
            else:
                print("checked")
                subprocess.call('bs_load_img_area ' + str(cm.check.rot) + " " + str(locations[i][0]) + " " + str(locations[i][1]) + " " + cm.check.file, shell = True)  
        if disp: 
            self.display(cm.check, wfm = cm.check.wfm, method = 'part')

    '''
    Manages slide transitions and the display styles
    The 'brains' of what type of transition, wfm, etc. should occur
        
    direction: Takes one of four arguments: int, 'next', or 'back', or 'remain'
        int:      Integer number, moves to slide number int
        'next':   Moves on to the next slide in the slideshow
        'back':   Moves back one slide in the slideshow
        'remain': Stays on the current slide
    style: different style slide transitions
        'swipe':      Creates a page-turn-like display from either left to right or right to left
        'center'out': Displays images center-out radially. Must be a part-display, so a CLEAR() function is automatically integrated in
        None:         Normal display
    '''
    def change_slide(self, slideshow, direction,  style = None): #, style = None): # Moves to next slide of slideshow

        cm_info = slideshow.cm_slideshow

        if type(direction) == int: 
            slideshow.cur_slide = direction # direction can be 'back' or 'next', or an integer will change to that slide number   
            return
        elif direction == "next": 
            slideshow.cur_slide += 1; prev = -1; swipe = 'left'
            if slideshow.cur_slide >= slideshow.length: 
                self.clear("full"); 
                self.display_main_menu()
            self.load(slideshow)
        elif direction == "back":
            slideshow.cur_slide -= 1; prev = 1; swipe = 'right'
            if slideshow.cur_slide < 0: slideshow.cur_slide = 0 # If already on first slide, remain therels.touch_zone
            self.load(slideshow)
        elif direction == "back two":
            slideshow.cur_slide -= 2; prev = 2; swipe = 'right'
            if slideshow.cur_slide < 0: slideshow.cur_slide = 0 # If already on first slide, remain there
            self.load(slideshow)    
        elif direction == "remain": 
            if style == None:
                self.display(cm_info, cm_info.disp[slideshow.cur_slide])            
            if style == "swipe":
                self.display_swipe(slideshow, "left", self.wfm_disp['text'])    
            if style == 'center-out':
                self.display_center_out(slideshow, cm_info.wfm[slideshow.cur_slide])
            return
        # --------------------------------------------------------------------------- 
        if cm_info.style == "swipe":    
            if   cm_info.wfm[slideshow.cur_slide] == self.wfm_disp['best']: # Best color
                if   cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['best']: self.display_swipe(slideshow, swipe, 13)
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['fast']: self.display_swipe(slideshow, swipe, 13, 'clear')
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['text']: self.display_swipe(slideshow, swipe, 13, 'clear', self.wfm_disp['text'])
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['strd']: self.display_swipe(slideshow, swipe, 13, 'clear')
                else: self.display_swipe(slideshow, "left", 13)                      
            elif cm_info.wfm[slideshow.cur_slide] == self.wfm_disp['fast']: # Fast color
                if   cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['best']: self.display_swipe(slideshow, swipe, 13, 'clear')
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['fast']: self.display_swipe(slideshow, swipe, 13)  
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['text']: self.display(slideshow, self.wfm_disp['fast'], slideshow.disp[slideshow.cur_slide])
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['strd']: self.display_swipe(slideshow, swipe, 13)
                else: self.display_swipe(slideshow, "left", 13)
            elif cm_info.wfm[slideshow.cur_slide] == self.wfm_disp['text']: # Text
                if   cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['best']: self.display_swipe(slideshow, swipe, 13, 'clear only')
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['fast']: self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide])   
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['text']: self.display(slideshow, self.wfm_disp['text'], slideshow.disp[slideshow.cur_slide]) 
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['strd']: self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide]) 
                else: self.display_swipe(slideshow, "left", 13)            
            elif cm_info.wfm[slideshow.cur_slide] == self.wfm_disp['strd']: # Strd color
                if   cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['best']: self.display_swipe(slideshow, swipe, 13, 'clear')
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['fast']: self.display_swipe(slideshow, swipe, 13)  
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['text']: self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide])
                elif cm_info.wfm[slideshow.cur_slide+prev] == self.wfm_disp['strd']: self.display_swipe(slideshow, swipe, 13)
                else: self.display_swipe(slideshow, "left", 13)                   
        # ------------------------------------------------------ 
        elif cm_info.style == "center-out":
            self.display_center_out(slideshow, cm_info.wfm[slideshow.cur_slide])
        # ------------------------------------------------------       
        else: # NORMAL DISPLAY STYLE
            if   slideshow.wfm[slideshow.cur_slide] == self.wfm_disp['best']: # Best color
                if   slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['best']: self.display(slideshow, self.wfm_disp['best'], slideshow.disp[slideshow.cur_slide])
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['fast']: self.clear('best'); self.display(slideshow, self.wfm_disp['best'], slideshow.disp[slideshow.cur_slide])
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['text']: self.clear('text'); self.display(slideshow, self.wfm_disp['best'], slideshow.disp[slideshow.cur_slide])
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['strd']: self.clear('best'); self.display(slideshow, self.wfm_disp['best'], slideshow.disp[slideshow.cur_slide])
                else: self.display_swipe(slideshow, "right", 13)                      
            elif slideshow.wfm[slideshow.cur_slide] == self.wfm_disp['fast']: # Fast color
                if   slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['best']: self.clear('best'); self.display(slideshow, self.wfm_disp['fast'], slideshow.disp[slideshow.cur_slide])
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['fast']: self.display(slideshow, self.wfm_disp['fast'], slideshow.disp[slideshow.cur_slide])  
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['text']: self.display(slideshow, self.wfm_disp['fast'], slideshow.disp[slideshow.cur_slide])
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['strd']: self.display(slideshow, self.wfm_disp['fast'], 13)
                else: self.display_swipe(slideshow, "right", 13)
            elif slideshow.wfm[slideshow.cur_slide] == self.wfm_disp['text']: # Text
                if   slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['best']: self.clear('best'); self.display(slideshow, self.wfm_disp['text'], slideshow.disp[slideshow.cur_slide])
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['fast']: self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide])   
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['text']: self.display(slideshow, self.wfm_disp['text'], slideshow.disp[slideshow.cur_slide]) 
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['strd']: self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide]) 
                else: self.display(slideshow, slideshow.disp[slideshow.cur_slide])           
            elif slideshow.wfm[slideshow.cur_slide] == self.wfm_disp['strd']: # Strd color
                if   slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['best']: self.clear('best'); self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide])
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['fast']: self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide])  
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['text']: self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide])
                elif slideshow.wfm[slideshow.cur_slide+prev] == self.wfm_disp['strd']: self.display(slideshow, self.wfm_disp['strd'], slideshow.disp[slideshow.cur_slide])           


    '''
    Displays the images across the screen in the direction defined by the user.
    The delay is the time in ms between each frame display on screen (16 frames set by fpga limit).
        'direction': 'left' or 'right'
        delay: any integer > 12
    I have to call CMDER in order to execute this because that's the only way to get frames displaying simultaneously on the screen
    *Only can be used when calling a slide from the charmr module. 
    *It find the slide to display using the current slideshow and slide number N
    Three display styles are available:
        'regular': the image display swipes across the screen
        'clear': a white clear swipes accross the screen immediately followed by an image swipe
        'clear only': a white clear swipes accross the screen but the following image is displayed normally
    The user can choose the wfm# used in clearing the image by entering a wfm# integer for 'clear_WFM'
    '''
    def display_swipe(self, slideshow, direction, delay, style = 'reg', clear_WFM = None, image_WFM = None):

        #global N, i, iwidth, j, jwidth

        N = slideshow.cur_slide
        rot = slideshow.rot[N]
        clear_Detect = 0

        cm_info = slideshow.cm_slideshow
        
        if isinstance(clear_WFM, int): pass
        elif self.auto[N] == 'yes':  clear_WFM = self.wfm_disp['best'] # Auto
        elif self.flsh[N] == 'full': clear_WFM = self.wfm_disp['init']
        elif self.flsh[N] == 'fast': clear_WFM = self.wfm_disp['fast']
        elif self.self[N] == 'strd': clear_WFM = self.wfm_disp['strd']
        elif self.flsh[N] == 'best': clear_WFM = self.wfm_disp['best']
            
        if clear_WFM == self.wfm_disp['init']: wfm_Time = 3541-100 # Assume it takes 100ms to load the image
        if clear_WFM == self.wfm_disp['strd']: wfm_Time = 1024-100
        if clear_WFM == self.wfm_disp['text']: wfm_Time = 377  # This is a fast enough flash, don't need to reduce the time
        if clear_WFM == self.wfm_disp['fast']: wfm_Time = 518 -100
        if clear_WFM == self.wfm_disp['best']: wfm_Time = 1518-100
        
        if isinstance(image_WFM, type(None)):
            image_WFM = cm_info.wfm[N]
        
        if os.path.exists("swipe.txt"):
            os.remove("swipe.txt")
        with open("swipe.txt", "w") as f:
            f.write("SET_ROT " + str(rot*90) + " \n")
            if style == 'clear' or style == 'clear only':
                f.write("LD_IMG " + self.directory + "white240.pgm\n")
            i = 0; j = 0 # i: image, j: clear
            i_iteration = 1
            width = int(math.ceil(1440/16))
            iwidth = width; jwidth = width # jwidth for image, iwidth for clear
            
            if rot == 2 or rot == 3: 
                if   direction == 'right': direction = 'left'
                elif direction == 'left': direction = 'right'
            
            def UPD_AREA_CLEAR(rot, direction):
                if   rot == 1 or rot == 3:  
                    if   direction == "right":
                        f.write("UPD_FULL_AREA " + str(clear_WFM) + " " + str(i) + " 0 " + str(iwidth) + " 1920 " + '\n')
                    elif direction == "left":
                        f.write("UPD_FULL_AREA " + str(clear_WFM) + " " + str(cm.wsize - iwidth - i) + " 0 " + str(iwidth) + " 1920 " + '\n')
                elif rot == 0 or rot == 2:
                    if direction == "right":
                        f.write("UPD_FULL_AREA " + str(clear_WFM) + " 0 " + str(i) + " 1920 " + str(iwidth) + '\n')
                    if direction == "left":
                        f.write("UPD_FULL_AREA " + str(clear_WFM) + " 0 " + str(cm.wsize - iwidth - i) + " 1920 " + str(iwidth) + '\n')
                            
            def UPD_AREA_IMAGE(rot, direction):
                if   rot == 1 or rot == 3:  
                    if   direction == "right":
                        f.write("UPD_FULL_AREA " + str(image_WFM) + " " + str(j) + " 0 " + str(jwidth) + " 1920 " + '\n') 
                    elif direction == "left":
                        f.write("UPD_FULL_AREA " + str(image_WFM) + " " + str(cm.wsize - jwidth - j) + " 0 " + str(jwidth) + " 1920 " + '\n') 
                elif rot == 0 or rot == 2:
                    if direction == "right":
                        f.write("UPD_FULL_AREA " + str(image_WFM) + " 0 " + str(j) + " 1920 " + str(jwidth) + '\n')
                    if direction == "left":
                        f.write("UPD_FULL_AREA " + str(image_WFM) + " 0 " + str(cm.wsize - jwidth - j) + " 1920 " + str(jwidth) + '\n')                     
            
            if style == 'clear':
                while i < cm.wsize or j < cm.wsize:
                    if cm.wsize - i < iwidth: iwidth = cm.wsize - i
                    if i < cm.wsize: # Starts swiping the white screen
                        UPD_AREA_CLEAR(rot, direction)
                        f.write("SLEEP " + str(delay) + "\n")
                        i += iwidth
                        i_iteration += 1
                        clear_Detect += delay                   
                    if i == cm.wsize: # If white swipe commands have sent and waiting for upload to finish, waits the remaining time to start next image
                        delay1 = delay*i_iteration - clear_Detect; delay2 = wfm_Time - clear_Detect
                        clear_Detect += max(delay1, delay2)
                        f.write("SLEEP " + str(clear_Detect) + "\n")  
                        f.write("LD_IMG " + slideshow.path + slideshow.file[N] + "\n")
                        i+=1                       
                    if clear_Detect >= (delay*i_iteration)-1 or clear_Detect >= wfm_Time-1: # Starts displaying the image when the white is finished
                        UPD_AREA_IMAGE(rot, direction)
                        f.write("SLEEP " + str(delay) + "\n")
                        j += jwidth
                        
            elif style == 'clear only':
                while i < cm.wsize:
                    if cm.wsize - i < iwidth: iwidth = cm.wsize - i
                    if i < cm.wsize: # Starts swiping the white screen
                        UPD_AREA_CLEAR(rot, direction)
                        f.write("SLEEP " + str(delay) + "\n")
                        i += iwidth
                        i_iteration += 1
                        clear_Detect += delay                   
                    if i == cm.wsize: # If white swipe commands have sent and waiting for upload to finish, waits the remaining time to start next image
                        delay1 = delay*i_iteration - clear_Detect; delay2 = wfm_Time - clear_Detect
                        clear_Detect += max(delay1, delay2)
                        f.write("SLEEP " + str(clear_Detect) + "\n")  
                        f.write("LD_IMG " + slideshow.path + slideshow.file[N] + "\n")
                        f.write("UPD_FULL " + str(slideshow.wfm[N]))
                        i+=1 
            
            else:
                f.write("LD_IMG " + cm_info.path + cm_info.file[N] + "\n")
                while j < cm.wsize:
                    if cm.wsize - j < jwidth: jwidth = cm.wsize - i
                    UPD_AREA_IMAGE(rot, direction)
                    f.write("SLEEP " + str(delay) + "\n")
                    j += jwidth
                            
        subprocess.call("SET_SPECIFIC_TEMP=25 PWRDOWN_DELAY=10 /mnt/mmc/api/tools/cmder /mnt/mmc/api/tools/swipe.txt", shell=True)

    def display_center_out(self, slideshow, wfm):

        N = slideshow.cur_slide

        rot = 1
        delay = 13
        clear_Detect = 0
        
        if   self.auto[N] == 'yes': # Auto flush defaults to normal clear wfm
            wfm_Time = 518 +200
            clear_WFM = self.wfm_disp['best']
        if   self.flsh[N] == 'full': 
            wfm_Time = 3541 +200
            clear_WFM = self.wfm_disp['init']
        elif self.flsh[N] == 'fast': 
            wfm_Time = 377 +200  
            clear_WFM = self.wfm_disp['text']
        elif self.flsh[N] == 'strd': 
            wfm_Time = 518 +200  
            clear_WFM = self.wfm_disp['fast']
        elif self.flsh[N] == 'best': 
            wfm_Time = 1518 +200 
            clear_WFM = self.wfm_disp['best']
            
        if os.path.exists("swipe.txt"): # Checks if tiler_module.py exists, deletes if it does. Then writes the module file.
            os.remove("swipe.txt")
        with open("swipe.txt", "w") as f:
            f.write("LD_IMG " + self.directory + "white240.pgm\n")
            n = 0; m = 0 # blank iteration count, analagous to i
            f.write("SET_ROT " + str(rot*90) + " \n")
            iwidth = 0; iheight = 0
            jwidth = 0; jheight = 0
            
            while iwidth < cm.wsize or jwidth < cm.wsize:
                
                if iwidth < cm.wsize:
                    iwidth = int(math.ceil(cm.wsize/16)*(n+1))
                    iheight = int(math.ceil(cm.hsize/16)*(n+1))
                    ixstart = int((cm.wsize - iwidth)/2)
                    iystart = int((cm.hsize - iheight)/2)
                    if iwidth > cm.wsize: iwidth = cm.wsize
                    if iheight > cm.hsize: iheight = cm.hsize
                    f.write("UPD_PART_AREA " + str(clear_WFM) + " " + str(ixstart) + " " + str(iystart) + " " + str(iwidth) + " " + str(iheight) + '\n')
                    f.write("SLEEP " + str(delay) + "\n")
                    n += 1 
                    clear_Detect += delay
                    
                if iwidth == cm.wsize: # Once the clear is finished, move on with writing the remaining wait time
                    delay1 = delay*n - clear_Detect; delay2 = wfm_Time - clear_Detect
                    clear_Detect += max(delay1, delay2)
                    f.write("SLEEP " + str(clear_Detect) + "\n")
                    f.write("LD_IMG " + slideshow.path + slideshow.file[N] + "\n")
                    iwidth += 1
                    
                if clear_Detect >= wfm_Time-1: # Starts displaying the image when the white is finished
                    jwidth = int(math.ceil(cm.wsize/16)*(m+1))
                    jheight = int(math.ceil(cm.hsize/16)*(m+1))
                    jxstart = int((cm.wsize - jwidth)/2)
                    jystart = int((cm.hsize - jheight)/2)
                    if jwidth > cm.wsize: jwidth = cm.wsize
                    if jheight > cm.hsize: jheight = cm.hsize
                    f.write("UPD_PART_AREA 5 " + str(jxstart) + " " + str(jystart) + " " + str(jwidth) + " " + str(jheight) + '\n')
                    f.write("SLEEP " + str(delay) + "\n")
                    m += 1
                    
        subprocess.call("SET_SPECIFIC_TEMP=25 PWRDOWN_DELAY=10 /mnt/mmc/api/tools/cmder /mnt/mmc/api/tools/swipe.txt", shell=True)


    '''
    The main menu screen
    '''
    def display_main_menu(self):
        self.clear("text")

        self.load(self.directory + "tmp_mainmenu.pgm", 1)  
        #self.display_clock("load")
        # BUTTONS(main, 'no display')      
        self.load_area(cm.banner.file, (0,80), cm.banner.rot)
        
        # if os.path.exists("tmp.txt"): 
        #     os.remove("tmp.txt")
        with open("tmp.txt", "w") as f: # Need cmder code to get all the main menu regions to display at once
            f.write("SET_ROT 90 \n")
            f.write("UPD_PART_AREA " + str(self.wfm_disp['text']))
            f.write(" 0 " + str(int(math.floor(.00000*cm.hsize))) + " " + str(cm.wsize) + " " + str(int(math.floor(.04115*cm.hsize))) + "\n") # HEADER
            f.write("UPD_PART_AREA " + str(self.wfm_disp['text']))
            f.write(" 0 " + str(int(math.floor(.15625*cm.hsize))) + " " + str(cm.wsize) + " " + str(int(math.floor(.73750*cm.hsize))) + "\n") # BODY
            f.write("UPD_PART_AREA " + str(self.wfm_disp['strd']))
            f.write(" 0 " + str(int(math.floor(.89375*cm.hsize))) + " " + str(cm.wsize) + " " + str(int(math.floor(.10625*cm.hsize))) + "\n") # FOOTER
            f.write("UPD_PART_AREA " + str(cm.banner.wfm))
            f.write(" 0 " + str(int(math.floor(.04167*cm.hsize))) + " " + str(cm.wsize) + " " + str(int(math.floor(.11458*cm.hsize))) + "\n") # BANNER 
        subprocess.call("/mnt/mmc/api/tools/cmder /mnt/mmc/api/tools/tmp.txt", shell=True)

    '''
    Loads the given image.

    ARGUMENTS
    img: IMAGE (the image being loaded from the charmr module file)
    rot (optional): int (rotation of image)
    '''
    def load(self, img, rot=1):
        self.rotation_Current = rot
        print('bs_load_img ' + str(rot) + ' ' + str(img))
        #os.system('bs_load_img ' + str(rot) + ' ' + str(img))
        subprocess.call('bs_load_img ' + str(rot) + ' ' + str(img), shell = True, close_fds=True)
        print("called")

    '''
    Loads only a specified area of the screen with the given image.

    ARGUMENTS
    img: IMAGE (the image being loaded from the charmr module file)
    rot: int (rotation of image)
    pos: list(int, int) (where on the screen the image should be loaded)
    '''
    def load_area(self, img, pos, rot=1):
        X = ' '; SSX = cm.hsize; SSY = cm.wsize
        if   str(rot) == '1':
            subprocess.call('bs_load_img_area ' + str(rot) +X+ str(pos[0]) +X+ str(pos[1]) +X+ str(img), shell = True)
        elif str(rot) == '0':
            subprocess.call('bs_load_img_area ' + str(rot) +X+ str(SSY - pos[1]) +X+ str(pos[0]) +X+ str(img), shell = True)
        elif str(rot) == '2':
            subprocess.call('bs_load_img_area ' + str(rot) +X+ str(pos[1]) +X+ str(SSX - pos[0]) +X+ str(img), shell = True)
        elif str(rot) == '3': 
            subprocess.call('bs_load_img_area ' + str(rot) + ' ' + str(SSX - pos[0]) + ' ' + str(SSY - pos[1]) + ' ' + str(img), shell = True)

    '''
    Displays the given image.

    ARGUMENTS
    img: IMAGE (the image being displayed from the charmr module file)
    method (optional): str (display type - cmder specification)
    '''
    def display(self, slideshow, wfm=2, method = 'full'):
        if isinstance(slideshow.cm_slideshow, cm.IMAGE):
            if isinstance(slideshow.cm_slideshow.wfm, list):
                wfm = slideshow.cm_slideshow.wfm[slideshow.cur_slide]
            else:
                wfm = slideshow.cm_slideshow.wfm   
            utils.command('bs_disp_' + method + ' ' + str(wfm), 'sub')
        else: 
            utils.command('bs_disp_' + method + ' ' + str(wfm), 'sub')

    '''
    Turns the text string into an image file, then saves the image file and returns the filepath

    ARGUMENTS
    text_String: str (the text to be converted to an image)
    font: str (the font of the text)
    font_Size: str (the text size)
    img_Blank: img (the blank image to write to)
    offset (optional): list(int, int) (the text offset in the image)

    RETURNS
    tmp: str (the filepath of the image created)
    '''
    def text_to_image(self, text_String, font, font_Size, img_Blank, offset = (10, 10)):
        img = Image.open(img_Blank)
        I1 = ImageDraw.Draw(img)
        I1.fontmode = "1"
        myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/" + font, font_Size)
        I1.text(offset, text_String, font=myFont, fill=0)
        tmp = self.directory + "tmp.pgm"    
        img.save(tmp)
        return tmp  

    '''
    Loads and displays the current time
    '''
    def display_clock(self, arg = "check"):
        
        current_time = utils.clock()

        if   cm.wsize == 1440: time_Written = self.text_to_image(current_time[0], "Sans_Monofonto.otf", 52, self.directory + "blank_time.pgm", (10,7))
        elif cm.wsize == 1264: time_Written = self.text_to_image(current_time[0], "Sans_Monofonto.otf", 42, self.directory + "blank_time.pgm", (0,10))
        
        if current_time[1] < 10:
            self.load_area(time_Written, cm.area.clock[0])
        else: 
            self.load_area(time_Written, cm.area.clock[1])
        if arg != "load":
            self.display(self.wfm_disp['text'], "part")

    def display_sketch_app(self):
        #def F_sketch(arg = None):
        """
        Clicking the sketch button during a paused slideshow calls acepsketch
        The draw function only works if the image is loaded as 'fast', highlighter as 'DU'
        This means for color images, any non-fast rendered images must be color index converted using color_convert()
        """
        
        if arg == 'app':
            self.clear('best')
            os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 
            # device.sect = None
            # F_main()
            return
        
    def display_pause_sketch_app(self, slideshow):
        
        self.load(slideshow) # Reload the slideshow slide #N
        self.display_area(slideshow, (0,80), (1440,1715)) #Redisplay the background slideshow     

    
    def display_pause(self, slideshow):

        N = slideshow.cur_slide
        cm_info = slideshow.cm_slideshow
        #def F_pause(): # Pauses the slideshow, pops up settings, and flashes an options banner
        """
        Opens a pause screen and waits for user input.
        From here user can see slide movement options, get to the settings menu, open brightness options, and open ACeP draw
        """
        # ----- LOADING CONTENT ------------
        # If exit button pressed on the pause menu screen:
        if device.sect == 'psettings': # coming back from psettings menu
            self.load(slideshow) # Reload the slideshow slide #N
            self.display(slideshow, 'part') #Redisplay the background slideshow     

        
        if cm_info.wfm[N] == 3:
            self.load(self.directory + "pause_highlight2.pgm")
        else: 
            self.load(self.directory + "pause_draw2.pgm")
        self.display_clock("load")
        tmp = self.text_to_image(str(N + 1) + '/' + str(len(slideshow.file)), 'Serif_DejaVu.ttf', 50, self.directory + "blank_slidenumber_pause.pgm")   
        self.load_area(tmp, (3,0))

        if   device.slide == 'bght':
            self.load_area(self.directory + 'label_brightness.pgm', (616,1718))   
            BUTTONS(bght, 'no display', self.directory + "check_brightness2.pgm", self.directory + "uncheck_brightness2.pgm") 
        elif device.slide == 'temp':
            self.load_area(self.directory + 'label_temperature.pgm', (616,1718))   
            BUTTONS(temp, 'no display', self.directory + "check_brightness2.pgm", self.directory + "uncheck_brightness2.pgm") 
        
        # ----- DISPLAYING PAUSE CONTENT ------------
        if slideshow.wfm[N] == wfm_Disp.best: 
            self.display(wfm_Disp.best, 'full') 
        if slideshow.wfm[N] == wfm_Disp.fast: 
            self.display(wfm_Disp.fast, 'full')  
        if slideshow.wfm[N] == wfm_Disp.text:
            self.display(wfm_Disp.strd, 'full')
        if slideshow.wfm[N] == wfm_Disp.strd: 
            self.display(wfm_Disp.strd, 'full')
            
        img = Image.open(slideshow.path + slideshow.file[N]) # save the current slide to sketch directory for loading
        tmp = "/mnt/mmc/application/sketch/tmp.pgm"    
        img.save(tmp)       

            
    def window_header(self, text):
        header = self.text_to_image(text, 'Sans_ZagReg.otf', 60, self.directory + "blank_window_header.pgm")
        self.load_area(header, (250,368)) 

    def display_main_settings_menu(self):
        #import Controller.get_input as get_input
        
        items = ['Go to slide', 
                 'Wfm mode #s',
                 'Demo mode',
                 'Restart']
  
        # ----- LOADING CONTENT ------------
        self.load(self.directory + "tmp_mainsettingsmenu.pgm")  
        self.window_header('Main settings')
        self.change_checkmarked_option('mset')
        
        # ----- WAITING FOR INPUT ----------
        while True:  
            basemenu.buttons(user_input)
            user_input = get_input()
            # ----- DISPLAYING BUTTONS AND OTHER CONTENT IF NOT YET LOADED

        
            if touch:# Touch takes priority over button, so listed before 'if select:'   
                command = MENU_TOUCH(mset) 
                if   command == 1: command = F_gotoslide()
                elif command == 2: command = F_wfm()
                elif command == 3: COMMAND("kill python charmr.py; python charmr_demo.py", "sub")
                elif command == 4: COMMAND("kill python charmr.py; python charmr.py", "sub")
                
                elif TOUCH_ZONE(TOUCH_DICT['slider']): # BRIGHTNESS/TEMP SLIDER
                    if   device.slide == 'bght': F_brightness()
                    elif device.slide == 'temp': F_temperature()
                elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS('display')
                elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE('display')      
                elif TOUCH_ZONE(TOUCH_DICT['settings_button']): F_main()
                elif TOUCH_ZONE(TOUCH_DICT['exit_button']): F_main()
                else: F_main()
                
            elif select:
                if   mset.check == 0: command = F_gotoslide()
                elif mset.check == 1: command = F_wfm()
                elif mset.check == 2: COMMAND("kill python charmr.p7; python charmr_demo.py", "sub")
                elif mset.check == 3: COMMAND("kill python charmr.py; python mcharmr.py", "sub") 
                
            else: command = None
            
            if   command == 'exit': F_main()
            elif command == 'back': F_msettings()

    def display_pausesettings(self):
        pass
    
    #     self.clear("best")

    #     if slide_number >= 0:
    #         self.change_slide(slide_number) 
    #     else: slideshow.cur_slide = slide_number
    #     direction = "next"; style = slideshow.cm_slideshow.styl

    #     auto_slideshow = threading.Thread(target=auto_run, args=(self, slideshow))

    #     auto_slideshow.run()

    # def auto_run(self, slideshow):
    #     while slideshow.cur_slide < slideshow.length:
    #         utils.wait(slideshow.slide_timer())
            
    #         if slideshow.cm_slideshow.styl == 'center-out':
    #             self.change_slide("next", "center-out")
    #         else: 
    #             self.change_slide("swipe", "center-out")