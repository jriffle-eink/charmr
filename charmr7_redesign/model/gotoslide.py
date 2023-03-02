from basemenu import BaseMenu
import charmr_module as cm
from view import Display

class MainSettingsMenu(BaseMenu):

    def __init__(self, check_file=str(cm.check.file), uncheck_file=str(cm.uncheck.file)):
        
        self.items = ['Go to slide', 
                      'Wfm mode #s',
                      'Demo mode',
                      'Restart']
        
        self.locations = super().menu_build("menu", '_mainmenu', self.items)
        super().__init__(self.locations, check_file, uncheck_file)

        self.settings = MainMenu() # pressing settings button again goes back to the main menu
        
        self.sketch = Sketch()
        
        self.display = Display()
    
    def process_input(user_input):
        if type(user_input) == str: # Button pressed
                            
            if user_input = 'up' or 'down':
                super().buttons(user_input) # change the buttons appropriately
                self.display.change_checkmarked_option() 
                
            elif user_input = 'enter':
                pass
 
        elif type(user_input) == list: # Screen touched           
            selection = super().menu_touch(user_input):
 
            if selection: 
                
                return selection
