import sys
import subprocess
import numpy as np

from basemenu import BaseMenu

sys.path.append('cmodule')

import charmr_module as cm

import utils as utils

'''
Controls the brightness and temperature settings of the demo
'''
class BrightnessTemperatureMenu(BaseMenu):
    def __init__(self, view, check_file="check_brightness2.pgm", uncheck_file="uncheck_brightness2.pgm"):

        locations = [0]*10
        for i in range(10):
            self.locations = (476+(i*49), 1772)

        super(BrightnessTemperatureMenu, self).__init__(locations, view, check_file, uncheck_file)#locations_list, check_file, uncheck_file)

        # The type of menu being worked with. If 'bght', the brightness of the demo nwill be modified by any given function. If 'temp', the
        # temperature will be modified.
        self.cur_type = "bght"

        # the current brightness/temp of the demo is stroed for easy access
        self.current_brightness = None
        self.current_temperature = None


    '''
    Will change the brightness/temperature of the demo and update the current_brightness/current_temperature field based on the cur_type.
    If the touch location given is not within the brightness/temp touch zones, no change will be made.

    ARGUMENTS
    touch_location: list (x, y coordinates of user touch)
    
    RETURN
    void
    '''
    def brightness_temperature_slider(self, touch_location): 
        #used to be F_brightness/ F_temperature
        change = False
        cur_val = None

        # if touch on brightness/temp button, brightness/temp slider is activated - add support for this


        if utils.touch_zone(touch_location, [[476,1730], [525,1850]]): 
            self.cur_check = 0

            cur_val = 0
            change = True
            #CHECK(menu.bght, 0, 'display', b_Check, b_Uncheck); AURORA(0)

        elif utils.touch_zone(touch_location, [[525,1730], [574,1850]]):
            self.cur_check = 1

            cur_val = 10
            change = True
            #CHECK(menu.bght, 1, 'display', b_Check, b_Uncheck); AURORA(10)

        elif utils.touch_zone(touch_location, [[574,1730], [623,1850]]):
            self.cur_check = 2

            cur_val = 20
            change = True
            #CHECK(menu.bght, 2, 'display', b_Check, b_Uncheck); AURORA(20)

        elif utils.touch_zone(touch_location, [[623,1730], [672,1850]]):
            self.cur_check = 3

            cur_val = 30
            change = True
            #CHECK(menu.bght, 3, 'display', b_Check, b_Uncheck); AURORA(30)

        elif utils.touch_zone(touch_location, [[672,1730], [721,1850]]):
            self.cur_check = 4

            cur_val = 40
            change = True
            #CHECK(menu.bght, 4, 'display', b_Check, b_Uncheck); AURORA(40)
            
        elif utils.touch_zone(touch_location, [[721,1730], [770,1850]]):
            self.cur_check = 5

            cur_val = 50
            change = True
            #CHECK(menu.bght, 5, 'display', b_Check, b_Uncheck); AURORA(50)

        elif utils.touch_zone(touch_location, [[770,1730], [819,1850]]):
            self.cur_check = 6

            cur_val = 60
            change = True
            #CHECK(menu.bght, 6, 'display', b_Check, b_Uncheck); AURORA(60)

        elif utils.touch_zone(touch_location, [[819,1730], [868,1850]]):
            self.cur_check = 7

            cur_val = 70
            change = True
            #CHECK(menu.bght, 7, 'display', b_Check, b_Uncheck); AURORA(70)

        elif utils.touch_zone(touch_location, [[868,1730], [917,1850]]):
            self.cur_check = 8 

            cur_val = 80
            change = True
            #CHECK(menu.bght, 8, 'display', b_Check, b_Uncheck); AURORA(80)

        elif utils.touch_zone(touch_location, [[917,1730], [966,1850]]):
            self.cur_check = 9 

            cur_val = 90
            change = True
            #CHECK(menu.bght, 9, 'display', b_Check, b_Uncheck); AURORA(90)

        if self.cur_type == "temp" and change:
            self.current_temperature = cur_val
            self.set_aurora_temp(self.current_temperature)

        elif self.cur_type == "bght" and change:
            self.current_brightness = cur_val
            self.set_aurora_brightness(self.current_brightness)
        

    '''
    Setter for the cur_type field

    ARGUMENTS
    selected: str (desired type)

    RETURN
    void
    '''
    def select_type(self, selected):
        if selected == "bght":
            self.cur_type = "bght"
            self.view.display_brightness()

        elif selected == "temp":
            self.cur_type = "temp"
            self.view.display_temp()

    '''
    Sets the brightness of the demo

    ARGUMENTS
    brt_val: int (desired brightness)

    RETURN
    void
    '''
    def set_aurora_brightness(self, brt_val):
        #used to be AURORA(brt)
        """
        Call this function with at least 1 argument to set the lighting brightness.
        brt1: the brightness value(0-100) of LED strip 1
        brt2: the brightness value(0-100) of LED strip 2.
        If no input is given for brt2, LED strip 2 brightness is set to 0.
        
        """
        
        subprocess.call("AURORA_UPDATE=off aurora3 set_brt 4 " + str(brt_val), shell=True)
        subprocess.call("AURORA_UPDATE=off aurora3 set_brt 3 " + str(brt_val), shell=True)
        subprocess.call("AURORA_UPDATE=off aurora3 set_brt 2 " + str(brt_val), shell=True)
        subprocess.call("aurora3 set_brt 1 " + str(brt_val), shell=True)
        
        self.view.change_checkmarked_option(self.locations, self.cur_check) 

    ''' 
    Sets the temperature of the demo

    ARGUMENTS
    temp: int (desired temp)

    RETURN
    void
    '''
    def set_aurora_temp(self, temp):
        #used to be AURORA_TEMP(temp) 
        """
        temp can be 0 to 9 (10 different temperatures)
        temp2=20 when temp=0
        temp1=20 when temp=9
        
        """
        
        temp1 = int(np.rint(temp*20/90))
        temp2 = int(np.rint(20-temp*20/90))
        
        subprocess.call("AURORA_UPDATE=off aurora3 set_cur 1 " + str(temp1), shell=True)
        subprocess.call("AURORA_UPDATE=off aurora3 set_cur 2 " + str(temp2), shell=True)
        subprocess.call("AURORA_UPDATE=off aurora3 set_cur 3 " + str(temp1), shell=True)
        subprocess.call("aurora3 set_cur 4 " + str(temp2), shell=True)
        
        self.view.change_checkmarked_option(self.locations, self.cur_check) 

# if __name__ == "__main__":

#     t = BrightnessTemperatureMenu()

#     t.brightness_temperature_slider([5, 5])