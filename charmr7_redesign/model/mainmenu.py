from basemenu import BaseMenu
#from mainsettingsmenu import MainSettingsMenu
import charmr_module as cm
from model.slideshow import Slideshow
import os
import utils

'''
Responsible for monitoring the state of the main menu/launching any main-menu related applications (main menu settings, slideshows, or sketch)
'''
class MainMenu(BaseMenu):
       
    def __init__(self, view, check_file=cm.check.file, uncheck_file=cm.uncheck.file):

        self.tmp_name = 'mainmenu'

        self.check_file = check_file
        self.uncheck_file = uncheck_file

        # build the menu locations
        self.locations = self.menu_build("main", self.tmp_name)
        
        self.view = view

        super(MainMenu, self).__init__(self.view, self.locations, self.check_file, self.uncheck_file)
        super(MainMenu, self).menu_locations(self.locations, 0)
                
        # the class responsible for monitoring main menu settings
        # self.main_settings_menu = MainSettingsMenu(self.view)
        
    def display(self, area = ['header', 'body', 'footer', 'banner']):
        
        self.view.display_main_menu(area) # loads and displays using cmder
        
        self.change_checkmark()
    
    def change_checkmark(self):    
    
        self.view.change_checkmarked_option(self.locations, self.cur_check)
    
    ''' 
    Launches the sketch app
    ''' 
    def launch_sketch_app(self):
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 

    '''
    Changes the slideshow number to the number placed in argument NOTE: remove hardcoding, allow for N number of arguments to select up to 
    N number of slideshows

    ARGUMENTS
    num: int (the slideshow number to change to)
    '''
    def change_slideshow(self, num):
        """
        Changes the slideshow number to the number placed in argument
        """    
        #s_Check = directory + 'check_bar.pgm'; s_Uncheck = directory + 'uncheck_bar.pgm'    

        return Slideshow(int(num))

        #CHECK(menu.sshw, int(arg)-1, None, s_Check, s_Uncheck)
        

    '''
    Selects an application based on user input.

    ARGUMENTS
    user_input: str or list (represnts either a button press (str) or tap touch (list))

    RETURN
    '''
    def process_input(self, user_input): pass
        


    '''
    Selects the application based on the number given NOTE: remove hardcoding, allow for N number of arguments to select up to 
    N number of slideshows

    ARGUMENTS
    arg: int (the index of the menu item to select)

    RETURNS
    The selected argument (either an instance of Sketch() or an instance of Slideshow(cm_slideshow))
    '''     
    def app_selector(self, arg):
        slideshow_number = 1
        app_List = [cm.app1, cm.app2, cm.app3, cm.app4, cm.app5]
        for i in range(arg): # integers 0 to arg-1
            if app_List[i].form == 'slideshow': 
                if i+1 == arg:

                        # #starts the slideshow thread?
                        # auto_slideshow = threading.Thread(target=slideshow_run, args=(self))

                        # auto_slideshow.run()

                        # sets up the selected slideshown and initiates automatic slide progression
                    return self.change_slideshow(arg)

                else: slideshow_number += 1

            elif app_List[i].form == 'sketch': 
                if i+1 == arg: 
                    pass
                    #return self.sketch


