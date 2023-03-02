
from basemenu import BaseMenu
import charmr_module as cm
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


    def process_input(self, user_input):
        if self.cur_check == 0:
            if type(user_input) == str: # Button pressed
                                
                if user_input in ['up', 'down']:
                    self.buttons(user_input) # change the buttons appropriately
                    self.view.change_checkmarked_option(self.locations, self.cur_check) 
                    
                elif user_input == 'enter':
                    #selection = self.cur_check
                    self.view.display_msetting_submenu(self.cur_check)
    
            elif type(user_input) == list: # Screen touched           
                self.cur_check = self.menu_touch(user_input)

                if self.cur_check == 4:
                    self.restart()

        else:
            if utils.touch_zone(user_input, self.general_touch_dict['exit']):
                self.cur_check = 0
                return 'main'

            elif utils.touch_zone(user_input, self.general_touch_dict['back']):
                self.cur_check = 0
                self.view.display_msettings()

            elif self.cur_check == 4:
                self.restart()

            else: 
                return self.run_app(user_input)

            
 
            
    def run_app(self, user_input):
        if self.cur_check == 1:
            self.retrieve_output(user_input, self.go_to_slide_touch_dict, 'go to slide')
        elif self.cur_check == 2:
            self.retrieve_output(user_input, self.wfm_touch_dict, 'wfm')
        elif self.cur_check == 3:
            self.user_mode_change(user_input)


    def launch_sketch_app(self):
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 
    
    def user_mode_change(self, user_input): # Change between demo mode and editor mode
        pass
    
    def restart(self):
        utils.command("kill python " + sys.argv[0] + "; python " + sys.argv[0], "sub")        




