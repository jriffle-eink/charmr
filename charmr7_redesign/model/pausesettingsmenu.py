from basemenu import BaseMenu
import charmr_module as cm
import utils as utils
from settingsmenu import SettingsMenu

class PauseSettingsMenu(SettingsMenu):
    def __init__(self, display, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):


        locations = self.menu_build('menu', '_psettings',
                              ['Go to slide', 
                               'Waveform', 
                               'Rotation', 
                               'Disp/Flsh',
                               'Main menu']
                               ) 

        self.check_file = check_file
        self.uncheck_file = uncheck_file

        super(PauseSettingsMenu, self).__init__(locations, display, check_file, uncheck_file)#locations, check_file, uncheck_file)  


        # used mainly for view purposes to know what items to display
        self.items = ['Go to slide', 'Waveform', 'Rotation', 'Disp/Flsh', 'Main menu']


        self.rot_touch_dict={
            tuple(['rot', '0']): [[470,900],    [670,1100]],
            tuple(['rot', '1']): [[770,900],    [970,1100]],
            tuple(['rot', '2']): [[470,1200],   [670,1400]],
            tuple(['rot', '3']): [[770,1200],   [970,1400]],
        }

        self.disp_flsh_touch_dict={
            tuple(['disp', 'full']): [[300,900],    [510,1100]],
            tuple(['disp', 'part']): [[510,900],    [720,1100]],
            tuple(['flsh', 'none']): [[720,900],    [930,1100]],
            tuple(['flsh', 'full']): [[930,900],   [1140,1100]],
            tuple(['flsh', 'best']): [[300,1100],   [510,1300]],
            tuple(['flsh', 'strd']): [[510,1100],   [720,1300]],
            tuple(['flsh', 'fast']): [[720,1100],   [930,1300]],
            tuple(['auto', 'auto_Opp']): [[930,1100],  [1140,1300]],
        }

    def process_input(self, user_input):
        if self.cur_check == 0:
            if type(user_input) == str: # Button pressed
                                
                if user_input in ['up', 'down']:
                    self.buttons(user_input) # change the buttons appropriately
                    self.display.change_checkmarked_option() 
                    
                elif user_input == 'enter':
                    #selection = self.cur_check
                    self.display.display_psetting_submenu(self.cur_check)
    
            elif type(user_input) == list: # Screen touched           
                self.cur_check = self.menu_touch(user_input)

                if self.cur_check == 5:
                    self.go_to_main()

        else:
            if utils.touch_zone(user_input, self.general_touch_dict['exit']):
                self.cur_check = 0
                return 'main'

            elif utils.touch_zone(user_input, self.general_touch_dict['back']):
                self.cur_check = 0
                self.display.display_psettings()

            elif self.cur_check == 5:
                self.go_to_main()

            else: 
                return self.run_app(user_input)

    

    def run_app(self, user_input):
        if self.cur_check == 1:
            self.retrieve_output(user_input, self.go_to_slide_touch_dict, 'go to slide')
        elif self.cur_check == 2:
            self.retrieve_output(user_input, self.wfm_touch_dict, 'wfm')
        elif self.cur_check == 3:
            self.retrieve_output(user_input, self.rot_touch_dict, 'rot')
        elif self.cur_check == 4:
            self.retrieve_output(user_input, self.disp_flsh_touch_dict, 'dispflsh')
        
    '''
    Returns user to main menu
    '''
    def go_to_main(self):
        # reset current command
        self.cur_check = 0
        return 'main'
