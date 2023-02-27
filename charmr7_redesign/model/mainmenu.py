from basemenu import BaseMenu
from mainsettingsmenu import MainSettingsMenu
import charmr_module as cm
from view import Display
from model.slideshow import Slideshow
import os

'''
Responsible for monitoring the state of the main menu/launching any main-menu related applications (main menu settings, slideshows, or sketch)
'''
class MainMenu(BaseMenu):
    
    def __init__(self, check_file=cm.check.file, uncheck_file=cm.uncheck.file):

        self.check_file = check_file
        self.uncheck_file = uncheck_file

        # build the menu locations
        self.locations, self.items = self.menu_build("main", '_mainmenu') 

        super(MainMenu, self).__init__()#locations, check_file, uncheck_file)

        # if there is a slideshow being worked with, it is stored here
        self.slideshow = None

        # the class responsible for monitoring main menu settings
        #self.settings = MainSettingsMenu()

        # the class responsible for monitoring sketch NOTE: might be unnecessary since sketch is built into demos and doesn't require much
        # external code
        #self.sketch = Sketch()
    
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
    def process_input(self, user_input):
        if type(user_input) == str: # Button pressed
                            
            if user_input in ['up','down']:
                super().buttons(user_input) # change the buttons appropriately
                #self.display.change_checkmarked_option() 
                
            elif user_input == 'enter':
                pass            
 
        elif type(user_input) == list: # Screen touched           
            selection = self.menu_touch(user_input)
 
            if selection: 
                selection = self.app_selector(selection)
                
                return selection
        
            else: return None

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


