# from basemenu import BaseMenu

# import charmr_module as cm
# from view import Display
# import os
# import utils

# class MainSettingsMenu(BaseMenu):

#     def __init__(self, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):
        
#         self.items = ['Go-to-slide', 
#                       'Wfm mode #s',
#                       'Demo mode',
#                       'Restart']
        
#         self.check_file = check_file
#         self.uncheck_file = uncheck_file
#         self.locations = self.menu_build("menu", '_mainsettingsmenu', self.items)
        
#         self.view = Display()
        
#         super(MainSettingsMenu, self).__init__(self.locations, self.check_file, self.uncheck_file)
        
#         super(MainSettingsMenu, self).menu_locations(self.locations, self.cur_check)

#     def display(self):
  
#         # ----- LOADING CONTENT ------------
#         self.view.load(self.view.directory + "tmp_mainsettingsmenu.pgm")  
        
#         # ----- DISPLAYING BUTTONS AND OTHER CONTENT IF NOT YET LOADED
#         self.view.window_header('Main settings')
        
#         self.change_checkmark()
        
#     def change_checkmark(self):
        
#         self.view.change_checkmarked_option(self.locations, self.cur_check) 
    
#     def process_input(self, user_input):
        
#         if type(user_input) == list:  
#             command = super(MainSettingsMenu, self).menu_touch(self.locations) 
#             if   command == 1: pass
#             elif command == 2: pass
#             elif command == 3: pass
#             elif command == 4: pass
            
#             # elif TOUCH_ZONE(TOUCH_DICT['slider']): # BRIGHTNESS/TEMP SLIDER
#             #     if   device.slide == 'bght': F_brightness()
#             #     elif device.slide == 'temp': F_temperature()
#             # elif TOUCH_ZONE(TOUCH_DICT['brightness_button']): BUTTON_BRIGHTNESS('display')
#             # elif TOUCH_ZONE(TOUCH_DICT['temperature_button']): BUTTON_TEMPERATURE('display')      
#             elif utils.touch_zone(user_input, self.touch_dict['settings_button']): 
                
#                 return 'settings_button'
#             # elif TOUCH_ZONE(TOUCH_DICT['exit_button']): F_main()
#             # else: F_main()
            
#         elif type(user_input) == str: # Button pressed
                            
#             if user_input in ['up', 'down']:
#                 super(MainSettingsMenu, self).buttons(user_input) # change the buttons appropriately
                
#                 self.change_checkmark()
                
#             elif user_input == 'enter':
#                 return True

#     def launch_sketch_app(self):
#         os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 

#     def go_to_slide(self):
#         pass
    
#     def wfm_mode_change(self):
#         pass
    
#     def user_mode_change(self): # Change between demo mode and editor mode
#         pass
    
#     def restart(self):
#         pass



from basemenu import BaseMenu

import charmr_module as cm
from view import Display
import os
import utils as utils
import sys
from settingsmenu import SettingsMenu

class MainSettingsMenu(SettingsMenu):

    def __init__(self, view, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):
        
        self.items = ['Go to slide', 
                      'Wfm mode #s',
                      'Demo mode',
                      'Restart']
        
        self.tmp_name = 'mainsettingsmenu'
        
        self.check_file = check_file
        self.uncheck_file = uncheck_file
        self.locations = self.menu_build("menu", self.tmp_name, self.items)
        
        self.view = view

        super(MainSettingsMenu, self).__init__(self.view, self.locations, self.check_file, self.uncheck_file)
        
    def display(self):
                
        self.view.load(self.view.directory + "tmp_" + self.tmp_name + ".pgm") # loads and displays using cmder
        
        self.change_checkmark()
    
    def change_checkmark(self):    
    
        self.view.change_checkmarked_option(self.locations, self.cur_check)    

    def display_go_to_slide(self):
        self.view.load_go_to_slide()

    def process_input(self, user_input):
        if utils.touch_zone(user_input, self.general_touch_dict['exit']):
            self.cur_check = 0
            return 'main'

        elif utils.touch_zone(user_input, self.general_touch_dict['back']):
            self.cur_check = 0
            self.view.display_msettings()

        else: 
            return self.run_app(user_input)

            
 
            
    def run_app(self, user_input):
        if self.cur_check == 1:
            self.retrieve_output(user_input, self.go_to_slide_touch_dict, 'go to slide')
        elif self.cur_check == 2:
            self.retrieve_output(user_input, self.wfm_touch_dict, 'wfm')
        elif self.cur_check == 3:
            pass
            #self.user_mode_change(user_input)


    def launch_sketch_app(self):
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 
    
    def user_mode_change(self, user_input): # Change between demo mode and editor mode
        pass
    
    def restart(self):
        utils.command("kill python " + sys.argv[0] + "; python " + sys.argv[0], "sub")        




