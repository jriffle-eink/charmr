from basemenu import BaseMenu
from model.mainsettingsmenu import MainSettingsMenu
import charmr_module as cm
from view import Display
from model.slideshow import Slideshow

class MainMenu(BaseMenu):
    
    def __init__(self, check_file=cm.check.file, uncheck_file=cm.uncheck.file):

        self.check_file = check_file
        self.uncheck_file = uncheck_file

        self.locations, self.items = self.menu_build("main", '_mainmenu') 

        super(BaseMenu, self).__init__()#locations, check_file, uncheck_file)

        self.slideshow = None

        #self.settings = MainSettingsMenu()

        #self.sketch = Sketch()
                
        self.display = Display()
    
    def launch_sketch_app(self):
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 

    def change_slideshow(arg):
        """
        Changes the slideshow number to the number placed in argument
        """    
        #s_Check = directory + 'check_bar.pgm'; s_Uncheck = directory + 'uncheck_bar.pgm'    

        self.slideshow = Slideshow(int(arg))

        #CHECK(menu.sshw, int(arg)-1, None, s_Check, s_Uncheck)
        
    def process_input(user_input):
        if type(user_input) == str: # Button pressed
                            
            if user_input in ['up','down']:
                super().buttons(user_input) # change the buttons appropriately
                self.display.change_checkmarked_option() 
                
            elif user_input == 'enter':
                pass            
 
        elif type(user_input) == list: # Screen touched           
            selection = super().menu_touch(user_input)
 
            if selection: 
                selection = self.app_selector(selection)
                
                return selection
        
            else: return None

    def app_selector(arg):
        slideshow_number = 1
        app_List = [cm.app1, cm.app2, cm.app3, cm.app4, cm.app5]
        for i in range(arg): # integers 0 to arg-1
            if app_List[i].form == 'slideshow': 
                if i+1 == arg:

                        # #starts the slideshow thread?
                        # auto_slideshow = threading.Thread(target=slideshow_run, args=(self))

                        # auto_slideshow.run()

                        # sets up the selected slideshown and initiates automatic slide progression
                    self.change_slideshow(arg)

                    return self.slideshow

                else: slideshow_number += 1

            elif app_List[i].form == 'sketch': 
                if i+1 == arg: 

                    return self.sketch

