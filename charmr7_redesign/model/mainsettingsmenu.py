from basemenu import BaseMenu
import mainmenu 
import charmr_module as cm
from view import Display

class MainSettingsMenu(BaseMenu):

    def __init__(self, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):
        
        self.items = ['Go to slide', 
                      'Wfm mode #s',
                      'Demo mode',
                      'Restart']
        self.check_file = check_file
        self.uncheck_file = uncheck_file
        self.locations = self.menu_build("menu", '_mainmenu', self.items)
        super(BaseMenu, self).__init__()

        #self.settings = MainMenu() # pressing settings button again goes back to the main menu
        
        #self.sketch = Sketch()
        
        self.display = Display()
    
    def process_input(user_input):
        if type(user_input) == str: # Button pressed
                            
            if user_input in ['up', 'down']:
                super().buttons(user_input) # change the buttons appropriately
                self.display.change_checkmarked_option() 
                
            elif user_input == 'enter':
                pass
 
        elif type(user_input) == list: # Screen touched           
            selection = super().menu_touch(user_input)
 
            if selection: 
                
                
                return selection

    def launch_sketch_app(self):
        os.system("FULL_WFM_MODE=2 PART_WFM_MODE=1 /mnt/mmc/api/tools/acepsketch /mnt/mmc/application/sketch/sketch_app.txt") 

    def go_to_slide(self):
        pass
    
    def wfm_mode_change(self):
        pass
    
    def user_mode_change(self): # Change between demo mode and editor mode
        pass
    
    def restart(self):
        pass



