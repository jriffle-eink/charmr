import charmr_module as cm
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
    def __init__(self, main, mset, pset, lght, bght, disp, flsh, auto, wfmm, wfms, rot, sshw):
        self.main = main
        self.mset = mset
        self.pset = pset
        self.lght = lght
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
    def __init__(self, time, wifi, btth, batt, proc, sect):
        self.time = time
        self.wifi = wifi
        self.btth = btth # bluetooth
        self.batt = batt
        self.proc = proc # process id  
        self.sect = sect # Keeps track of where we are in the software. None (startingup), 'main', 'slideshow', 'pause', 'psettings'
        
class WFM_DISPLAYS:
    def __init__(self, init, text, fast, strd, best):
        self.init = init
        self.text = text
        self.fast = fast
        self.strd = strd
        self.best = best
        
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
    
    if device.sect == None: # If coming from startup, clear with 'best'
        CLEAR('best')    
    else: CLEAR("text")
    device.sect = 'main' # Section now set to the main menu 
    
    LOAD(directory + "tmp_mainmenu.pgm", 1)  
    CLOCK("load")
    BUTTONS(main, 'no display')      
    LOAD_AREA(cm.banner.file, cm.banner.rot, (0,80))
    
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
            if   command == 0: APP_SELECTOR(1)
            elif command == 1: APP_SELECTOR(2)
            elif command == 2: APP_SELECTOR(3)
            elif command == 3: APP_SELECTOR(4)     
            elif command == 4: CLEAR("best"); F_snake()   
            
            elif TOUCH_ZONE([.0000*cm.wsize,.9375*cm.hsize], [.1493*cm.wsize,1.000*cm.hsize]): F_brightness()            
            elif TOUCH_ZONE([.1493*cm.wsize,.8854*cm.hsize], [.3125*cm.wsize,1.000*cm.hsize]): F_lighting()
            elif TOUCH_ZONE([.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,1.000*cm.hsize]): pass
            elif TOUCH_ZONE([.8507*cm.wsize,.8854*cm.hsize], [1.000*cm.wsize,1.000*cm.hsize]): F_msettings() 
                           
        elif select: # IF SELECT BUTTON WAS PRESSED
            if   main.check == 0: APP_SELECTOR(1)    #  START SLIDESHOW APP 1
            elif main.check == 1: APP_SELECTOR(2)   
            elif main.check == 1: APP_SELECTOR(3)   
            elif main.check == 3: APP_SELECTOR(4)    # START ACEP SKETCH
            elif main.check == 4: CLEAR("best"); F_snake()      
        
def F_msettings(): # MAIN MENU SETTINGS
    
    # ----- LOADING CONTENT ------------
    LOAD(directory + "tmp_msettings.pgm", 1)  
    WINDOW_HEADER('Main settings')
    DISPLAY(wfm_Disp.text, 'part')
    
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
            
            elif TOUCH_ZONE([.0000*cm.wsize,.9375*cm.hsize], [.1493*cm.wsize,1.000*cm.hsize]): F_brightness() # Brightness button           
            elif TOUCH_ZONE([.1493*cm.wsize,.8854*cm.hsize], [.3125*cm.wsize,1.000*cm.hsize]): F_lighting()   # Lighting button
            elif TOUCH_ZONE([.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,1.000*cm.hsize]): pass; #SKETCH("sketch")     # Sketch button 
            elif TOUCH_ZONE([.8507*cm.wsize,.8854*cm.hsize], [1.000*cm.wsize,1.000*cm.hsize]): F_main()  # Settings button
            elif TOUCH_ZONE([.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]): F_main()  # Exit button   
            else: F_main('msettings')
            
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
        LOAD(slideshow.path + slideshow.file[N], slideshow.rot[N]) # Reload the slideshow
        DISPLAY(slideshow.wfm[N], 'part') #Redisplay the background slideshow     
    device.sect = 'pause'
    
    LOAD(directory + "pause.pgm", 1)
    CLOCK("load")
    tmp = TEXT_TO_IMAGE(str(N + 1) + '/' + str(len(slideshow.file)), 'Serif_DejaVu.ttf', 50, directory + "blank_slidenumber_pause.pgm")   
    LOAD_AREA(tmp, 1, (3,0))
    
    # ----- DISPLAYING CONTENT ------------
    if slideshow.wfm[N] == wfm_Disp.best: 
        DISPLAY(wfm_Disp.best, 'full') 
    if slideshow.wfm[N] == wfm_Disp.fast: 
        DISPLAY(wfm_Disp.fast, 'full')  
    if slideshow.wfm[N] == wfm_Disp.text:
        DISPLAY(wfm_Disp.strd, 'part')
    if slideshow.wfm[N] == wfm_Disp.strd: 
        DISPLAY(wfm_Disp.strd, 'full')
        
    img = Image.open(slideshow.path + slideshow.file[N]) # save the current slide to sketch directory for loading
    tmp = "/mnt/mmc/application/sketch/tmp.pgm"    
    img.save(tmp)       
        
    # ----- WAITING FOR INPUT ----------
    GET_INPUT()
    if touch:  
        if   TOUCH_ZONE([.0000*cm.wsize,.9375*cm.hsize], [.1493*cm.wsize,1.000*cm.hsize]): F_brightness()        
        elif TOUCH_ZONE([.1493*cm.wsize,.8854*cm.hsize], [.3125*cm.wsize,1.000*cm.hsize]): F_lighting()
        elif TOUCH_ZONE([.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,1.000*cm.hsize]): SKETCH("sketch")
        elif TOUCH_ZONE([.8507*cm.wsize,.8854*cm.hsize], [1.000*cm.wsize,1.000*cm.hsize]): F_psettings()
        else: F_slideshow(menu.sshw.check+1, N-1)
    if button:
        if button == 'enter': return
        if button == 'up':    CHANGE_SLIDE("back", slideshow.styl)
        if button == 'down':  CHANGE_SLIDE("next", slideshow.styl)
        
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
                LOAD(directory + "menu_reg.pgm", 1) 
                DISPLAY(wfm_Disp.best, 'full') 
            if slideshow.wfm[N] == wfm_Disp.fast: 
                LOAD(directory + "menu_reg.pgm", 1)
                DISPLAY(wfm_Disp.fast, 'full')  
            if slideshow.wfm[N] == wfm_Disp.strd: 
                LOAD(directory + "menu_reg.pgm", 1)
                DISPLAY(wfm_Disp.strd, 'full')
                
        device.sect = 'psettings' # set new device section
        LOAD(directory + "tmp_psettings.pgm", 1)   
        WINDOW_HEADER('Slideshow settings')  
        BUTTONS(pset, 'no display')
   
        DISPLAY(wfm_Disp.text, 'part')
            
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
            
            elif TOUCH_ZONE([.0000*cm.wsize,.9375*cm.hsize], [.1493*cm.wsize,1.000*cm.hsize]): F_brightness() # Brightness button           
            elif TOUCH_ZONE([.1493*cm.wsize,.8854*cm.hsize], [.3125*cm.wsize,1.000*cm.hsize]): F_lighting()   # Lighting button
            elif TOUCH_ZONE([.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,1.000*cm.hsize]): pass#SKETCH("screen")     # Sketch button 
            elif TOUCH_ZONE([.8507*cm.wsize,.8854*cm.hsize], [1.000*cm.wsize,1.000*cm.hsize]): F_pause()  # Settings button
            elif TOUCH_ZONE([.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]): F_pause()  # Exit button  
        
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
#------ BRIGHTNESS MENU -----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------- 
    
def F_brightness(): # BRIGHTNESS MENU

    # ----- LOADING CONTENT ------------
    b_Check = directory + "check_brightness.pgm"; b_Uncheck = directory + "uncheck_brightness.pgm"
    LOAD(directory + "menu_brightness.pgm", 1)
    CLOCK('set')
    if origin == 'slideshow':
        tmp = TEXT_TO_IMAGE(str(N + 1) + '/' + str(len(slideshow.file)), 'Serif_DejaVu.ttf', 50, directory + "blank_slidenumberpause.pgm")   
        LOAD_AREA(tmp, 1, (3,0))
    
    # ----- DISPLAYING CONTENT ------------
    if   origin == 'main':
        BUTTONS(menu.bght, 'display', b_Check, b_Uncheck)
    elif origin == 'slideshow':
        if slideshow.wfm[N] != wfm_Disp.text: 
            DISPLAY(slideshow.wfm[N], 'part')
        else:
            DISPLAY(wfm_Disp.text, 'part')  
        BUTTONS(pset, 'display') 
        BUTTONS(menu.bght, 'display', b_Check, b_Uncheck)
        
    # ----- STAY IN MENU UNTIL SPECIFIED -----------
    while True:   
        
        # ----- WAITING FOR INPUT ----------
        GET_INPUT() 
        if touch:            
            if   TOUCH_ZONE([.0000*cm.wsize,.5130*cm.hsize], [.2778*cm.wsize,.5771*cm.hsize]): CHECK(menu.bght, 0, 'display', b_Check, b_Uncheck); AURORA(100)
            elif TOUCH_ZONE([.0000*cm.wsize,.5771*cm.hsize], [.2778*cm.wsize,.6406*cm.hsize]): CHECK(menu.bght, 1, 'display', b_Check, b_Uncheck); AURORA(80)
            elif TOUCH_ZONE([.0000*cm.wsize,.6406*cm.hsize], [.2778*cm.wsize,.7042*cm.hsize]): CHECK(menu.bght, 2, 'display', b_Check, b_Uncheck); AURORA(60)
            elif TOUCH_ZONE([.0000*cm.wsize,.7042*cm.hsize], [.2778*cm.wsize,.7677*cm.hsize]): CHECK(menu.bght, 3, 'display', b_Check, b_Uncheck); AURORA(40)
            elif TOUCH_ZONE([.0000*cm.wsize,.7677*cm.hsize], [.2778*cm.wsize,.8313*cm.hsize]): CHECK(menu.bght, 4, 'display', b_Check, b_Uncheck); AURORA(20)
            elif TOUCH_ZONE([.0000*cm.wsize,.8313*cm.hsize], [.2778*cm.wsize,.8948*cm.hsize]): CHECK(menu.bght, 5, 'display', b_Check, b_Uncheck); AURORA(0)
            elif TOUCH_ZONE([.1493*cm.wsize,.8854*cm.hsize], [.3125*cm.wsize,1.000*cm.hsize]): F_lighting()
            elif TOUCH_ZONE([.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,1.000*cm.hsize]): pass#SKETCH("screen") 
            elif TOUCH_ZONE([.0000*cm.wsize,.9375*cm.hsize], [.1493*cm.wsize,1.000*cm.hsize]): 
                if   origin == 'main': F_msettings()
                elif origin == 'slideshow': F_psettings()
            else: break
                    
        if button: # if the up/down button was pressed, moves appropriately using BUTTONS()
            BUTTONS(menu.bght, 'display', b_Check, b_Uncheck)
            if menu.bght.check == 0: AURORA(100)
            if menu.bght.check == 1: AURORA(80)
            if menu.bght.check == 2: AURORA(60)
            if menu.bght.check == 3: AURORA(40)
            if menu.bght.check == 4: AURORA(20)
            if menu.bght.check == 5: AURORA(0)
  
#-----------------------------------------------------------------------------------------------
#------ DISP/FLSH MENU -------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------- 

def F_dispflsh():
    
    # ----- LOADING CONTENT ------------
    LOAD(directory + "menu_dispflsh.pgm", 1)
    WINDOW_HEADER('Display/Flash menu')

    # ----- DISPLAYING CONTENT (W/O BUTTONS) ------------   
    DISPLAY(wfm_Disp.text, 'full') # Since always displaying over a previous menu, text display wfm#3 will always work 
        
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
            elif TOUCH_ZONE([.0000*cm.wsize,.9375*cm.hsize], [.1493*cm.wsize,1.000*cm.hsize]): F_brightness()           
            elif TOUCH_ZONE([.1493*cm.wsize,.8854*cm.hsize], [.3125*cm.wsize,1.000*cm.hsize]): F_lighting()
            elif TOUCH_ZONE([.6910*cm.wsize,.8854*cm.hsize], [.8507*cm.wsize,1.000*cm.hsize]): pass # SKETCH("screen") 
            elif TOUCH_ZONE([.6736*cm.wsize,.1771*cm.hsize], [.7708*cm.wsize,.2396*cm.hsize]): return 'back'  
            elif TOUCH_ZONE([.7743*cm.wsize,.1781*cm.hsize], [.8590*cm.wsize,.2417*cm.hsize]): return 'exit' # exit button 
            elif TOUCH_ZONE([.8507*cm.wsize,.8854*cm.hsize], [1.000*cm.wsize,1.000*cm.hsize]): return 'exit' # settings button
            else: continue
        
#-----------------------------------------------------------------------------------------------
#------ CHANGE SLIDE NUMBER --------------------------------------------------------------------
#----------------------------------------------------------------------------------------------- 
        
def F_gotoslide():
    
    # ----- LOADING CONTENT ------------
    LOAD(directory + 'menu_gotoslide.pgm', 1)  
    WINDOW_HEADER('Go-to-slide menu')  
    GET_SLIDE((849, 617))
    slide = ""   
    
    while True:        
        s_Check = directory + "check_bar.pgm"; s_Uncheck = directory + "uncheck_bar.pgm"
        BUTTONS(menu.sshw, "no display", s_Check, s_Uncheck)

        img = Image.open(directory + "blank_gotoslide.pgm")
        I1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/Serif_DejaVu.ttf", 80)
        I1.text((10, 10), slide, font=myFont, fill=0)
        
        img.save(directory + "tmp_gotoslide.pgm")
        LOAD_AREA(directory + 'tmp_gotoslide.pgm', 1, (758, 743))        
        DISPLAY(wfm_Disp.text, 'part')
        
        GET_INPUT()
        if touch:
            if   TOUCH_ZONE([760,490],  [860,610]):   CHECK(menu.sshw, 0, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(1); GET_SLIDE((849, 617))
            elif TOUCH_ZONE([876,490],  [976,610]):   CHECK(menu.sshw, 1, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(2); GET_SLIDE((849, 617))
            elif TOUCH_ZONE([992,490], [1092,610]):   CHECK(menu.sshw, 2, None, s_Check, s_Uncheck); CHANGE_SLIDESHOW(3); GET_SLIDE((849, 617))

            elif TOUCH_ZONE([440,940],  [627,1080]):  slide = slide + '7'
            elif TOUCH_ZONE([627,940],  [813,1080]):  slide = slide + '8'
            elif TOUCH_ZONE([813,940],  [1000,1080]): slide = slide + '9'
            elif TOUCH_ZONE([440,1080], [627,1220]):  slide = slide + '4' 
            elif TOUCH_ZONE([627,1080], [813,1220]):  slide = slide + '5'  
            elif TOUCH_ZONE([813,1080], [1000,1220]): slide = slide + '6' 
            elif TOUCH_ZONE([440,1220], [627,1360]):  slide = slide + '1'
            elif TOUCH_ZONE([627,1220], [813,1360]):  slide = slide + '2' 
            elif TOUCH_ZONE([813,1220], [1000,1360]): slide = slide + '3'
            elif TOUCH_ZONE([627,1360], [813,1500]):  slide = slide + '0'
            elif TOUCH_ZONE([440,1360], [627,1500]):  # BACK
                slide = slide[:-1]
                if len(slide) == 0: slide = ""
            elif TOUCH_ZONE([813,1360], [1000,1500]): # ENTER
                if int(slide) >= len(slideshow.file):
                    print(int(slide))
                    print(len(slideshow.file))
                    slide = len(slideshow.file)
                F_slideshow(menu.sshw.check + 1, int(slide) - 2); F_main()
            elif TOUCH_ZONE([760,1710],   [990,1920]): F_lighting()
            elif TOUCH_ZONE([1000,1760], [1215,1920]): pass#SKETCH("screen") 
            elif TOUCH_ZONE([970,340],    [1110,460]): return 'back'  
            elif TOUCH_ZONE([1110,340],   [1240,460]): return 'exit' 
            elif TOUCH_ZONE([1240,1760], [1440,1920]): return 'exit' #settings
            
            else: continue
   
#-----------------------------------------------------------------------------------------------
#------ LIGHTING MENU --------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
             
""" device.sect can be 'main', 'pause', or 'psettings' """
def F_lighting():
    LOAD(directory + "tmp_lighting.pgm", 1)  
    WINDOW_HEADER('Lighting menu')   
    button_Location = 0
    BUTTONS(lght, 'no display')
    
    while True:
        if device.sect == 'pause':
            if   slideshow.wfm[N] == wfm_Disp.best: 
                DISPLAY(wfm_Disp.best, 'full') # Can this transition to a display of 3?
            elif slideshow.wfm[N] == wfm_Disp.fast: 
                DISPLAY(wfm_Disp.fast, 'full')  
            elif slideshow.wfm[N] == wfm_Disp.text:
                DISPLAY(wfm_Disp.text, 'part')
            elif slideshow.wfm[N] == wfm_Disp.strd: 
                DISPLAY(wfm_Disp.fast, 'full')    
            device.sect = 'psettings' # lighting menu when paused considered a part of 'psettings'
        elif device.sect == 'psettings':
            DISPLAY(wfm_Disp.text, 'part')
        elif device.sect == 'main':   
            DISPLAY(wfm_Disp.text, 'part')
            
        GET_INPUT()
        if touch:# Touch takes priority over button
            command = MENU_TOUCH(lght)
            if   command == 0: os.system('daymode');   lght.location = 0
            elif command == 1: os.system('nightmode'); lght.location = 1
            elif command == 2: os.system('amber');     lght.location = 2
            elif command == 3: os.system('bluemode');  lght.location = 3
            
            elif TOUCH_ZONE([0,1800],     [215,1920]): F_brightness()
            elif TOUCH_ZONE([760,1710],   [990,1920]): #lighting button
                if   device.sect == 'main': F_main()
                elif device.sect == 'psettings': F_pause()
            elif TOUCH_ZONE([1000,1760], [1215,1920]): pass #SKETCH("screen") 
            elif TOUCH_ZONE([1115,342],   [1237,464]): #exit
                if   device.sect == 'main':  F_main()
                elif device.sect == 'psettings': F_pause()
            elif TOUCH_ZONE([1240,1760], [1440,1920]): #settings
                if   device.sect == 'main': F_msettings()
                elif device.sect == 'psettings': F_psettings()
            else: # press off of screen somewhere
                if   device.sect == 'main': F_main()
                elif device.sect == 'psettings': F_pause()                
            
        if button:
            if select == 0: os.system('daymode');   button_Location = 0
            if select == 1: os.system('nightmode'); button_Location = 1
            if select == 2: os.system('amber');     button_Location = 2
            if select == 3: os.system('bluemode');  button_Location = 3

#-----------------------------------------------------------------------------------------------
#------ ROTATION MENU --------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------  
            
def F_rotation():
    r_Check = directory + "check_bar.pgm"; r_Uncheck = directory + "uncheck_bar.pgm"
    LOAD(directory + "menu_rotation.pgm", 1)

    while True:
        data = GET_DATA('rot', 'slideshow')
        WINDOW_HEADER('Rotation menu')
        CHECK(menu.rot, int(data), 'no display', r_Check, r_Uncheck)
        DISPLAY(wfm_Disp.text, 'part')
        
        GET_INPUT()
        if touch:
            if   TOUCH_ZONE([470,900],    [670,1100]): CHECK(menu.rot, 0, None, r_Check, r_Uncheck); REPLACE_DATA('rot', 0, 'slideshow');
            elif TOUCH_ZONE([770,900],    [970,1100]): CHECK(menu.rot, 1, None, r_Check, r_Uncheck); REPLACE_DATA('rot', 1, 'slideshow'); 
            elif TOUCH_ZONE([470,1200],   [670,1400]): CHECK(menu.rot, 2, None, r_Check, r_Uncheck); REPLACE_DATA('rot', 2, 'slideshow');
            elif TOUCH_ZONE([770,1200],   [970,1400]): CHECK(menu.rot, 3, None, r_Check, r_Uncheck); REPLACE_DATA('rot', 3, 'slideshow');
            elif TOUCH_ZONE([760,1710],   [990,1920]): F_lighting()
            elif TOUCH_ZONE([1000,1760], [1215,1920]): pass#SKETCH("screen") 
            elif TOUCH_ZONE([970,340],    [1110,460]): return 'back'  
            elif TOUCH_ZONE([1110,340],   [1240,460]): return 'exit' 
            elif TOUCH_ZONE([1240,1760], [1440,1920]): return 'exit' 
            else: continue
        
#-----------------------------------------------------------------------------------------------
#------ WAVEFORM MENU --------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------  
        
def F_wfm():
    w_Check = directory + "check_bar.pgm"; w_Uncheck = directory + "uncheck_bar.pgm"

    LOAD(directory + "menu_wfm.pgm", 1)
    WINDOW_HEADER('Waveform menu')
    
    if device.sect == 'psettings':
        while True:
            data = GET_DATA('wfm', 'slideshow')
            CHECK(menu.wfms, int(data), 'no display', w_Check, w_Uncheck)
            DISPLAY(wfm_Disp.text, 'part')
            GET_INPUT()
            if touch:
                if   TOUCH_ZONE([300,900],    [510,1100]): CHECK(menu.wfms, 0, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 0, 'slideshow');
                elif TOUCH_ZONE([510,900],    [720,1100]): CHECK(menu.wfms, 1, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 1, 'slideshow');
                elif TOUCH_ZONE([720,900],    [930,1100]): CHECK(menu.wfms, 2, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 2, 'slideshow');
                elif TOUCH_ZONE([930,900],   [1140,1100]): CHECK(menu.wfms, 3, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 3, 'slideshow'); 
                elif TOUCH_ZONE([300,1100],   [510,1300]): CHECK(menu.wfms, 4, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 4, 'slideshow');
                elif TOUCH_ZONE([510,1100],   [720,1300]): CHECK(menu.wfms, 5, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 5, 'slideshow');
                elif TOUCH_ZONE([720,1100],   [930,1300]): CHECK(menu.wfms, 6, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 6, 'slideshow');
                elif TOUCH_ZONE([930,1100],  [1140,1300]): CHECK(menu.wfms, 7, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 7, 'slideshow');  
                elif TOUCH_ZONE([760,1710],   [990,1920]): F_lighting()
                elif TOUCH_ZONE([1000,1760], [1215,1920]): pass#SKETCH("screen") 
                elif TOUCH_ZONE([970,340],    [1110,460]): return 'back'  
                elif TOUCH_ZONE([1110,340],   [1240,460]): return 'exit' 
                elif TOUCH_ZONE([1240,1760], [1440,1920]): return 'exit' 
                else: continue
        
    elif device.sect == 'main':
        image = 'banner'
        while True:
            data = GET_DATA('wfm', image) # Get data first, so screens pop up around the same time
            if   image == 'banner':  LOAD(directory + 'menu_wfm_banner.pgm', 1)
            elif image == 'main':    LOAD(directory + 'menu_wfm_main.pgm', 1)
            elif image == 'startup': LOAD(directory + 'menu_wfm_startup.pgm', 1)
            elif image == 'check':   LOAD(directory + 'menu_wfm_checkicons.pgm', 1)
            WINDOW_HEADER('Waveform menu')
            CHECK(menu.wfmm, int(data), 'display', w_Check, w_Uncheck)
            DISPLAY(wfm_Disp.text, 'part')    
            GET_INPUT()
            if touch:
                if   TOUCH_ZONE([300,1040],   [510,1240]): CHECK(menu.wfmm, 0, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 0, image);
                elif TOUCH_ZONE([510,1040],   [720,1240]): CHECK(menu.wfmm, 1, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 1, image);
                elif TOUCH_ZONE([720,1040],   [930,1240]): CHECK(menu.wfmm, 2, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 2, image);
                elif TOUCH_ZONE([930,1040],  [1140,1240]): CHECK(menu.wfmm, 3, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 3, image);
                elif TOUCH_ZONE([300,1240],   [510,1440]): CHECK(menu.wfmm, 4, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 4, image); 
                elif TOUCH_ZONE([510,1240],   [720,1440]): CHECK(menu.wfmm, 5, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 5, image);
                elif TOUCH_ZONE([720,1240],   [930,1440]): CHECK(menu.wfmm, 6, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 6, image);
                elif TOUCH_ZONE([930,1240],  [1140,1440]): CHECK(menu.wfmm, 7, None, w_Check, w_Uncheck); REPLACE_DATA('wfm', 7, image);
                elif TOUCH_ZONE([220,500],     [470,650]): image = 'banner'
                elif TOUCH_ZONE([470,500],     [720,650]): image = 'main'
                elif TOUCH_ZONE([720,500],     [970,650]): image = 'startup'
                elif TOUCH_ZONE([970,500],    [1220,650]): image = 'check'  
                elif TOUCH_ZONE([760,1710],   [990,1920]): F_lighting() 
                elif TOUCH_ZONE([1000,1760], [1215,1920]): pass#SKETCH("screen")
                elif TOUCH_ZONE([970,340],    [1110,460]): return 'back'  
                elif TOUCH_ZONE([1110,340],   [1240,460]): return 'exit' 
                elif TOUCH_ZONE([1240,1760], [1440,1920]): return 'exit' # self
                else: continue       

#################################################################################################################################################################
# UTILITY FUNCTIONS #############################################################################################################################################
#################################################################################################################################################################

def APP_SELECTOR(arg):
    slideshow_number = 1
    app_List = [cm.app1, cm.app2, cm.app3, cm.app4, cm.app5]
    for i in range(arg):
        print(i);print(arg); print(slideshow_number); print(app_List[i].form)
        if   app_List[i].form == 'slideshow': 
            if    i+1 == arg: F_slideshow(slideshow_number)
            else: slideshow_number += 1
        elif app_List[i].form == 'sketch': 
            if    i+1 == arg: SKETCH('app')

def AURORA(brt):  
    """
    Call this function with at least 1 argument to set the lighting brightness.
    brt1: the brightness value(0-100) of LED strip 1
    brt2: the brightness value(0-100) of LED strip 2.
    If no input is given for brt2, LED strip 2 brightness is set to 0.
    
    """
    global button, select, menu
    
    subprocess.call("AURORA_UPDATE=off aurora3 set_brt 4 " + str(brt*(.8)), shell=True)
    subprocess.call("AURORA_UPDATE=off aurora3 set_brt 3 " + str(brt*(.8)), shell=True)
    subprocess.call("AURORA_UPDATE=off aurora3 set_brt 2 " + str(brt*(.8)), shell=True)
    subprocess.call("aurora3 set_brt 1 " + str(brt*(.8)), shell=True)    
    
    menu.bght.check = (100 - int(brt))/20

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
        if disp == 'display': DISPLAY(cm.check.wfm, 'part')
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
    if   disp == 'display': DISPLAY(cm.check.wfm, 'part')
    if   button == 'down': MENU.check = (MENU.check+1)%n
    elif button == 'up': MENU.check = (MENU.check-1)%n
    button = False
    WAIT(100)

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
        LOAD(slideshow.path + slideshow.file[N], slideshow.rot[N])
    elif direction == "back":
        N -= 1; prev = 1; swipe = 'right'
        if N < 0: N = 0 # If already on first slide, remain there
        LOAD(slideshow.path + slideshow.file[N], slideshow.rot[N])
    elif direction == "back two":
        N -= 2; prev = 2; swipe = 'right'
        if N < 0: N = 0 # If already on first slide, remain there
        LOAD(slideshow.path + slideshow.file[N], slideshow.rot[N])    
    elif direction == "remain": 
        if style == None:
            DISPLAY(slideshow.wfm[N], slideshow.disp[N])            
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
            else: DISPLAY(slideshow.wfm[N], slideshow.disp[N])           
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
    global slideshow; N
    """
    Clears the current screen. Takes one of 5 arguments: 'slideshow', 'full', 'fast', 'strd', 'best', or 'none'
    'slideshow': Manages clearing before the current slide in the slideshow, based on user specifications and recommendations
    The other arguments can be user designated in the program or read from the charmr_module
    Auto flash is set to 'norm' (standard display white flash)
    """ 
    if  flsh == 'full': 
        LOAD(directory + 'white240.pgm', 1); 
        subprocess.call("bs_disp_" + disp + " 0", shell = True)    
    elif flsh == 'text': 
        LOAD(directory + 'white240.pgm', 1); 
        subprocess.call("bs_disp_" + disp + " 3", shell = True)
    elif flsh == 'fast':   
        LOAD(directory + 'white240.pgm', 1); 
        subprocess.call("bs_disp_" + disp + " 4", shell = True)
    elif flsh == 'strd': 
        LOAD(directory + 'white240.pgm', 1); 
        subprocess.call("bs_disp_" + disp + " 2", shell = True)
    elif flsh == 'best': 
        LOAD(directory + 'white240.pgm', 1); 
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
            LOAD_AREA(time_Written, 1, cm.area.clock[0])
        else: 
            LOAD_AREA(time_Written, 1, cm.area.clock[1])
        if arg != "load":
            DISPLAY(wfm_Disp.text, "part")
        
def COMMAND(string, call):
    if   call == 'sub':   subprocess.call(string, shell = True)
    elif call == 'os':    os.system(string)
    elif call == 'Popen': subprocess.Popen(string, stdout=subprocess.PIPE, shell = True)

def DISPLAY(wfm, method = 'full'):
    subprocess.call('bs_disp_' + method + ' ' + str(wfm), shell = True)
              
def DISPLAY_AREA(wfm, pos1, pos2):
    """
    Displays the image loaded into the buffer.
    wfm: The waveform number used in displaying
    method = 'full' or 'part': 'full' updates the entire area while 'part' only updates pixels of different values
    pos1, pos2: The area on the screen to be displayed. 
        Measured as (x,y) from the top left of the screen, pos1 is the top left corner of the display area (x1,y1) 
        and pos2 is the bottom right corner of the display area (x2,y2), making a rectangle of area (x2-x1) * (y2-y1)
    """
    global rotation_Current, slideshow, N
  
    X = ' '; SSX = cm.hsize; SSY = cm.wsize
    if   rotation_Current == 1:
        COMMAND('bs_disp_full_area ' + str(wfm) +X+ str(pos1[0]) +X+ str(pos1[1]) +X+ str(pos2[0]-pos1[0]) +X+ str(pos2[1]-pos1[1]), 'sub')
    elif rotation_Current == 0: 
        COMMAND('bs_disp_full_area ' + str(wfm) +X+ str(SSY - pos1[1]) +X+ str(pos1[0]) +X+ str(pos2[1]-pos1[1]) +X+ str(pos2[0] - pos1[0]), 'sub') 
    elif rotation_Current == 2:
        COMMAND('bs_disp_full_area ' + str(wfm) +X+ str(pos1[1]) +X+ str(SSX - pos1[0]) +X+ str(pos2[1]-pos1[1]) +X+ str(pos2[0] - pos1[0]) + ' block_rails_active', 'sub') 
    elif rotation_Current == 3:
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
    global slideshow, N
    img = Image.open(directory + "blank_gotoslide.pgm")
    I1 = ImageDraw.Draw(img)
    I1.fontmode = "1"
    myFont = ImageFont.truetype(r"/mnt/mmc/images/charmr/TrueTypeFonts/Serif_DejaVu.ttf", 80)
    I1.text((10, 10), str(N + 1) + '/' + str(len(slideshow.file)), font=myFont, fill=0)
    img.save(directory + 'tmp_currentslide.pgm')
    LOAD_AREA(directory + 'tmp_currentslide.pgm', 1, arg)
    
def LOAD(img, rot):
    global rotation_Current
    rotation_Current = rot
    subprocess.call('bs_load_img ' + str(rot) + ' ' + str(img), shell = True)
    
def LOAD_AREA(img, rot, pos):
    X = ' '; SSX = cm.hsize; SSY = cm.wsize
    if   str(rot) == '1':
        subprocess.call('bs_load_img_area ' + str(rot) +X+ str(pos[0]) +X+ str(pos[1]) +X+ str(img), shell = True)
    elif str(rot) == '0':
        subprocess.call('bs_load_img_area ' + str(rot) +X+ str(SSY - pos1[1]) +X+ str(pos1[0]) +X+ str(img), shell = True)
    elif str(rot) == '2':
        subprocess.call('bs_load_img_area ' + str(rot) +X+ str(pos[1]) +X+ str(SSX - pos[0]) +X+ str(img), shell = True)
    elif str(rot) == '3': 
        subprocess.call('bs_load_img_area ' + str(rot) + ' ' + str(SSX - pos[0]) + ' ' + str(SSY - pos[1]) + ' ' + str(img), shell = True)

def LOAD_SAVED_WB():
    subprocess.call("SET_SPECIFIC_TEMP=25 PWRDOWN_DELAY=10 /mnt/mmc/api/tools/cmder bs_load_img 1 tmp/prevwb", shell=True)

def MENU_BUILD(menu_Type, name = "", items = []):
    if   int(cm.wsize) == 1440 and int(cm.hsize) == 1920: 
        if   menu_Type == 'main': 
            img = directory + "menu_main.pgm"
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
        if TOUCH_ZONE([x1,math.ceil(.4219*cm.hsize)], [x2,math.ceil(.5260*cm.hsize)]): CHECK(button_List, 0, 'display'); return 0
    elif len(button_List.locations) == 2:
        if TOUCH_ZONE([x1,math.ceil(.3281*cm.hsize)], [x2,math.ceil(.4375*cm.hsize)]): CHECK(button_List, 0, 'display'); return 0
        if TOUCH_ZONE([x1,math.ceil(.5313*cm.hsize)], [x2,math.ceil(.6458*cm.hsize)]): CHECK(button_List, 1, 'display'); return 1       
    elif len(button_List.locations) == 3:
        if TOUCH_ZONE([x1,math.ceil(.4323*cm.hsize)], [x2,math.ceil(.5417*cm.hsize)]): CHECK(button_List, 1, 'display'); return 1
        if TOUCH_ZONE([x1,math.ceil(.5729*cm.hsize)], [x2,math.ceil(.6771*cm.hsize)]): CHECK(button_List, 2, 'display'); return 2
    elif len(button_List.locations) == 4:
        if TOUCH_ZONE([x1,math.ceil(.2917*cm.hsize)], [x2,math.ceil(.3958*cm.hsize)]): CHECK(button_List, 0, 'display'); return 0
        if TOUCH_ZONE([x1,math.ceil(.3958*cm.hsize)], [x2,math.ceil(.5104*cm.hsize)]): CHECK(button_List, 1, 'display'); return 1
        if TOUCH_ZONE([x1,math.ceil(.5104*cm.hsize)], [x2,math.ceil(.6250*cm.hsize)]): CHECK(button_List, 2, 'display'); return 2
        if TOUCH_ZONE([x1,math.ceil(.6250*cm.hsize)], [x2,math.ceil(.7292*cm.hsize)]): CHECK(button_List, 3, 'display'); return 3  
    elif len(button_List.locations) == 5:
        if TOUCH_ZONE([x1,math.ceil(.2708*cm.hsize)], [x2,math.ceil(.3593*cm.hsize)]): CHECK(button_List, 0, 'display'); return 0
        if TOUCH_ZONE([x1,math.ceil(.3593*cm.hsize)], [x2,math.ceil(.4583*cm.hsize)]): CHECK(button_List, 1, 'display'); return 1
        if TOUCH_ZONE([x1,math.ceil(.4583*cm.hsize)], [x2,math.ceil(.5521*cm.hsize)]): CHECK(button_List, 2, 'display'); return 2
        if TOUCH_ZONE([x1,math.ceil(.5521*cm.hsize)], [x2,math.ceil(.6458*cm.hsize)]): CHECK(button_List, 3, 'display'); return 3
        if TOUCH_ZONE([x1,math.ceil(.6458*cm.hsize)], [x2,math.ceil(.7292*cm.hsize)]): CHECK(button_List, 4, 'display'); return 4

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

def SKETCH(arg):
    """
    Call to sketch on the screen. Takes optional argument 'app'
    'app': Calls the main application ACePsketch 
    no argument: Allows user to draw on the screen on the spot.
    """
    global slideshow, N
    if   arg == 'app':
        subprocess.call("cd /mnt/mmc/application/sketch", shell = True)
        subprocess.call("FULL_WFM_MODE=4 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/" + cm.sketch_App + ".txt", shell = True)        
        F_main()
    elif arg == 'sketch':
        subprocess.call("cd /mnt/mmc/application/sketch", shell = True)
        os.system("FULL_WFM_MODE=4 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/colorpen_sketch_fast.txt")        
        if N != None:
            LOAD(str(slideshow.path) + str(slideshow.file[N]), slideshow.rot[N])
            DISPLAY(slideshow.wfm[N], 'part')
            LOAD(directory + 'pause.pgm', 1)
        else: 
            LOAD(cm.main.file, cm.main.rot)

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

def TOUCH_ZONE(L1, L2): # Detects whether the touch was in a specific area
    """
    L1 and L2 are tuples at the top left corner and bottom right corner of the touch zone, respectively.
    check is the button number touched, counting from top down (starting at 0)

    """
    global wsize
    if touch[0] > cm.wsize - L2[0] and touch[0] < cm.wsize - L1[0] and touch[1] > L1[1] and touch[1] < L2[1]:   
        return True
    else: return False

def WAIT(t):
    """
    Pauses the program for t milliseconds
    """
    time.sleep(t/1000)
    
def WINDOW_HEADER(text):
    header = TEXT_TO_IMAGE(text, 'Sans_ZagReg.otf', 60, directory + "blank_window_header.pgm")
    LOAD_AREA(header, 1, (250,368))  
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SNAKE GAME :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                          

def F_snake():
    global touch
    score = 0
    food_Replace = True
    gameover = False
    
    # Initialize 10x10 grid, each pixel contains value food=True/False and body=True/False
    # All body segments counted nmbr = 0 to N, starting from head. All non-body segments are nmbr = -1
    grid = np.ndarray((10,10), dtype=np.object) 
    for i in range(10):
        for j in range(10):
            grid[i][j] = SNAKE_ATTRIBUTES(False, False, -1)
           
    touch_proc = subprocess.Popen('get_touch -d 10000 -n', stdout=subprocess.PIPE, shell=True) # Start touch detect

    LOAD(directory + "snake_screen.pgm", 1) 
    DISPLAY(5)
    WAIT(500)

    I = 1; J = 4
    move = np.array([1,0])
    grid[I][J].body=True; grid[I][J].nmbr = 0 # Snake head
        
    hiscore = GET_DATA('hscr', 'snake')
    name = GET_DATA('name', 'snake')
    
    tmp = TEXT_TO_IMAGE(str(int(hiscore)), 'Pixel_GBB.ttf', 60, directory + "blank_hi-score.pgm")
    LOAD_AREA(tmp, 1, (299,633))  
    
    tmp = TEXT_TO_IMAGE(str(score), 'Pixel_GBB.ttf', 60, directory + "blank_score.pgm")
    LOAD_AREA(tmp, 1, (222,490))      

    tmp = TEXT_TO_IMAGE(name[1:-2], 'Pixel_GBB.ttf', 60, directory + "blank_snake_name.pgm")
    LOAD_AREA(tmp, 1, (185,708))  
    
#---------------------------------------------------------------------------------------------------------------------------
# BEGIN GAME
#---------------------------------------------------------------------------------------------------------------------------    
    while gameover == False:       
        gameover = True
                
        if food_Replace == True: # Place food if not already on screen   
            random1 = np.random.randint(0, 9)
            random2 = np.random.randint(0, 9)
            while grid[random1,random2].body == True: # Find location for food snake doesn't exist in
                random1 = np.random.randint(0, 9)
                random2 = np.random.randint(0, 9)
            grid[random1][random2].food = True
            random1 = random1*50 + 470
            random2 = random2*50 + 500
            LOAD_AREA_FAST(directory + "snake_block.pgm", 1, (random1, random2))
            food_Replace = False
            
        touch_proc = subprocess.Popen('get_touch -d 10000 -n', stdout=subprocess.PIPE, shell=True) # Start touch detect        
#---------------------------------------------------------------------------------------------------------------------------
# BEGIN MOVEMENT ITERATIONS
#---------------------------------------------------------------------------------------------------------------------------    
        while True: 

            newtouch = False
            if I + move[0] > 9 or I + move[0] < 0 or J + move[1] < 0 or J + move[1] > 9: break
            
            i=I; j=J # To trace through the snake and keep track of new integers                    
            if grid[i + move[0]][j + move[1]].body == True: break # If the head runs into the body, break out
            if grid[i + move[0]][j + move[1]].food == False: # only erase tail if no food in next spot
                while True: # Find the highest number (Tail), tracing back down the snake
                    if    i<9 and grid[i+1][j].nmbr == grid[i][j].nmbr + 1: grid[i][j].nmbr = grid[i][j].nmbr + 1; i += 1; continue
                    elif  i>0 and grid[i-1][j].nmbr == grid[i][j].nmbr + 1: grid[i][j].nmbr = grid[i][j].nmbr + 1; i -= 1; continue
                    elif  j<9 and grid[i][j+1].nmbr == grid[i][j].nmbr + 1: grid[i][j].nmbr = grid[i][j].nmbr + 1; j += 1; continue
                    elif  j>0 and grid[i][j-1].nmbr == grid[i][j].nmbr + 1: grid[i][j].nmbr = grid[i][j].nmbr + 1; j -= 1; continue
                    else: 
                        grid[i][j].nmbr = -1 # If last in chain, decrease to -1
                        grid[i][j].body = False # No longer a body part
                        LOAD_AREA_FAST(directory + "snake_noblock.pgm", 1, POSITION(i,j)); 
                        break # TAIL ERASED
            else: 
                newtouch = True
                grid[i + move[0]][j + move[1]].food = False
                food_Replace = True
                score += 1
                
                tmp = TEXT_TO_IMAGE(str(score), 'Pixel_GBB.ttf', 70, directory + "blank_score.pgm")
                LOAD_AREA(tmp, 1, (220,480)) 

                while True: 
                    if    i<9 and grid[i+1][j].nmbr == grid[i][j].nmbr + 1: grid[i][j].nmbr = grid[i][j].nmbr + 1; i += 1; continue
                    elif  i>0 and grid[i-1][j].nmbr == grid[i][j].nmbr + 1: grid[i][j].nmbr = grid[i][j].nmbr + 1; i -= 1; continue
                    elif  j<9 and grid[i][j+1].nmbr == grid[i][j].nmbr + 1: grid[i][j].nmbr = grid[i][j].nmbr + 1; j += 1; continue
                    elif  j>0 and grid[i][j-1].nmbr == grid[i][j].nmbr + 1: grid[i][j].nmbr = grid[i][j].nmbr + 1; j -= 1; continue
                    else: 
                        grid[i][j].nmbr = grid[i][j].nmbr + 1 # If last in chain, increase as well
                        LOAD_AREA_FAST(directory + "snake_block.pgm", 1, POSITION(i,j)); # To keep time frame steps equal
                        break  
                    
            if touch_proc.returncode is not None:
                touch, err = touch_proc.communicate()
                touch_Split = touch.split(', ')
                tx = int(touch_Split[0]); ty = int(touch_Split[1])
                touch = [tx, ty]    
                if   TOUCH_ZONE([655,1184],   [787,1310]): 
                    if move[1] == 1: pass
                    else: move = np.array([0, -1]) # UP
                elif TOUCH_ZONE([655,1482],   [787,1613]): 
                    if move[1] == -1: pass
                    else: move = np.array([0, 1]) # DOWN
                elif TOUCH_ZONE([506,1331],   [636,1466]): 
                    if move[0] == 1: pass
                    else: move = np.array([-1, 0]) # LEFT
                elif TOUCH_ZONE([812,1331],   [935,1466]): 
                    if move[0] == -1: pass
                    else: move = np.array([1, 0]); # RIGHT
                elif TOUCH_ZONE([0,1740],     [350,1920]): F_snake()
                elif TOUCH_ZONE([1090,1740], [1440,1920]): F_main()   
                newtouch = True
                break
                    
            I = I + move[0]; J = J + move[1]  # Officially change the head position integers                      
            LOAD_AREA_FAST(directory + "snake_block.pgm", 1, POSITION(I, J)) # LOAD HEAD TO NEXT POSITION   
            grid[I, J].body = True; grid[I, J].nmbr = 0 # Change head attributes
            DISPLAY(3, 'part')
            touch_proc.poll()
            if touch_proc.returncode is not None:
                touch, err = touch_proc.communicate()
                touch_Split = touch.split(', ')
                tx = int(touch_Split[0]); ty = int(touch_Split[1])
                touch = [tx, ty]    
                if   TOUCH_ZONE([655,1184],   [787,1310]): move = np.array([0, -1]) # UP
                elif TOUCH_ZONE([655,1482],   [787,1613]): move = np.array([0, 1]) # DOWN
                elif TOUCH_ZONE([506,1331],   [636,1466]): move = np.array([-1, 0]) # LEFT
                elif TOUCH_ZONE([812,1331],   [935,1466]): move = np.array([1, 0]); # RIGHT
                elif TOUCH_ZONE([0,1740],     [350,1920]): F_snake()
                elif TOUCH_ZONE([1090,1740], [1440,1920]): F_main()   
                newtouch = True
            if newtouch: gameover = False; break
    
    if int(score) > int(hiscore): 
        REPLACE_DATA('hscr', score, 'snake')
        LOAD(directory + "snake_hi-score.pgm", 1)
        DISPLAY(5, "part")
        name = ""
        while True:
            GET_INPUT()
            if touch:
                if   TOUCH_ZONE([111,1151],   [231,1271]): name = name + 'Q'
                elif TOUCH_ZONE([231,1151],   [351,1271]): name = name + 'W'
                elif TOUCH_ZONE([351,1151],   [471,1271]): name = name + 'E'
                elif TOUCH_ZONE([471,1151],   [591,1271]): name = name + 'R'
                elif TOUCH_ZONE([591,1151],   [711,1271]): name = name + 'T'
                elif TOUCH_ZONE([711,1151],   [831,1271]): name = name + 'Y'
                elif TOUCH_ZONE([831,1151],   [951,1271]): name = name + 'U'
                elif TOUCH_ZONE([951,1151],  [1071,1271]): name = name + 'I'
                elif TOUCH_ZONE([1071,1151], [1191,1271]): name = name + 'O'
                elif TOUCH_ZONE([1191,1151], [1311,1271]): name = name + 'P'
                elif TOUCH_ZONE([155,1271],   [275,1391]): name = name + 'A'
                elif TOUCH_ZONE([275,1271],   [395,1391]): name = name + 'S'
                elif TOUCH_ZONE([395,1271],   [515,1391]): name = name + 'D'
                elif TOUCH_ZONE([515,1271],   [635,1391]): name = name + 'F'
                elif TOUCH_ZONE([635,1271],   [755,1391]): name = name + 'G'
                elif TOUCH_ZONE([755,1271],   [875,1391]): name = name + 'H'
                elif TOUCH_ZONE([875,1271],   [995,1391]): name = name + 'J'
                elif TOUCH_ZONE([995,1271],  [1115,1391]): name = name + 'K'
                elif TOUCH_ZONE([1115,1271], [1235,1391]): name = name + 'L'
                elif TOUCH_ZONE([210,1391],   [330,1511]): name = name + 'Z'
                elif TOUCH_ZONE([330,1391],   [450,1511]): name = name + 'X'
                elif TOUCH_ZONE([450,1391],   [570,1511]): name = name + 'C'
                elif TOUCH_ZONE([570,1391],   [690,1511]): name = name + 'V'
                elif TOUCH_ZONE([690,1391],   [810,1511]): name = name + 'B'
                elif TOUCH_ZONE([810,1391],   [930,1511]): name = name + 'N'
                elif TOUCH_ZONE([930,1391],  [1050,1511]): name = name + 'M'         
                elif TOUCH_ZONE([1066,1406], [1330,1530]): # DELETE BUTTON
                    name = name[:-1]
                    if len(name) == 0: name = "" 
                elif TOUCH_ZONE([1066,1555], [1370,1690]): 
                    REPLACE_DATA('name', "\'"+str(name)+"\'", 'snake')     
                    LOAD_AREA(directory + "snake_saved.pgm", 1, (540,1750))
                    DISPLAY_AREA(5, (570,1750), (870,1900))
                elif TOUCH_ZONE([0,1740],     [350,1920]): RELOAD(); F_snake()
                elif TOUCH_ZONE([1090,1740], [1440,1920]): RELOAD(); F_main()  
                    
                if len(name) > 3: name = name[:-1] # 3 Character maximum
                
                tmp = TEXT_TO_IMAGE("\'"+name+"\'", 'Pixel_GBB.ttf', 110, directory + "blank_snake_name.pgm")
                LOAD_AREA(tmp, 1, (740,1550)) 

                DISPLAY(4, 'part')
    
    else:        
        LOAD_AREA_FAST(directory + "snake_gameover.pgm", 1, (0, 1140))
        DISPLAY(3, 'part')
        while True:
            GET_INPUT()
            if   TOUCH_ZONE([0,1740],    [350,1920]):  F_snake()
            elif TOUCH_ZONE([1090,1740], [1440,1920]): F_main() 
            
def LOAD_AREA_FAST(img, rot, pos):
    X = ' '
    subprocess.call('bs_load_img_area ' + str(rot) +X+ str(pos[0]) +X+ str(pos[1]) +X+ str(img), shell = True)  
        
def POSITION(i, j):
    value = (470 + (i*50), 500 + (j*50))
    return value    

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
        
#                 1            2            3             4           5             6    
rot_List  = [[526, 1060], [833, 1060], [526, 1357],  [833, 1357]]
bght_List = [[1, 986],    [1, 1108],   [1, 1230],    [1, 1352],   [1, 1474],    [1, 1596]]
disp_List = [[654, 826],  [990, 826]]
flsh_List = [[599, 1108], [822, 1108], [1046, 1108], [599, 1300], [822, 1300]]
auto_List = [1046, 1300]
menu_List = [[270, 620],  [270, 820],  [270, 1020],  [270, 1220]]
sshw_List = [[771, 575],  [887, 575],  [1003, 575]]

main = MENU_CHECK([], 0)
mset = MENU_CHECK([], 0)
pset = MENU_CHECK([], 0)
lght = MENU_CHECK([], 0)
rot  = MENU_CHECK(rot_List, 0)
bght = MENU_CHECK(bght_List, 0)
disp = MENU_CHECK(disp_List, 0)
flsh = MENU_CHECK(flsh_List, 0)
auto = MENU_CHECK(auto_List, 0)
wfmm = MENU_CHECK(wfmm_List, 0)
wfms = MENU_CHECK(wfms_List, 0)
sshw = MENU_CHECK(sshw_List, 0)

# All menus easily accessible
menu = MENUS(main, mset, pset, lght, bght, disp, flsh, auto, wfmm, wfms, rot, sshw)

# Start clearing the screen
CLEAR('best')
CLEAR('full')
CLEAR('text')
if cm.aurora: # If the demo has aurora lighting, set to default values
    COMMAND('daymode', 'sub')
    AURORA(100)
LOAD(cm.startup.file, cm.startup.rot) # load startup screena and display
DISPLAY(cm.startup.wfm, 'part')

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

img, button_List = MENU_BUILD('menu', '_lighting',
                              ['Daymode', 
                               'Nightmode', 
                               'Amber', 
                               'Bluemode']
                               )
lght_List = button_List

main = MENU_CHECK(main_List, 0)
mset = MENU_CHECK(mset_List, 0)
pset = MENU_CHECK(pset_List, 0)
lght = MENU_CHECK(lght_List, 0)

ctme = None # Current time
wifi = None # Detect wifi network
btth = None # Detect bluetooth
batt = None # Detect battery level
sect = None
if 'device.proc' in locals(): # If the demo is restarted but it failed to kill the process at the end, kill now
    os.kill(device.proc, signal.SIGKILL)
proc = os.getpid()

device = DEVICE(ctme, wifi, btth, batt, proc, sect)

# wfm PP1 22-40C 
wfm_Disp = WFM_DISPLAYS(0, 3, 4, 2, 5) # wfm display qualities translated to numbers

# wfm MCC 1466-16-B2 
#wfm_Disp = WFM_DISPLAYS(2, 2, 2, 2, 2)

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