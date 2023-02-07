import charmr_module as cm
from color_convert import *
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


class MENU_CHECK: #Each page will an option for button layouts and the current selected button
    def __init__(self, locations, check): 
        self.locations = locations
        self.check = check
        
class MENUS: # 
    def __init__(self, main, mset, pset, temp, bght, disp, flsh, auto, wfmm, wfms, rot, sshw):
        self.main = main
        self.mset = mset
        self.pset = pset
        self.temp = temp
        self.bght = bght
        self.disp = disp
        self.flsh = flsh
        self.auto = auto
        self.wfmm = wfmm # Waveform menu from main menu
        self.wfms = wfms # Waveform menu from slideshow settings
        self.rot  = rot
        self.sshw = sshw    

class SNAKE_ATTRIBUTES:
    def __init__(self, food, body, nmbr):
        self.food = food
        self.body = body
        self.nmbr = nmbr
        
class DEVICE: # Lower-level system monitoring
    def __init__(self, time, wifi, btth, batt, proc, sect, slide):
        self.time = time
        self.wifi = wifi
        self.btth = btth # bluetooth
        self.batt = batt
        self.proc = proc # process id  
        self.sect = sect # Keeps track of where we are in the software. None (startingup), 'main', 'slideshow', 'pause', 'psettings'
        self.slide = slide # brightness/temperature scroll at bottom of screen. Either 'bght' or 'temp'
        
class WFM_DISPLAYS:
    def __init__(self, init, text, fast, strd, best, DU, DUIN, DUOUT):
        self.init = init
        self.text = text
        self.fast = fast
        self.strd = strd
        self.best = best
        self.DU = DU
        self.DUIN = DUIN
        self.DUOUT = DUOUT
        
TOUCH_DICT = {
    'brightness_button': [[0,1716], [215,1920]],
    'temperature_button': [[215,1716], [420,1920]],
    'sketch_button': [[.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,1.000*cm.hsize]],
    'settings_button': [[.8507*cm.wsize,.8854*cm.hsize], [1.000*cm.wsize,1.000*cm.hsize]],
    'exit_button': [[.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]],
    'back_button': [[.6736*cm.wsize,.1771*cm.hsize], [.7708*cm.wsize,.2396*cm.hsize]],
    'slider': [[460,1730], [990,1850]]
    }
        
"""
Functions: AURORA(), BUTTONS(), CHANGE_SLIDE(), CHANGE_SLIDESHOW(), CHECK(), CLEAR(), COMMAND(), DISPLAY(), 
    DISPLAY_AREA(), GET_DATA(), GET_INPUT(), GET_SLIDE(), LOAD(), LOAD_AREA(), RELOAD(), REPLACE_DATA(), 
    SKETCH(), TOUCH_ZONE(), WAIT()
    
All screens are treated as functions
The intent here is to have mostly pre-built menus to adjust functionality, and for the user to have minimal interaction with the code

What the user will have to do each time is:
    Upload charmr module data using charmr_constructor.py program
    Reconfigure TOUCH_ZONE() areas for changed button layouts
    Fine-tune image displays

For larger changes to the structure, the code is simplified to make changes simple and intuitive
Deleting buttons or menus are straightforward

If the user wants to upload new menus, all menus MUST be black and white only (or else wfms need to change and speed decreases)

Version features:
    Imports all demo data/info from module (slideshows, menu, etc)
    Simultanous button, touch, and swipe detect
    ACeP sketch w/o highlighter
    ACeP draw w/o highlighter or clear
    Image wfm/rotation change buttons w/ data replacements
    Disp, flsh, auto (smart) flsh buttons w/ data replacements
        Instantaneous data reimporting
    Two synchonized brightness menus
    No global varriables needed calling by user
    Automatically add time to slide equal to wfm display time
    All load locations equated across different rotations
        Everything measured from top left
"""    
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# STARTUP AND MAIN SCREENS :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        
    
def F_main(): # MAIN MENU SCREEN
    CHANGE_SLIDE(0) # Slide resets to zero when sent back to main menu
       
    CLEAR('best')
    device.sect = 'main' # Section now set to the main menu 
    
    LOAD(directory + "tmp_mainmenu.pgm")  
    CLOCK("load")
    BUTTONS(main, 'no display')    
    
    LOAD_AREA(directory + 'label_brightness.pgm', (616,1718))   
    BUTTONS(bght, 'no display', directory + "check_brightness2.pgm", directory + "uncheck_brightness2.pgm")
    device.slide = 'bght'    
    
    LOAD_AREA(cm.banner, (0,80))
    
    if os.path.exists("tmp.txt"): 
        os.remove("tmp.txt")
    with open("tmp.txt", "w") as f: # Need cmder code to get all the main menu regions to display at once
        f.write("SET_ROT 90 \n")
        f.write("UPD_PART_AREA " + str(wfm_Disp.text)) 
        f.write(" 0 " + str(int(math.floor(.00000*cm.hsize))) + " " + str(cm.wsize) + " " + str(int(math.floor(.04115*cm.hsize))) + "\n") # HEADER
        f.write("UPD_PART_AREA " + str(wfm_Disp.text)) 
        f.write(" 0 " + str(int(math.floor(.15625*cm.hsize))) + " " + str(cm.wsize) + " " + str(int(math.floor(.73750*cm.hsize))) + "\n") # BODY
        f.write("UPD_PART_AREA " + str(wfm_Disp.strd))
        f.write(" 0 " + str(int(math.floor(.89375*cm.hsize))) + " " + str(cm.wsize) + " " + str(int(math.floor(.10625*cm.hsize))) + "\n") # FOOTER
        f.write("UPD_PART_AREA " + str(cm.banner.wfm))
        f.write(" 0 " + str(int(math.floor(.04167*cm.hsize))) + " " + str(cm.wsize) + " " + str(int(math.floor(.11458*cm.hsize))) + "\n") # BANNER 
    subprocess.call("/mnt/mmc/api/tools/cmder /mnt/mmc/api/tools/tmp.txt", shell=True)
    
    while True:  
        BUTTONS(main, 'display')
        GET_INPUT() # Wait for user input (touch or buttons)
        
        if touch: # IF SCREEN WAS TOUCHED
            command = MENU_TOUCH(main)
            if   command == 1: APP_SELECTOR(1)
            elif command == 2: APP_SELECTOR(2)
            elif command == 3: APP_SELECTOR(3)
            elif command == 4: APP_SELECTOR(4)               
            elif command == 5: APP_SELECTOR(5)     
            
            elif TOUCH_ZONE(TOUCH_DICT['slider']): 
                if   device.slide == 'bght': F_brightness()
                elif device.slide == 'temp': F_temperature()
            elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
            elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE()          
            elif TOUCH_ZONE(TOUCH_DICT['settings_button']): F_msettings() 
                           
        elif select: # IF SELECT BUTTON WAS PRESSED
            if   main.check == 1: APP_SELECTOR(1)
            elif main.check == 2: APP_SELECTOR(2)
            elif main.check == 3: APP_SELECTOR(3)   
            elif main.check == 4: APP_SELECTOR(4)    
            elif main.check == 5: APP_SELECTOR(5)
        
def F_msettings(): # MAIN MENU SETTINGS
    # ----- LOADING CONTENT ------------
    LOAD(directory + "tmp_msettings.pgm")  
    WINDOW_HEADER('Main settings')
    
    # ----- WAITING FOR INPUT ----------
    while True:  
        # ----- DISPLAYING BUTTONS AND OTHER CONTENT IF NOT YET LOADED
        BUTTONS(mset, 'display') 
        GET_INPUT()
    
        if touch:# Touch takes priority over button, so listed before 'if select:'   
            command = MENU_TOUCH(mset) 
            if   command == 0: command = F_gotoslide()
            elif command == 1: command = F_wfm()
            elif command == 2: COMMAND("kill python charmr2.py; python mosaic14_customer.py", "sub")
            elif command == 3: RESTART() 
            elif command == 4: TERMINATE()
            
            elif TOUCH_ZONE(TOUCH_DICT['slider']): # BRIGHTNESS/TEMP SLIDER
                if   device.slide == 'bght': F_brightness()
                elif device.slide == 'temp': F_temperature()
            elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
            elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE()      
            elif TOUCH_ZONE(TOUCH_DICT['settings_button']): F_main()
            elif TOUCH_ZONE(TOUCH_DICT['exit_button']): F_main()
            else: F_main()
            
        elif select:
            if   mset.check == 0: command = F_gotoslide()
            elif mset.check == 1: command = F_wfm()
            elif mset.check == 2: COMMAND("kill python " + sys.argv[0] + "; python mosaic14_customer.py", "sub")
            elif mset.check == 3: RESTART()  
            
        else: command = None
        
        if   command == 'exit': F_main()
        elif command == 'back': F_msettings()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SLIDESHOW MANAGEMENT AND SLIDESHOW PAUSE/MENU ::::::::::::::::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def F_slideshow(slideshow_Number, slide_Number = -1):
    global N
    device.sect = 'slideshow'
    CLEAR("best")
    CHANGE_SLIDESHOW(slideshow_Number)
    if slide_Number >= 0:
        CHANGE_SLIDE(slide_Number) 
    else: N = slide_Number
    direction = "next"; style = slideshow.styl

    while N < len(slideshow.file):
        CHANGE_SLIDE(direction, style) # LOADS AND DISPLAYS SLIDE
        SLIDE_TIMER()
        # if    slideshow.styl == 'reader': GET_INPUT('swipe') # 'reader' style has no timer
        # else: SLIDE_TIMER() # Passes each slide after user-defined time
        if  type(touch) == list: 
            F_pause()
            direction = 'remain'
            CLEAR("strd")# Tap touch returns list value
        elif type(touch) == str: # Swipe touch returns string value
            if touch == "swipe left":  
                direction = "next"; style = "swipe"
            if touch == "swipe right":
                direction = "back"; style = "swipe"
            if touch == "swipe down":
                F_main()
            if touch == "swipe up":
                F_pause()
        elif button:
            if   button == 'enter': F_pause()
            elif button == 'up':   direction = "next"; style = slideshow.styl
            elif button == 'down': direction = "back"; style = slideshow.styl
        else: 
            direction = "next"      
            if slideshow.styl == 'center-out': style = 'center-out'
            else: style = "swipe" # Default is to progress to next slide if there was no input
        
#-----------------------------------------------------------------------------------------------
#------ PAUSE SCREEN ---------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------- 

def F_pause(): # Pauses the slideshow, pops up settings, and flashes an options banner
    """
    Opens a pause screen and waits for user input.
    From here user can see slide movement options, get to the settings menu, open brightness options, and open ACeP draw
    """
    # ----- LOADING CONTENT ------------
    # If exit button pressed on the pause menu screen:
    if device.sect == 'psettings': # coming back from psettings menu
        LOAD(slideshow) # Reload the slideshow slide #N
        DISPLAY(slideshow, 'part') #Redisplay the background slideshow     
    device.sect = 'pause'
    
    if slideshow.wfm[N] == 3:
        LOAD(directory + "pause_highlight2.pgm")
    else: 
        LOAD(directory + "pause_draw2.pgm")
    CLOCK("load")
    tmp = TEXT_TO_IMAGE(str(N + 1) + '/' + str(len(slideshow.file)), 'Serif_DejaVu.ttf', 50, directory + "blank_slidenumber_pause.pgm")   
    LOAD_AREA(tmp, (3,0))

    if   device.slide == 'bght':
        LOAD_AREA(directory + 'label_brightness.pgm', (616,1718))   
        BUTTONS(bght, 'no display', directory + "check_brightness2.pgm", directory + "uncheck_brightness2.pgm") 
    elif device.slide == 'temp':
        LOAD_AREA(directory + 'label_temperature.pgm', (616,1718))   
        BUTTONS(temp, 'no display', directory + "check_brightness2.pgm", directory + "uncheck_brightness2.pgm") 
    
    # ----- DISPLAYING PAUSE CONTENT ------------
    if slideshow.wfm[N] == wfm_Disp.best: 
        DISPLAY(wfm_Disp.best, 'full') 
    if slideshow.wfm[N] == wfm_Disp.fast: 
        DISPLAY(wfm_Disp.fast, 'full')  
    if slideshow.wfm[N] == wfm_Disp.text:
        DISPLAY(wfm_Disp.strd, 'full')
    if slideshow.wfm[N] == wfm_Disp.strd: 
        DISPLAY(wfm_Disp.strd, 'full')
        
    img = Image.open(slideshow.path + slideshow.file[N]) # save the current slide to sketch directory for loading
    tmp = "/mnt/mmc/application/sketch/tmp.pgm"    
    img.save(tmp)       
        
    # ----- WAITING FOR INPUT ----------
    while True:
        GET_INPUT()
        if touch:  
            if   TOUCH_ZONE(TOUCH_DICT['slider']): 
                if   device.slide == 'bght': F_brightness()
                elif device.slide == 'temp': F_temperature()
            elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
            elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE()   
            elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch()
            elif TOUCH_ZONE(TOUCH_DICT['settings_button']): F_psettings()
            else: F_slideshow(menu.sshw.check+1, N-1)
        if button:
            if button == 'enter': break
            if button == 'up':    CHANGE_SLIDE("back", slideshow.styl); break
            if button == 'down':  CHANGE_SLIDE("next", slideshow.styl); break
        
#-----------------------------------------------------------------------------------------------
#------ SLIDESHOW SETTINGS MENU ----------------------------------------------------------------
#----------------------------------------------------------------------------------------------- 
 
def F_psettings(): # MAIN MENU SETTINGS
    # ----- STAY IN MENU UNTIL SPECIFIED -----------
    while True: # Touch and button management for menu screen settings   
    
        # ----- DISPLAYING CONTENT ------------
        # Can come from 'pause' or 'psettings'
        if device.sect == 'pause': # Flash the menu area white so text wfm# can be used in menu
            if slideshow.wfm[N] == wfm_Disp.best:
                LOAD(directory + "menu_reg.pgm") 
                DISPLAY(wfm_Disp.best, 'full') 
            if slideshow.wfm[N] == wfm_Disp.fast: 
                LOAD(directory + "menu_reg.pgm")
                DISPLAY(wfm_Disp.fast, 'full')  
            if slideshow.wfm[N] == wfm_Disp.strd: 
                LOAD(directory + "menu_reg.pgm")
                DISPLAY(wfm_Disp.strd, 'full')
                
        device.sect = 'psettings' # set new device section
        LOAD(directory + "tmp_psettings.pgm")   
        WINDOW_HEADER('Slideshow settings')
        BUTTONS(pset, 'display')
            
        # ----- WAITING FOR INPUT ----------
        GET_INPUT()  
          
        if touch:# Touch takes priority over button, so listed before 'if select:'
            command = MENU_TOUCH(pset) # Checks if the menu options were touched, 'command' returns number if touched
            if   command == 0: command = F_gotoslide()
            elif command == 1: command = F_wfm()
            elif command == 2: command = F_rotation()
            elif command == 3: command = F_dispflsh()
            elif command == 4: command = F_main()
            # ----- other touch zones to be specified
            
            elif TOUCH_ZONE(TOUCH_DICT['slider']): 
                if   device.slide == 'bght': F_brightness()
                elif device.slide == 'temp': F_temperature()
            elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
            elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
            elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch()
            elif TOUCH_ZONE(TOUCH_DICT['settings_button']): F_pause()  # Settings button
            elif TOUCH_ZONE(TOUCH_DICT['exit_button']): F_pause()  # Exit button  
        
        elif select: # if the select button was pressed, looks for the current check location and proceeds with command
            if   pset.check == 0: command = F_gotoslide()
            elif pset.check == 1: command = F_wfm()
            elif pset.check == 2: command = rotation()
            elif pset.check == 3: command = F_dispflsh()
            elif pset.check == 4: command = F_main()
           
        else: command = None
          
        if   command == 'exit': F_pause()
        elif command == 'back': F_psettings()
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# FUNCTIONAL MENUS :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#-----------------------------------------------------------------------------------------------
#------ BRIGHTNESS SCROLL ----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------- 
    
def F_brightness(): 
    # ----- LOADING CONTENT ------------
    b_Check = directory + "check_brightness2.pgm"; b_Uncheck = directory + "uncheck_brightness2.pgm"
        
    if   TOUCH_ZONE([[476,1730], [525,1850]]): CHECK(menu.bght, 0, 'display', b_Check, b_Uncheck); AURORA(0)
    elif TOUCH_ZONE([[525,1730], [574,1850]]): CHECK(menu.bght, 1, 'display', b_Check, b_Uncheck); AURORA(10)
    elif TOUCH_ZONE([[574,1730], [623,1850]]): CHECK(menu.bght, 2, 'display', b_Check, b_Uncheck); AURORA(20)
    elif TOUCH_ZONE([[623,1730], [672,1850]]): CHECK(menu.bght, 3, 'display', b_Check, b_Uncheck); AURORA(30)
    elif TOUCH_ZONE([[672,1730], [721,1850]]): CHECK(menu.bght, 4, 'display', b_Check, b_Uncheck); AURORA(40)
    elif TOUCH_ZONE([[721,1730], [770,1850]]): CHECK(menu.bght, 5, 'display', b_Check, b_Uncheck); AURORA(50)
    elif TOUCH_ZONE([[770,1730], [819,1850]]): CHECK(menu.bght, 6, 'display', b_Check, b_Uncheck); AURORA(60)
    elif TOUCH_ZONE([[819,1730], [868,1850]]): CHECK(menu.bght, 7, 'display', b_Check, b_Uncheck); AURORA(70)
    elif TOUCH_ZONE([[868,1730], [917,1850]]): CHECK(menu.bght, 8, 'display', b_Check, b_Uncheck); AURORA(80)
    elif TOUCH_ZONE([[917,1730], [966,1850]]): CHECK(menu.bght, 9, 'display', b_Check, b_Uncheck); AURORA(90)
    
    return
        
#-----------------------------------------------------------------------------------------------
#------ DISP/FLSH MENU -------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------- 

def F_dispflsh():
    # ----- LOADING CONTENT ------------
    LOAD(directory + "menu_dispflsh.pgm")
    WINDOW_HEADER('Display/Flash menu')
        
    # ----- STAY IN MENU UNTIL SPECIFIED -----------
    while True:
        # ----- RETRIEVE DATA FROM MODULE -----------
        data_Disp = GET_DATA('disp', 'slideshow')
        data_Flsh = GET_DATA('flsh', 'slideshow')
        data_Auto = GET_DATA('auto', 'slideshow')
        
        # ----- CONVERT DATA TO MENU LOCATIONS ------------
        if str(data_Disp) == 'full': CHECK(menu.disp, 0)
        if str(data_Disp) == 'part': CHECK(menu.disp, 1)
        
        if str(data_Flsh) == 'none': CHECK(menu.flsh, 0)
        if str(data_Flsh) == 'full': CHECK(menu.flsh, 1)
        if str(data_Flsh) == 'best': CHECK(menu.flsh, 2)
        if str(data_Flsh) == 'strd': CHECK(menu.flsh, 3)
        if str(data_Flsh) == 'fast': CHECK(menu.flsh, 4)
        
        if   str(data_Auto) == 'yes': CHECK(menu.auto, 1); auto_Opp = 'no' # for single buttons, check=1 is yes, check=0 is no
        elif str(data_Auto) == 'no':  CHECK(menu.auto, 0); auto_Opp = 'yes'        
        
        # ----- DISPLAY BUTTONS -------------
        BUTTONS(menu.disp)   
        BUTTONS(menu.flsh)
        BUTTONS(menu.auto)
        
        # ----- WAITING FOR INPUT ----------       
        GET_INPUT()
        if touch:            
            if   TOUCH_ZONE([635,820],     [747,976]): REPLACE_DATA('disp', 'full', 'slideshow')
            elif TOUCH_ZONE([953,820],    [1095,976]): REPLACE_DATA('disp', 'part', 'slideshow')
            elif TOUCH_ZONE([594,1104],   [680,1260]): REPLACE_DATA('flsh', 'none', 'slideshow') 
            elif TOUCH_ZONE([820,1104],   [900,1260]): REPLACE_DATA('flsh', 'full', 'slideshow')  
            elif TOUCH_ZONE([1040,1104], [1120,1260]): REPLACE_DATA('flsh', 'best', 'slideshow') 
            elif TOUCH_ZONE([545,1295],   [730,1450]): REPLACE_DATA('flsh', 'strd', 'slideshow') 
            elif TOUCH_ZONE([790,1295],   [920,1450]): REPLACE_DATA('flsh', 'fast', 'slideshow') 
            elif TOUCH_ZONE([1000,1295], [1160,1450]): REPLACE_DATA('auto', auto_Opp, 'slideshow')  
            elif TOUCH_ZONE(TOUCH_DICT['slider']): 
                if   device.slide == 'bght': F_brightness()
                elif device.slide == 'temp': F_temperature()
            elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
            elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
            elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch()
            elif TOUCH_ZONE(TOUCH_DICT['back_button']): return 'back'  
            elif TOUCH_ZONE(TOUCH_DICT['exit_button']): return 'exit' # exit button 
            elif TOUCH_ZONE(TOUCH_DICT['settings_button']): return 'exit' # settings button
            else: continue
        
#-----------------------------------------------------------------------------------------------
#------ CHANGE SLIDE NUMBER --------------------------------------------------------------------
#----------------------------------------------------------------------------------------------- 
        
def F_gotoslide():
    # ----- LOADING CONTENT ------------
    LOAD(directory + 'menu_gotoslide.pgm')  
    WINDOW_HEADER('Go-to-slide menu')  
    GET_SLIDE((849, 617))
    slide = ""   
    
    while True:        
        img = Image.open(directory + "blank_gotoslide.pgm")
        I1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/Serif_DejaVu.ttf", 80)
        I1.text((10, 10), slide, font=myFont, fill=0)
        
        img.save(directory + "tmp_gotoslide.pgm")
        LOAD_AREA(directory + 'tmp_gotoslide.pgm', (758, 743))  
        
        s_Check = directory + "check_bar.pgm"; s_Uncheck = directory + "uncheck_bar.pgm"
        BUTTONS(menu.sshw, "display", s_Check, s_Uncheck)
        
        GET_INPUT()
        if touch:
            if   TOUCH_ZONE([[760,490],  [860,610]]):   CHECK(menu.sshw, 0, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(1); GET_SLIDE((849, 617))
            elif TOUCH_ZONE([[876,490],  [976,610]]):   CHECK(menu.sshw, 1, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(2); GET_SLIDE((849, 617))
            elif TOUCH_ZONE([[992,490], [1092,610]]):   CHECK(menu.sshw, 2, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(3); GET_SLIDE((849, 617))

            elif TOUCH_ZONE([[440,940],  [627,1080]]):  slide = slide + '7'
            elif TOUCH_ZONE([[627,940],  [813,1080]]):  slide = slide + '8'
            elif TOUCH_ZONE([[813,940],  [1000,1080]]): slide = slide + '9'
            elif TOUCH_ZONE([[440,1080], [627,1220]]):  slide = slide + '4' 
            elif TOUCH_ZONE([[627,1080], [813,1220]]):  slide = slide + '5'  
            elif TOUCH_ZONE([[813,1080], [1000,1220]]): slide = slide + '6' 
            elif TOUCH_ZONE([[440,1220], [627,1360]]):  slide = slide + '1'
            elif TOUCH_ZONE([[627,1220], [813,1360]]):  slide = slide + '2' 
            elif TOUCH_ZONE([[813,1220], [1000,1360]]): slide = slide + '3'
            elif TOUCH_ZONE([[627,1360], [813,1500]]):  slide = slide + '0'
            elif TOUCH_ZONE([[440,1360], [627,1500]]):  # BACK
                slide = slide[:-1]
                if len(slide) == 0: slide = ""
            elif TOUCH_ZONE([[813,1360], [1000,1500]]): # ENTER
                if int(slide) >= len(slideshow.file):
                    slide = len(slideshow.file)
                F_slideshow(menu.sshw.check + 1, int(slide) - 2); F_main()
            elif TOUCH_ZONE(TOUCH_DICT['slider']): 
                if   device.slide == 'bght': F_brightness()
                elif device.slide == 'temp': F_temperature()
            elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
            elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
            elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch()
            elif TOUCH_ZONE(TOUCH_DICT['back_button']): return 'back'  
            elif TOUCH_ZONE(TOUCH_DICT['exit_button']): return 'exit' # exit button 
            elif TOUCH_ZONE(TOUCH_DICT['settings_button']): return 'exit' # settings button
            
            else: continue
    
#-----------------------------------------------------------------------------------------------
#------ ROTATION MENU --------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------  
            
def F_rotation():
    r_Check = directory + "check_bar.pgm"; r_Uncheck = directory + "uncheck_bar.pgm"
    LOAD(directory + "menu_rotation.pgm")

    while True:
        data = GET_DATA('rot', 'slideshow')
        WINDOW_HEADER('Rotation menu')
        CHECK(menu.rot, int(data), 'display', r_Check, r_Uncheck)
        
        GET_INPUT()
        if touch:
            if   TOUCH_ZONE([[470,900],    [670,1100]]): CHECK(menu.rot, 0, None, r_Check, r_Uncheck); REPLACE_DATA('rot', 0, 'slideshow');
            elif TOUCH_ZONE([[770,900],    [970,1100]]): CHECK(menu.rot, 1, None, r_Check, r_Uncheck); REPLACE_DATA('rot', 1, 'slideshow'); 
            elif TOUCH_ZONE([[470,1200],   [670,1400]]): CHECK(menu.rot, 2, None, r_Check, r_Uncheck); REPLACE_DATA('rot', 2, 'slideshow');
            elif TOUCH_ZONE([[770,1200],   [970,1400]]): CHECK(menu.rot, 3, None, r_Check, r_Uncheck); REPLACE_DATA('rot', 3, 'slideshow');
            elif TOUCH_ZONE(TOUCH_DICT['slider']): 
                if   device.slide == 'bght': F_brightness()
                elif device.slide == 'temp': F_temperature()
            elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
            elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
            elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch()
            elif TOUCH_ZONE(TOUCH_DICT['back_button']): return 'back'  
            elif TOUCH_ZONE(TOUCH_DICT['exit_button']): return 'exit' # exit button 
            elif TOUCH_ZONE(TOUCH_DICT['settings_button']): return 'exit' # settings button
            else: continue

#-----------------------------------------------------------------------------------------------
#------ ON-SCREEN SKETCH -----------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------  
        
def F_sketch(arg = None):
    """
    Clicking the sketch button during a paused slideshow calls acepsketch
    The draw function only works if the image is loaded as 'fast', highlighter as 'DU'
    This means for color images, any non-fast rendered images must be color index converted using color_convert()
    """
    global slideshow, N   
    
    if arg == 'app':
        CLEAR('best')
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 
        device.sect = None
        F_main()
        return
    
    if device.sect == 'psettings': # If demo was in a menu when the sketch button was pressed, remove the menu by reloading  and displaying the slide
        LOAD(slideshow) # Reload the slideshow slide #N
        DISPLAY_AREA(slideshow, (0,80), (1440,1715)) #Redisplay the background slideshow     

    if slideshow.wfm[N] == 3: # Only use highlighter on black and white text images
        LOAD("/mnt/mmc/images/charmr/1440x1920/highlighter.pgm")   
        DISPLAY(2, 'full')
        LOAD(slideshow)
        DISPLAY_AREA(6, (0,80), (1440,1715))
        converted = PP1_22_40C(slideshow.path + slideshow.file[N], 'text', 'pen') # color_convert.PP1_22_40C() for this GAL3 .wbf       
        # highlight_sketch.txt calls Jaya's ACeP sketch program. The background image is loaded as tmp_converted
        # This means that the color_convert function must be run regardless of the current wfm
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_highlighter.txt")
    else: # else use draw
        LOAD("/mnt/mmc/images/charmr/1440x1920/draw.pgm")   
        DISPLAY(2, 'full')
        converted = PP1_22_40C(slideshow.path + slideshow.file[N], 'strd', 'fast') # color_convert.PP1_22_40C() for this GAL3 .wbf       
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_draw.txt")  
        
    F_pause() # Go back to pause when finished

#-----------------------------------------------------------------------------------------------
#------ TEMPERATURE SCROLL ---------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
                      
def F_temperature(): 

    # ----- LOADING CONTENT ------------
    b_Check = directory + "check_brightness2.pgm"; b_Uncheck = directory + "uncheck_brightness2.pgm"
        
    if   TOUCH_ZONE([[476,1730], [525,1850]]): CHECK(menu.temp, 0, 'display', b_Check, b_Uncheck); AURORA_TEMP(0)
    elif TOUCH_ZONE([[525,1730], [574,1850]]): CHECK(menu.temp, 1, 'display', b_Check, b_Uncheck); AURORA_TEMP(10)
    elif TOUCH_ZONE([[574,1730], [623,1850]]): CHECK(menu.temp, 2, 'display', b_Check, b_Uncheck); AURORA_TEMP(20)
    elif TOUCH_ZONE([[623,1730], [672,1850]]): CHECK(menu.temp, 3, 'display', b_Check, b_Uncheck); AURORA_TEMP(30)
    elif TOUCH_ZONE([[672,1730], [721,1850]]): CHECK(menu.temp, 4, 'display', b_Check, b_Uncheck); AURORA_TEMP(40)
    elif TOUCH_ZONE([[721,1730], [770,1850]]): CHECK(menu.temp, 5, 'display', b_Check, b_Uncheck); AURORA_TEMP(50)
    elif TOUCH_ZONE([[770,1730], [819,1850]]): CHECK(menu.temp, 6, 'display', b_Check, b_Uncheck); AURORA_TEMP(60)
    elif TOUCH_ZONE([[819,1730], [868,1850]]): CHECK(menu.temp, 7, 'display', b_Check, b_Uncheck); AURORA_TEMP(70)
    elif TOUCH_ZONE([[868,1730], [917,1850]]): CHECK(menu.temp, 8, 'display', b_Check, b_Uncheck); AURORA_TEMP(80)
    elif TOUCH_ZONE([[917,1730], [966,1850]]): CHECK(menu.temp, 9, 'display', b_Check, b_Uncheck); AURORA_TEMP(90)
    
    return
        
#-----------------------------------------------------------------------------------------------
#------ WAVEFORM MENU --------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------  
        
def F_wfm():
    w_Check = directory + "check_bar.pgm"; w_Uncheck = directory + "uncheck_bar.pgm"

    LOAD(directory + "menu_wfm.pgm")
    WINDOW_HEADER('Waveform menu')
    
    if device.sect == 'psettings':
        while True:
            data = GET_DATA('wfm', 'slideshow')
            CHECK(menu.wfms, int(data), 'display', w_Check, w_Uncheck)
           
            GET_INPUT()
            if touch:
                if   TOUCH_ZONE([[300,900],    [510,1100]]): CHECK(menu.wfms, 0, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 0, 'slideshow');
                elif TOUCH_ZONE([[510,900],    [720,1100]]): CHECK(menu.wfms, 1, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 1, 'slideshow');
                elif TOUCH_ZONE([[720,900],    [930,1100]]): CHECK(menu.wfms, 2, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 2, 'slideshow');
                elif TOUCH_ZONE([[930,900],   [1140,1100]]): CHECK(menu.wfms, 3, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 3, 'slideshow'); 
                elif TOUCH_ZONE([[300,1100],   [510,1300]]): CHECK(menu.wfms, 4, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 4, 'slideshow');
                elif TOUCH_ZONE([[510,1100],   [720,1300]]): CHECK(menu.wfms, 5, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 5, 'slideshow');
                elif TOUCH_ZONE([[720,1100],   [930,1300]]): CHECK(menu.wfms, 6, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 6, 'slideshow');
                elif TOUCH_ZONE([[930,1100],  [1140,1300]]): CHECK(menu.wfms, 7, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 7, 'slideshow');  
                if   TOUCH_ZONE(TOUCH_DICT['slider']): 
                    if   device.slide == 'bght': F_brightness()
                    elif device.slide == 'temp': F_temperature()
                elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
                elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
                elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch() 
                elif TOUCH_ZONE(TOUCH_DICT['back_button']): return 'back'  
                elif TOUCH_ZONE(TOUCH_DICT['exit_button']): return 'exit' 
                elif TOUCH_ZONE(TOUCH_DICT['settings_button']): return 'exit'
                else: continue
        
    elif device.sect == 'main':
        image = 'banner'
        while True:          
            if   image == 'banner':  LOAD(directory + 'menu_wfm_banner.pgm')
            elif image == 'main':    LOAD(directory + 'menu_wfm_main.pgm')
            elif image == 'startup': LOAD(directory + 'menu_wfm_startup.pgm')
            elif image == 'check':   LOAD(directory + 'menu_wfm_checkicons.pgm')           
            data = GET_DATA('wfm', image) # Get data first, so screens pop up around the same time
            CHECK(menu.wfmm, int(data), 'display', w_Check, w_Uncheck)

            GET_INPUT()
            if touch:
                if   TOUCH_ZONE([[300,1040],   [510,1240]]): CHECK(menu.wfmm, 0, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 0, image);
                elif TOUCH_ZONE([[510,1040],   [720,1240]]): CHECK(menu.wfmm, 1, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 1, image);
                elif TOUCH_ZONE([[720,1040],   [930,1240]]): CHECK(menu.wfmm, 2, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 2, image);
                elif TOUCH_ZONE([[930,1040],  [1140,1240]]): CHECK(menu.wfmm, 3, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 3, image);
                elif TOUCH_ZONE([[300,1240],   [510,1440]]): CHECK(menu.wfmm, 4, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 4, image); 
                elif TOUCH_ZONE([[510,1240],   [720,1440]]): CHECK(menu.wfmm, 5, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 5, image);
                elif TOUCH_ZONE([[720,1240],   [930,1440]]): CHECK(menu.wfmm, 6, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 6, image);
                elif TOUCH_ZONE([[930,1240],  [1140,1440]]): CHECK(menu.wfmm, 7, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 7, image);
                elif TOUCH_ZONE([[220,500],     [470,650]]): image = 'banner'
                elif TOUCH_ZONE([[470,500],     [720,650]]): image = 'main'
                elif TOUCH_ZONE([[720,500],     [970,650]]): image = 'startup'
                elif TOUCH_ZONE([[970,500],    [1220,650]]): image = 'check'  
                if   TOUCH_ZONE(TOUCH_DICT['slider']): 
                    if   device.slide == 'bght': F_brightness()
                    elif device.slide == 'temp': F_temperature()
                elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS()
                elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE() 
                elif TOUCH_ZONE(TOUCH_DICT['sketch_button']): F_sketch() 
                elif TOUCH_ZONE(TOUCH_DICT['back_button']): return 'back'  
                elif TOUCH_ZONE(TOUCH_DICT['exit_button']): return 'exit' 
                elif TOUCH_ZONE(TOUCH_DICT['settings_button']): return 'exit'
                else: continue       

#################################################################################################################################################################
# UTILITY FUNCTIONS #############################################################################################################################################
#################################################################################################################################################################

def APP_SELECTOR(arg):
    slideshow_number = 1
    app_List = [cm.app1, cm.app2, cm.app3, cm.app4, cm.app5]
    for i in range(arg):
        if   app_List[i].form == 'slideshow': 
            if    i+1 == arg: F_slideshow(slideshow_number)
            else: slideshow_number += 1
        elif app_List[i].form == 'sketch': 
            if    i+1 == arg: F_sketch('app')

def AURORA(brt):  
    """
    Call this function with at least 1 argument to set the lighting brightness.
    brt1: the brightness value(0-100) of LED strip 1
    brt2: the brightness value(0-100) of LED strip 2.
    If no input is given for brt2, LED strip 2 brightness is set to 0.
    
    """
    global button, select, menu
    
    subprocess.call("AURORA_UPDATE=off aurora3 set_brt 4 " + str(brt), shell=True)
    subprocess.call("AURORA_UPDATE=off aurora3 set_brt 3 " + str(brt), shell=True)
    subprocess.call("AURORA_UPDATE=off aurora3 set_brt 2 " + str(brt), shell=True)
    subprocess.call("aurora3 set_brt 1 " + str(brt), shell=True)
    
    menu.bght.check = brt/10 
    
def AURORA_TEMP(temp):  
    """
    temp can be 0 to 9 (10 different temperatures)
    temp2=20 when temp=0
    temp1=20 when temp=9
    
    """
    global button, select, menu
    
    temp1 = int(np.rint(temp*20/90))
    temp2 = int(np.rint(20-temp*20/90))
    
    subprocess.call("AURORA_UPDATE=off aurora3 set_cur 1 " + str(temp1), shell=True)
    subprocess.call("AURORA_UPDATE=off aurora3 set_cur 2 " + str(temp2), shell=True)
    subprocess.call("AURORA_UPDATE=off aurora3 set_cur 3 " + str(temp1), shell=True)
    subprocess.call("aurora3 set_cur 4 " + str(temp2), shell=True)
    
    menu.temp.check = temp/10


def BUTTONS(MENU, disp = 'display', check_File = str(cm.check.file), uncheck_File = str(cm.uncheck.file)):
    """
    Manages the button locations and button movements of all the menu lists.
    Works for menus with any number of buttons, 1 through N
    Once called, button presses are automatically interpreted and the menu list is altered.
    MENU: The menu name (menu.{name}), of the menu list to be managed. 
    disp: If disp = 'display', diplays the updated menu list using DISPLAY(charmr_module.check.wfm, 'part')
    check_File & uncheck_File: If the user wishes to use a different checkmark icon, place the file destinations here.
    """
    global button, select, menu
    select = False
    if type(MENU.locations[0]) == int:
        if MENU.check == 1:
            subprocess.call('bs_load_img_area ' + str(cm.check.rot) + " " + str(MENU.locations[0]) + " " + str(MENU.locations[1]) + " " + check_File, shell = True)
        else:     
            subprocess.call('bs_load_img_area ' + str(cm.uncheck.rot) + " " + str(MENU.locations[0]) + " " + str(MENU.locations[1]) + " " + uncheck_File, shell = True)  
        if disp == 'display': DISPLAY(cm.check, 'part')
        return
    
    n = len(MENU.locations)
    array = [0]*n
    for i in range(n):
        if i == 0: array[i] = 1
        else: array[i] = 0
    matrix = [ [array[(col-row)%n] for col in range(n)] for row in range(n)] # Matrix defining the possible check button positions (identity matrix)
    # Here the column # is the button that is checked, while the row # is the initally selected button location
    if   button == 'down':  matrix = [ [array[(col-row-1)%n] for col in range(n)] for row in range(n)] 
    elif button == 'up':    matrix = [ [array[(col-row+1)%n] for col in range(n)] for row in range(n)]      
    elif button == 'enter': select = MENU.check # Enter/pause button
    # In this new matrix, the column # is the new button to be checked, while the row # is the previously checked location   
    for i in range(n): # Finds the checked value (1) and makes all other buttons unchecked (0)
        if matrix[MENU.check][i] != 1:
            subprocess.call('bs_load_img_area ' + str(cm.uncheck.rot) + " " + str(MENU.locations[i][0]) + " " + str(MENU.locations[i][1]) + " " + uncheck_File, shell = True)
        else:
            subprocess.call('bs_load_img_area ' + str(cm.check.rot) + " " + str(MENU.locations[i][0]) + " " + str(MENU.locations[i][1]) + " " + check_File, shell = True)  
    if   disp == 'display': DISPLAY(cm.check, 'part')
    if   button == 'down': MENU.check = (MENU.check+1)%n
    elif button == 'up': MENU.check = (MENU.check-1)%n
    button = False
    WAIT(100)
    
def BUTTON_BRIGHTNESS():
    LOAD_AREA(directory + 'label_brightness.pgm', (616,1718))   
    BUTTONS(bght, 'no display', directory + "check_brightness2.pgm", directory + "uncheck_brightness2.pgm")
    device.slide = 'bght'

def BUTTON_TEMPERATURE():
    LOAD_AREA(directory + 'label_temperature.pgm', (616,1718));
    BUTTONS(temp, 'no display', directory + "check_brightness2.pgm", directory + "uncheck_brightness2.pgm")
    device.slide = 'temp'

def CHANGE_SLIDE(direction, style = None): # Moves to next slide of slideshow
    """
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
    """
    global slideshow, N # N is the slide number

    if type(direction) == int: 
        N = direction # direction can be 'back' or 'next', or an integer will change to that slide number   
        return
    elif direction == "next": 
        N += 1; prev = -1; swipe = 'left'
        if N >= len(slideshow.file): CLEAR("full"); F_main()
        LOAD(slideshow)
    elif direction == "back":
        N -= 1; prev = 1; swipe = 'right'
        if N < 0: N = 0 # If already on first slide, remain there
        LOAD(slideshow)
    elif direction == "back two":
        N -= 2; prev = 2; swipe = 'right'
        if N < 0: N = 0 # If already on first slide, remain there
        LOAD(slideshow)    
    elif direction == "remain": 
        if style == None:
            DISPLAY(slideshow, slideshow.disp[N])            
        if style == "swipe":
            DISPLAY_SWIPE("left", wfm_Disp.text)    
        if style == 'center-out':
            DISPLAY_CENTER_OUT(slideshow.wfm[N])
        return
    # --------------------------------------------------------------------------- 
    if style == "swipe":    
        if   slideshow.wfm[N] == wfm_Disp.best: # Best color
            if   slideshow.wfm[N+prev] == wfm_Disp.best: DISPLAY_SWIPE(swipe, 13)
            elif slideshow.wfm[N+prev] == wfm_Disp.fast: DISPLAY_SWIPE(swipe, 13, 'clear')
            elif slideshow.wfm[N+prev] == wfm_Disp.text: DISPLAY_SWIPE(swipe, 13, 'clear', wfm_Disp.text)
            elif slideshow.wfm[N+prev] == wfm_Disp.strd: DISPLAY_SWIPE(swipe, 13, 'clear')
            else: DISPLAY_SWIPE("left", 13)                      
        elif slideshow.wfm[N] == wfm_Disp.fast: # Fast color
            if   slideshow.wfm[N+prev] == wfm_Disp.best: DISPLAY_SWIPE(swipe, 13, 'clear')
            elif slideshow.wfm[N+prev] == wfm_Disp.fast: DISPLAY_SWIPE(swipe, 13)  
            elif slideshow.wfm[N+prev] == wfm_Disp.text: DISPLAY(wfm_Disp.fast, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.strd: DISPLAY_SWIPE(swipe, 13)
            else: DISPLAY_SWIPE("left", 13)
        elif slideshow.wfm[N] == wfm_Disp.text: # Text
            if   slideshow.wfm[N+prev] == wfm_Disp.best: DISPLAY_SWIPE(swipe, 13, 'clear only')
            elif slideshow.wfm[N+prev] == wfm_Disp.fast: DISPLAY(wfm_Disp.strd, slideshow.disp[N])   
            elif slideshow.wfm[N+prev] == wfm_Disp.text: DISPLAY(wfm_Disp.text, slideshow.disp[N]) 
            elif slideshow.wfm[N+prev] == wfm_Disp.strd: DISPLAY(wfm_Disp.strd, slideshow.disp[N]) 
            else: DISPLAY_SWIPE("left", 13)            
        elif slideshow.wfm[N] == wfm_Disp.strd: # Strd color
            if   slideshow.wfm[N+prev] == wfm_Disp.best: DISPLAY_SWIPE(swipe, 13, 'clear')
            elif slideshow.wfm[N+prev] == wfm_Disp.fast: DISPLAY_SWIPE(swipe, 13)  
            elif slideshow.wfm[N+prev] == wfm_Disp.text: DISPLAY(wfm_Disp.strd, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.strd: DISPLAY_SWIPE(swipe, 13)
            else: DISPLAY_SWIPE("left", 13)                   
    # ------------------------------------------------------ 
    elif style == "center-out":
        DISPLAY_CENTER_OUT(slideshow.wfm[N])
    # ------------------------------------------------------       
    else: # NORMAL DISPLAY STYLE
        if   slideshow.wfm[N] == wfm_Disp.best: # Best color
            if   slideshow.wfm[N+prev] == wfm_Disp.best: DISPLAY(wfm_Disp.best, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.fast: CLEAR('best'); DISPLAY(wfm_Disp.best, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.text: CLEAR('text'); DISPLAY(wfm_Disp.best, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.strd: CLEAR('best'); DISPLAY(wfm_Disp.best, slideshow.disp[N])
            else: DISPLAY_SWIPE("right", 13)                      
        elif slideshow.wfm[N] == wfm_Disp.fast: # Fast color
            if   slideshow.wfm[N+prev] == wfm_Disp.best: CLEAR('best'); DISPLAY(wfm_Disp.fast, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.fast: DISPLAY(wfm_Disp.fast, slideshow.disp[N])  
            elif slideshow.wfm[N+prev] == wfm_Disp.text: DISPLAY(wfm_Disp.fast, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.strd: DISPLAY(wfm_Disp.fast, 13)
            else: DISPLAY_SWIPE("right", 13)
        elif slideshow.wfm[N] == wfm_Disp.text: # Text
            if   slideshow.wfm[N+prev] == wfm_Disp.best: CLEAR('best'); DISPLAY(wfm_Disp.text, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.fast: DISPLAY(wfm_Disp.strd, slideshow.disp[N])   
            elif slideshow.wfm[N+prev] == wfm_Disp.text: DISPLAY(wfm_Disp.text, slideshow.disp[N]) 
            elif slideshow.wfm[N+prev] == wfm_Disp.strd: DISPLAY(wfm_Disp.strd, slideshow.disp[N]) 
            else: DISPLAY(slideshow, slideshow.disp[N])           
        elif slideshow.wfm[N] == wfm_Disp.strd: # Strd color
            if   slideshow.wfm[N+prev] == wfm_Disp.best: CLEAR('best'); DISPLAY(wfm_Disp.strd, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.fast: DISPLAY(wfm_Disp.strd, slideshow.disp[N])  
            elif slideshow.wfm[N+prev] == wfm_Disp.text: DISPLAY(wfm_Disp.strd, slideshow.disp[N])
            elif slideshow.wfm[N+prev] == wfm_Disp.strd: DISPLAY(wfm_Disp.strd, slideshow.disp[N])        
    
def CHANGE_SLIDESHOW(arg):
    """
    Changes the slideshow number to the number placed in argument
    """    
    s_Check = directory + 'check_bar.pgm'; s_Uncheck = directory + 'uncheck_bar.pgm'    

    global slideshow
    if int(arg) == 1: slideshow = cm.slideshow1
    if int(arg) == 2: slideshow = cm.slideshow2
    if int(arg) == 3: slideshow = cm.slideshow3
    
    CHECK(menu.sshw, int(arg)-1, None, s_Check, s_Uncheck);
    
def CHECK(MENU, new_Check=0, disp = None, check_File = cm.check.file, uncheck_File = cm.uncheck.file):
    """
    Changes the checkmark value in a menu list. Takes between 1 and 5 arguments.
    MENU: The menu name (menu.{name}), of the menu list to be altered.
    new_Check: The new check mark value to be displayed in the menu (1st position = 0, 2nd position = 1, etc.)
    disp: Either None or 'display', will display the check buttons on the screen if informed.
    check_File & uncheck_File: If the user wishes to use a different checkmark icon, place the file destinations here.
    
    **If list has a single button, check=1 is on and check=0 is off
    """
    if MENU == 'all':
        menu.psettings.check = new_Check
        menu.msettings.check = new_Check
        menu.main.check = new_Check
        menu.lighting.check = new_Check
        return
    MENU.check = new_Check
    BUTTONS(MENU, disp, check_File, uncheck_File)

def CLEAR(flsh, disp = 'full'):
    """
    Clears the current screen. Takes one of 5 arguments: 'slideshow', 'full', 'fast', 'strd', 'best', or 'none'
    'slideshow': Manages clearing before the current slide in the slideshow, based on user specifications and recommendations
    The other arguments can be user designated in the program or read from the charmr_module
    Auto flash is set to 'norm' (standard display white flash)
    """ 
    if  flsh == 'full': 
        LOAD(directory + 'white240.pgm'); 
        subprocess.call("bs_disp_" + disp + " 0", shell = True)    
    elif flsh == 'text': 
        LOAD(directory + 'white240.pgm'); 
        subprocess.call("bs_disp_" + disp + " 3", shell = True)
    elif flsh == 'fast':   
        LOAD(directory + 'white240.pgm'); 
        subprocess.call("bs_disp_" + disp + " 4", shell = True)
    elif flsh == 'strd': 
        LOAD(directory + 'white240.pgm'); 
        subprocess.call("bs_disp_" + disp + " 2", shell = True)
    elif flsh == 'best': 
        LOAD(directory + 'white240.pgm'); 
        subprocess.call("bs_disp_" + disp + " 5", shell = True)
    elif flsh == 'none': pass

def CLOCK(arg = "check"):
    if arg == "set": device.time = None
    sample_Time = datetime.datetime.now() + datetime.timedelta(hours=11, minutes=6, seconds=33) # The controller clock isn't correct, needs an offset 
    if sample_Time.minute > 9:
        current_Time = str(str(sample_Time.hour) + ":" + str(sample_Time.minute) + sample_Time.strftime("%p"))
    else:
        current_Time = str(str(sample_Time.hour) + ":0" + str(sample_Time.minute) + sample_Time.strftime("%p"))
    if device.time != current_Time or arg == 'load':
        device.time = current_Time
        if sample_Time.hour > 12:
            hour = sample_Time.hour - 12
        else:
            hour = sample_Time.hour
        if sample_Time.minute > 9:
            current_Time = str(hour) + ":" + str(sample_Time.minute) + sample_Time.strftime("%p")
        else:
            current_Time = str(hour) + ":0" + str(sample_Time.minute) + sample_Time.strftime("%p")    
        if   cm.wsize == 1440: time_Written = TEXT_TO_IMAGE(current_Time, "Sans_Monofonto.otf", 52, directory + "blank_time.pgm", (10,7))
        elif cm.wsize == 1264: time_Written = TEXT_TO_IMAGE(current_Time, "Sans_Monofonto.otf", 42, directory + "blank_time.pgm", (0,10))
        if hour < 10:
            LOAD_AREA(time_Written, cm.area.clock[0])
        else: 
            LOAD_AREA(time_Written, cm.area.clock[1])
        if arg != "load":
            DISPLAY(wfm_Disp.text, "part")
        
def COMMAND(string, call):
    if   call == 'sub':   subprocess.call(string, shell = True)
    elif call == 'os':    os.system(string)
    elif call == 'Popen': subprocess.Popen(string, stdout=subprocess.PIPE, shell = True)

def DISPLAY(WFM, method = 'full'):
    if isinstance(WFM, cm.IMAGE):
        if isinstance(WFM.wfm, list):
            wfm = WFM.wfm[N]
        else:
            wfm = WFM.wfm   
        COMMAND('bs_disp_' + method + ' ' + str(wfm), 'sub')
    else: 
        COMMAND('bs_disp_' + method + ' ' + str(WFM), 'sub')
        
def DISPLAY_AREA(WFM, pos1, pos2, rot=1): # pos1 is upper left coordinate tuple and pos2 is lower right coordinate tuple
    if isinstance(WFM, cm.IMAGE):
        if isinstance(WFM.wfm, list):
            wfm = WFM.wfm[N]
            rot = WFM.rot[N]
        else: 
            wfm = WFM.wfm  
    else: wfm = WFM
    
    """
    Displays the image loaded into the buffer.
    WFM: The waveform number used in displaying (or object of IMAGE class from charmer module)
    method = 'full' or 'part': 'full' updates the entire area while 'part' only updates pixels of different values
    pos1, pos2: The area on the screen to be displayed. 
        Measured as (x,y) from the top left of the screen, pos1 is the top left corner of the display area (x1,y1) 
        and pos2 is the bottom right corner of the display area (x2,y2), making a rectangle of area (x2-x1) * (y2-y1)
    """  
    X = ' '; SSX = cm.hsize; SSY = cm.wsize
    if   rot == 1:
        COMMAND('bs_disp_full_area ' + str(wfm) +X+ str(pos1[0]) +X+ str(pos1[1]) +X+ str(pos2[0]-pos1[0]) +X+ str(pos2[1]-pos1[1]), 'sub')
    elif rot == 0: 
        COMMAND('bs_disp_full_area ' + str(wfm) +X+ str(SSY - pos1[1]) +X+ str(pos1[0]) +X+ str(pos2[1]-pos1[1]) +X+ str(pos2[0] - pos1[0]), 'sub') 
    elif rot == 2:
        COMMAND('bs_disp_full_area ' + str(wfm) +X+ str(pos1[1]) +X+ str(SSX - pos1[0]) +X+ str(pos2[1]-pos1[1]) +X+ str(pos2[0] - pos1[0]) + ' block_rails_active', 'sub') 
    elif rot == 3:
        COMMAND('bs_disp_full_area ' + str(wfm) +X+ str(SSX - pos1[0]) +X+ str(SSY - pos1[1]) +X+ str(pos2[0]-pos1[0]) +X+ str(pos2[1]-pos1[1]) + ' block_rails_active', 'sub')
    
def DISPLAY_CENTER_OUT(wfm):
    """
    """
    global slideshow, N
    rot = 1
    delay = 13
    clear_Detect = 0
    
    if   slideshow.auto[N] == 'yes': # Auto flush defaults to normal clear wfm
        wfm_Time = 518 +200
        clear_WFM = wfm_Disp.best
    if   slideshow.flsh[N] == 'full': 
        wfm_Time = 3541 +200
        clear_WFM = wfm_Disp.init
    elif slideshow.flsh[N] == 'fast': 
        wfm_Time = 377 +200  
        clear_WFM = wfm_Disp.text
    elif slideshow.flsh[N] == 'strd': 
        wfm_Time = 518 +200  
        clear_WFM = wfm_Disp.fast
    elif slideshow.flsh[N] == 'best': 
        wfm_Time = 1518 +200 
        clear_WFM = wfm_Disp.best
        
    if os.path.exists("swipe.txt"): # Checks if tiler_module.py exists, deletes if it does. Then writes the module file.
        os.remove("swipe.txt")
    with open("swipe.txt", "w") as f:
        f.write("LD_IMG " + directory + "white240.pgm\n")
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

def DISPLAY_SWIPE(direction, delay, style = 'reg', clear_WFM = None, image_WFM = None):
    """
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
    """
    global slideshow, N, i, iwidth, j, jwidth
    rot = slideshow.rot[N]
    clear_Detect = 0
    
    if isinstance(clear_WFM, int): pass
    elif slideshow.auto[N] == 'yes':  clear_WFM = wfm_Disp.best # Auto
    elif slideshow.flsh[N] == 'full': clear_WFM = wfm_Disp.init
    elif slideshow.flsh[N] == 'fast': clear_WFM = wfm_Disp.fast
    elif slideshow.flsh[N] == 'strd': clear_WFM = wfm_Disp.strd
    elif slideshow.flsh[N] == 'best': clear_WFM = wfm_Disp.best
        
    if clear_WFM == wfm_Disp.init: wfm_Time = 3541-100 # Assume it takes 100ms to load the image
    if clear_WFM == wfm_Disp.strd: wfm_Time = 1024-100
    if clear_WFM == wfm_Disp.text: wfm_Time = 377  # This is a fast enough flash, don't need to reduce the time
    if clear_WFM == wfm_Disp.fast: wfm_Time = 518 -100
    if clear_WFM == wfm_Disp.best: wfm_Time = 1518-100
    
    if isinstance(image_WFM, type(None)):
        image_WFM = slideshow.wfm[N]
    
    if os.path.exists("swipe.txt"):
        os.remove("swipe.txt")
    with open("swipe.txt", "w") as f:
        f.write("SET_ROT " + str(rot*90) + " \n")
        if style == 'clear' or style == 'clear only':
            f.write("LD_IMG " + directory + "white240.pgm\n")
        i = 0; j = 0 # i: image, j: clear
        i_iteration = 1
        width = int(math.ceil(1440/16))
        iwidth = width; jwidth = width # jwidth for image, iwidth for clear
        
        if rot == 2 or rot == 3: 
            if   direction == 'right': direction = 'left'
            elif direction == 'left': direction = 'right'
        
        def UPD_AREA_CLEAR(rot, direction):
            global slideshow, N, i, iwidth, j, jwidth
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
            global slideshow, N, i, iwidth, j, jwidth
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
            f.write("LD_IMG " + slideshow.path + slideshow.file[N] + "\n")
            while j < cm.wsize:
                if cm.wsize - j < jwidth: jwidth = cm.wsize - i
                UPD_AREA_IMAGE(rot, direction)
                f.write("SLEEP " + str(delay) + "\n")
                j += jwidth
                        
    subprocess.call("SET_SPECIFIC_TEMP=25 PWRDOWN_DELAY=10 /mnt/mmc/api/tools/cmder /mnt/mmc/api/tools/swipe.txt", shell=True)
                
def GET_DATA(data_Type, image):
    """
    Retrieves the user-specified data from the charmr module file.
    data_Type: The type of data to be retrieved. 'wfm', 'rot' 'disp', etc.
    image: The user specified image to take the data value from. 'banner', 'slideshow', 'startup', etc.
    """
    global slideshow
    with open("charmr_module.py", "r") as f: # Opening file to read current wfm
        lines = f.readlines()
    for number1, line in enumerate(lines):
        if image == 'slideshow': # This seems like and unneccessary way to access the data, but the module file updates before any reimport.
                                 # Without reading through the file every time, the user would not see the updated value on the screen.
            if line.find(str(slideshow.name) + "." + data_Type) == 0:
                data = line[len(str(slideshow.name) + "." + data_Type)+1:]
                data = data.replace('"', '').replace('\'', '')
                data = data.strip('[').replace(']', "").split(', ')
                data[len(data)-1] = data[len(data)-1].strip("\n")
                return data[N] 
        else:
            if line.find(image + "." + data_Type) == 0:
                data = line[len(str(image) + "." + data_Type)+1:]
                return data            

def GET_INPUT(swipe = None, t=None): # Optional t input is the timeout, meant for slideshow
    """
    get_Input() waits indefintely for either a screen touch or a button press and returns global values 'button, touch'
    If a button is pressed, returns as 'up', 'down' or 'enter'. Brightness button returns as None.
    The screen can be either tapped or swiped.
        If screen is tapped, returns as a tuple giving location of the tap.
        If the screen is swiped, returns the direction of swipe as a string 'swipe left', 'swipe right', 'swipe up', or 'swipe down'
    Optional argument t: Timeout feature. get_Input will wait for t milliseconds before exiting function and moving on
    """
    global touch, button
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
                if (time.time() - start_Time)*1000 >= t: break
            else: 
                CLOCK("check") # On-screen clock display
            if touchd_proc.returncode is None: pass
            else: break
    else:
        while button_proc.returncode is None:
            button_proc.poll()
            if t != None:
                if (time.time() - start_Time)*1000 >= t: break
            else: 
                CLOCK("check")
    
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
        return
    
    elif button_proc.returncode is not None: 
        button, err = button_proc.communicate(); 
        button = int(button); touch = None
        if   button == 1: button = 'up'
        elif button == 2: button = 'down'
        elif button == 4: button = 'enter'
        if cm.touch: touchd_proc.kill()
        
    else: 
        button = None; touch = None
        button_proc.kill(); 
        if cm.touch: touchd_proc.kill()
        
def GET_SLIDE(arg):
    img = Image.open(directory + "blank_gotoslide.pgm")
    I1 = ImageDraw.Draw(img)
    I1.fontmode = "1"
    myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/Serif_DejaVu.ttf", 80)
    I1.text((10, 10), str(N + 1) + '/' + str(len(slideshow.file)), font=myFont, fill=0)
    img.save(directory + 'tmp_currentslide.pgm')
    LOAD_AREA(directory + 'tmp_currentslide.pgm', arg)       
    
def LOAD(img, rot=1): # Can take img = slideshow as only argument, determines what to load from there.
    if isinstance(img, cm.IMAGE):
        if isinstance(img.rot, list):
            img2 = img.path + img.file[N]
            rot2 = img.rot[N]
        else: 
            img2 = img.file
            rot2 = img.rot
    else: img2 = img; rot2 = rot
            
    subprocess.call('bs_load_img ' + str(rot2) + ' ' + str(img2), shell = True)
    
def LOAD_AREA(img, pos, rot=1): #pos = screen coordinate tuple from top left (x,y)
    X = ' '; SSX = cm.hsize; SSY = cm.wsize
    if isinstance(img, cm.IMAGE):
        if isinstance(img.rot, list):
            img2 = img.path + img.file[N]
            rot2 = img.rot[N]
        else: 
            img2 = img.file
            rot2 = img.rot
    else: img2 = img; rot2 = rot
                        
    if   str(rot) == '1':
        subprocess.call('bs_load_img_area ' + str(rot2) +X+ str(pos[0]) +X+ str(pos[1]) +X+ str(img2), shell = True)
    elif str(rot) == '0':
        subprocess.call('bs_load_img_area ' + str(rot2) +X+ str(SSY - pos1[1]) +X+ str(pos1[0]) +X+ str(img2), shell = True)
    elif str(rot) == '2':
        subprocess.call('bs_load_img_area ' + str(rot2) +X+ str(pos[1]) +X+ str(SSX - pos[0]) +X+ str(img2), shell = True)
    elif str(rot) == '3': 
        subprocess.call('bs_load_img_area ' + str(rot2) + ' ' + str(SSX - pos[0]) + ' ' + str(SSY - pos[1]) + ' ' + str(img2), shell = True)

def LOAD_SAVED_WB():
    subprocess.call("SET_SPECIFIC_TEMP=25 PWRDOWN_DELAY=10 /mnt/mmc/api/tools/cmder bs_load_img 1 tmp/prevwb", shell=True)

def MENU_BUILD(menu_Type, name = "", items = []):
    if   int(cm.wsize) == 1440 and int(cm.hsize) == 1920: 
        if   menu_Type == 'main': 
            img = directory + "menu_main2.pgm"
            if cm.app1.name != "": items.append(cm.app1.name)
            if cm.app2.name != "": items.append(cm.app2.name)
            if cm.app3.name != "": items.append(cm.app3.name)
            if cm.app4.name != "": items.append(cm.app4.name)
            if cm.app5.name != "": items.append(cm.app5.name)
        elif menu_Type == 'menu': 
            img = directory + "menu_reg.pgm"
    elif int(cm.wsize) == 1264 and int(cm.hsize) == 1680: 
        if   menu_Type == 'main': 
            img = directory + "menu_main.pgm"
            if cm.app1.name != "": items.append(cm.app1.name)
            if cm.app2.name != "": items.append(cm.app2.name)
            if cm.app3.name != "": items.append(cm.app3.name)
            if cm.app4.name != "": items.append(cm.app4.name)
            if cm.app5.name != "": items.append(cm.app5.name)
        elif menu_Type == 'menu': 
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
    return menu, button_List     

def MENU_TOUCH(button_List):
    
    x1 = math.ceil(.1944*cm.wsize); x2 = math.ceil(.7986*cm.wsize)
    if   len(button_List.locations) == 1:
        if TOUCH_ZONE([[x1,math.ceil(.4219*cm.hsize)], [x2,math.ceil(.5260*cm.hsize)]]): CHECK(button_List, 0, 'display'); return 1
    elif len(button_List.locations) == 2:
        if TOUCH_ZONE([[x1,math.ceil(.3281*cm.hsize)], [x2,math.ceil(.4375*cm.hsize)]]): CHECK(button_List, 0, 'display'); return 1
        if TOUCH_ZONE([[x1,math.ceil(.5313*cm.hsize)], [x2,math.ceil(.6458*cm.hsize)]]): CHECK(button_List, 1, 'display'); return 2       
    elif len(button_List.locations) == 3:
        if TOUCH_ZONE([[x1,math.ceil(.2969*cm.hsize)], [x2,math.ceil(.4010*cm.hsize)]]): CHECK(button_List, 0, 'display'); return 1
        if TOUCH_ZONE([[x1,math.ceil(.4323*cm.hsize)], [x2,math.ceil(.5417*cm.hsize)]]): CHECK(button_List, 1, 'display'); return 2
        if TOUCH_ZONE([[x1,math.ceil(.5729*cm.hsize)], [x2,math.ceil(.6771*cm.hsize)]]): CHECK(button_List, 2, 'display'); return 3
    elif len(button_List.locations) == 4:
        if TOUCH_ZONE([[x1,math.ceil(.2917*cm.hsize)], [x2,math.ceil(.3958*cm.hsize)]]): CHECK(button_List, 0, 'display'); return 1
        if TOUCH_ZONE([[x1,math.ceil(.3958*cm.hsize)], [x2,math.ceil(.5104*cm.hsize)]]): CHECK(button_List, 1, 'display'); return 2
        if TOUCH_ZONE([[x1,math.ceil(.5104*cm.hsize)], [x2,math.ceil(.6250*cm.hsize)]]): CHECK(button_List, 2, 'display'); return 3
        if TOUCH_ZONE([[x1,math.ceil(.6250*cm.hsize)], [x2,math.ceil(.7292*cm.hsize)]]): CHECK(button_List, 3, 'display'); return 4  
    elif len(button_List.locations) == 5:
        if TOUCH_ZONE([[x1,math.ceil(.2708*cm.hsize)], [x2,math.ceil(.3593*cm.hsize)]]): CHECK(button_List, 0, 'display'); return 1
        if TOUCH_ZONE([[x1,math.ceil(.3593*cm.hsize)], [x2,math.ceil(.4583*cm.hsize)]]): CHECK(button_List, 1, 'display'); return 2
        if TOUCH_ZONE([[x1,math.ceil(.4583*cm.hsize)], [x2,math.ceil(.5521*cm.hsize)]]): CHECK(button_List, 2, 'display'); return 3
        if TOUCH_ZONE([[x1,math.ceil(.5521*cm.hsize)], [x2,math.ceil(.6458*cm.hsize)]]): CHECK(button_List, 3, 'display'); return 4
        if TOUCH_ZONE([[x1,math.ceil(.6458*cm.hsize)], [x2,math.ceil(.7292*cm.hsize)]]): CHECK(button_List, 4, 'display'); return 5

def READ_WB():
    subprocess.call("SET_SPECIFIC_TEMP=25 PWRDOWN_DELAY=10 /mnt/mmc/api/tools/cmder read_wb", shell=True)

def RELOAD():
    import charmr_module as cm
    reload(cm)
    REIMPORT()
    
def REIMPORT():
    import charmr_module as cm
    reload(cm)
    
def REPLACE_DATA(data_Type, replacement, image):
    """
    Replaces image info in the charmrmodule file.
    data_Type: Type of info to be replaced ('rot', 'wfm', 'disp', etc)
    replacement: The info's replacement value
    image: The image whose info is being replaced (slideshow1, banner, etc)
    """
    with open("charmr_module.py", "r") as f: # Replace value in file
        lines = f.readlines()
    for number1, line in enumerate(lines):
        if image == 'slideshow': # Special case because slideshow data are arrays
            global slideshow
            if line.find(str(slideshow.name) + "." + data_Type) == 0:
                data = line[len(str(slideshow.name) + "." + data_Type) + 1:]
                data = data.replace('"', '').replace('\'', '')
                data = data.strip('[').replace(']', "").split(', ')
                data[len(data) - 1] = data[len(data) - 1].strip("\n")
                data[N] = replacement
        else:
            if line.find(image + "." + data_Type) == 0:
                data = line[len(str(image) + "." + data_Type) + 1:]
                data = replacement
    with open("charmr_module.py", "w") as f:
        for line in lines:
            if image == 'slideshow':
                if line.find(str(slideshow.name) + "." + data_Type) == -1: f.write(line) # If the string is not in the data line, returns value -1
                else: f.write(str(slideshow.name) + "." + data_Type + "=" + str(data) + "\n")
            else:
                if line.find(image + "." + data_Type + "=") == -1: f.write(line)
                else: f.write(image + "." + data_Type + "=" + str(data) + "\n")       
    RELOAD()

def RESTART():
    COMMAND("kill python " + sys.argv[0] + "; python " + sys.argv[0], "sub")        

def SLIDE_TIMER():
    global slideshow, N           
    if str(slideshow.wfm[N]) == '2': time_Added = 1024
    if str(slideshow.wfm[N]) == '3': time_Added = 377
    if str(slideshow.wfm[N]) == '4': time_Added = 518
    if str(slideshow.wfm[N]) == '5': time_Added = 1518
    if str(slideshow.wfm[N]) == '6': time_Added = 377
    if str(slideshow.wfm[N]) == '7': time_Added = 729 
    GET_INPUT('swipe', int(slideshow.time[N])+time_Added) 
    
def TERMINATE():
    COMMAND("kill python " + sys.argv[0] + "; touch tmp/terminate_charmr.txt", "sub")    
            
def TEXT_TO_IMAGE(text_String, font, font_Size, img_Blank, offset = (10, 10)):
    img = Image.open(img_Blank)
    I1 = ImageDraw.Draw(img)
    I1.fontmode = "1"
    myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/" + font, font_Size)
    I1.text(offset, text_String, font=myFont, fill=0)
    tmp = directory + "tmp.pgm"    
    img.save(tmp)
    return tmp         

def TOUCH_ZONE(location): # Detects whether the touch was in a specific area
    """
    location is a list of size 2 of tuples of size 2.
    The first tuple is the top left corner and second tuple is the bottom right corner of the touch zone, respectively.
    """
    if touch[0] > cm.wsize - location[1][0] and touch[0] < cm.wsize - location[0][0] and touch[1] > location[0][1] and touch[1] < location[1][1]:   
        return True
    else: return False

def WAIT(t):
    """
    Pauses the program for t milliseconds
    """
    time.sleep(t/1000)
    
def WINDOW_HEADER(text):
    header = TEXT_TO_IMAGE(text, 'Sans_ZagReg.otf', 60, directory + "blank_window_header.pgm")
    LOAD_AREA(header, (250,368))    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# VARIABLE DECLARATIONS AND PROGRAM START ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    

# N is slide number, start out at 0
N = 0
# No touch or button detections
touch = None; button = None; select = False
#Set slideshow global variable to cm.slideshow1
slideshow = cm.slideshow1

# Looks in cm to determine screen size and which directory to use
if cm.wsize == 1440 and cm.hsize == 1920: directory = '/mnt/mmc/images/charmr/1440x1920/'
if cm.wsize == 1264 and cm.hsize == 1680: directory = '/mnt/mmc/images/charmr/1264x1680/'

# (works only for 1440x1920 screen size)
# Builds the button locations for the irregular menus
wfmm_List = [0]*8; wfms_List = [0]*8
for i in range(len(wfmm_List)):
    if i >= 0 and i < 4: # Places the bar icon in the correct wfm block
        wfmm_List[i] = (366+(i*210), 1200)
        wfms_List[i] = (366+(i*210), 1060)        
    if i >= 4:
        wfmm_List[i] = (366+((i-4)*210), 1400)
        wfms_List[i] = (366+((i-4)*210), 1260)  

bght_List = [0]*10
for i in range(10):
    bght_List[i] = (476+(i*49), 1772)
    
temp_List = [0]*10
for i in range(10):
    temp_List[i] = (476+(i*49), 1772)
    
#                 1            2            3             4           5 
rot_List  = [[526, 1060], [833, 1060], [526, 1357],  [833, 1357]]
disp_List = [[654, 826],  [990, 826]]
flsh_List = [[599, 1108], [822, 1108], [1046, 1108], [599, 1300], [822, 1300]]
auto_List = [1046, 1300]
menu_List = [[270, 620],  [270, 820],  [270, 1020],  [270, 1220]]
sshw_List = [[771, 575],  [887, 575],  [1003, 575]]

main = MENU_CHECK([], 0)
mset = MENU_CHECK([], 0)
pset = MENU_CHECK([], 0)
temp = MENU_CHECK(temp_List, 0)
rot  = MENU_CHECK(rot_List, 0)
bght = MENU_CHECK(bght_List, 0)
disp = MENU_CHECK(disp_List, 0)
flsh = MENU_CHECK(flsh_List, 0)
auto = MENU_CHECK(auto_List, 0)
wfmm = MENU_CHECK(wfmm_List, 0)
wfms = MENU_CHECK(wfms_List, 0)
sshw = MENU_CHECK(sshw_List, 0)

# All menus easily accessible
menu = MENUS(main, mset, pset, temp, bght, disp, flsh, auto, wfmm, wfms, rot, sshw)

if cm.aurora: # If the demo has aurora lighting, set to default values
    AURORA(80)
    AURORA_TEMP(30)
# Start clearing the screen
CLEAR('best')
CLEAR('full')
CLEAR('text')

LOAD(cm.startup) # load startup screen and display
DISPLAY(cm.startup, 'part')

# Builds all teh regular-style menus. See MENU_BUILD function for details
img, button_List = MENU_BUILD('main', '_mainmenu') 
main_List = button_List

img, button_List = MENU_BUILD('menu', '_msettings',
                              ['Go to slide', 
                               'Waveforms',
                               'Demo mode',
                               'Restart',
                               'Terminate']
                               ) 
mset_List = button_List

img, button_List = MENU_BUILD('menu', '_psettings',
                              ['Go to slide', 
                               'Waveform', 
                               'Rotation', 
                               'Disp/Flsh',
                               'Main menu']
                               )   
pset_List = button_List

main = MENU_CHECK(main_List, 0)
mset = MENU_CHECK(mset_List, 0)
pset = MENU_CHECK(pset_List, 0)

ctme = None # Current time
wifi = None # Detect wifi network
btth = None # Detect bluetooth
batt = None # Detect battery level
sect = None
slide = None
if 'device.proc' in locals(): # If the demo is restarted but it failed to kill the process at the end, kill now
    os.kill(device.proc, signal.SIGKILL)
proc = os.getpid()

device = DEVICE(ctme, wifi, btth, batt, proc, sect, slide)

# wfm PP1 22-40C 
wfm_Disp = WFM_DISPLAYS(0, 3, 4, 2, 5, 1, 6, 7) # wfm display qualities translated to numbers

# wfm MCC 1466-16-B2 
#wfm_Disp = WFM_DISPLAYS(2, 2, 2, 2, 2, 2, 2, 2)

# # Crash management. Disabled for now
# watchdog_Time = time.time()
# def WATCHDOG():
#     while True:
#         if time.time() - watchdog_Time > 7:
#               HANDLE_CRASH()
#               watchdog_Time = time.time()
#         time.sleep(4)

# def START_SCRIPT():
#     try: F_main('startup')
#     except: HANDLE_CRASH() 

# def HANDLE_CRASH(): # kills the process and creates the terminate file to be found in the bash script
#     time.sleep(3)
#     COMMAND("kill python charmr2.py", "sub")
#     COMMAND("touch tmp/restart_charmr.txt", "sub")

# START_SCRIPT_Thread = threading.Thread(target = START_SCRIPT)
# watchdog_Time = time.time()
# WATCHDOG_Thread = threading.Thread(target = WATCHDOG, args=(watchdog_Time,))
# WATCHDOG_Thread.setDaemon(True)

# WATCHDOG_Thread.start()
# START_SCRIPT_Thread.start()

F_main() # Start